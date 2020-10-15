#include "log.h"
#include "vospi.h"
#include "falsecolour.h"
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <pthread.h>
#include <semaphore.h>
#include <assert.h>
#include <string.h>
#include <linux/fb.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

/* The Lepton resolution */
#define LEP_WIDTH 160
#define LEP_HEIGHT 120

/* Faux-AGC parameters */
#define MIN_AGC_RANGE 200

// The size of the circular frame buffer
#define FRAME_BUF_SIZE 8

// Positions of the reader and writer in the frame buffer
int reader = 0, writer = 0;

// semaphore tracking the number of frames available
sem_t count_sem;

// a lock protecting accesses to the frame buffer
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

// The frame buffer
vospi_frame_t* frame_buf[FRAME_BUF_SIZE];

/**
 * Read frames from the device into the circular buffer.
 */
void* get_frames_from_device(void* spidev_path_ptr)
{
    char* spidev_path = (char*)spidev_path_ptr;
    int spi_fd;

    // Declare a static frame to use as a scratch space to avoid locking the framebuffer while
    // we're waiting for a new frame
    vospi_frame_t frame;

    // Initialise the segments
    for (int seg = 0; seg < VOSPI_SEGMENTS_PER_FRAME; seg ++) {
      frame.segments[seg].packet_count = VOSPI_PACKETS_PER_SEGMENT_NORMAL;
    }

    // Open the spidev device
    log_info("opening SPI device... %s", spidev_path);
    if ((spi_fd = open(spidev_path, O_RDWR)) < 0) {
      log_fatal("SPI: failed to open device - check permissions & spidev enabled");
      exit(-1);
    }

    // Initialise the VoSPI interface
    if (vospi_init(spi_fd, 20000000) == -1) {
        log_fatal("SPI: failed to condition SPI device for VoSPI use.");
        exit(-1);
    }

    // Synchronise, then receive frames forever
    do {

      log_info("aquiring VoSPI synchronisation");

      if (0 == sync_and_transfer_frame(spi_fd, &frame)) {
        log_error("failed to obtain frame from device.");
        exit(-10);
      }

      log_info("VoSPI stream synchronised");

      do {

          if (!transfer_frame(spi_fd, &frame)) {
            break;
          }

          pthread_mutex_lock(&lock);

          // Copy the newly-received frame into place
          memcpy(frame_buf[writer], &frame, sizeof(vospi_frame_t));

          // Move the writer ahead
          writer = (writer + 1) & (FRAME_BUF_SIZE - 1);

          // Unlock and post the space semaphore
          pthread_mutex_unlock(&lock);
          sem_post(&count_sem);

      } while (1); // While synchronised
    } while (1);  // Forever

}

/**
 * Draw frames to the framebuffer as they become available.
 */
void* draw_frames_to_fb(void* fb_dev_path_ptr)
{
    char* fb_dev_path = (char*)fb_dev_path_ptr;
    struct fb_var_screeninfo v_info;
    struct fb_fix_screeninfo f_info;
    long int screen_size = 0;
    long int line_length = 0;
    int fb_fd;
    char *fb_ptr;

    // Open the framebuffer and obtain some information about it
    fb_fd = open(fb_dev_path, O_RDWR);
    if (!fb_fd) {
      log_error("cannot open framebuffer device.");
      return NULL;
    }

    // Get fixed screen information
    if (ioctl(fb_fd, FBIOGET_FSCREENINFO, &f_info)) {
      log_error("cannot read fb fixed information.");
      return NULL;
    }
    // Get variable screen information
    if (ioctl(fb_fd, FBIOGET_VSCREENINFO, &v_info)) {
      log_error("cannot read fb variable information.");
      return NULL;
    }

    // Change variable info
    v_info.bits_per_pixel = 24;
    v_info.xres = LEP_WIDTH;
    v_info.yres = LEP_HEIGHT;
    if (ioctl(fb_fd, FBIOPUT_VSCREENINFO, &v_info)) {
      log_error("cannot write fb variable information.");
      return NULL;
    }

    // Get variable screen information
    if (ioctl(fb_fd, FBIOGET_VSCREENINFO, &v_info)) {
      log_error("cannot re-read fb variable information.");
      return NULL;
    }
    // Get fixed screen information
    if (ioctl(fb_fd, FBIOGET_FSCREENINFO, &f_info)) {
      log_error("cannot re-read fb fixed information.");
      return NULL;
    }

    // Capture linear display size
    screen_size = f_info.smem_len;
    line_length = f_info.line_length;

    // Print FB details
    log_info(
      "framebuffer spec: %dx%d, %d bpp, lsize: %d, llen: %d",
      v_info.xres, v_info.yres, v_info.bits_per_pixel, screen_size, line_length
    );

    // Mmap the framebuffer
    fb_ptr = (char*)mmap(0, screen_size, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, 0);
    if ((int)fb_ptr == -1) {
      log_error("couldn't mmap the framebuffer");
      exit(1);
    }

    // Declare a frame on the stack to copy data into and use to render from
    vospi_frame_t next_frame;

    while (1) {

      // Wait if there are no new frames to transmit
      sem_wait(&count_sem);

      // Lock the data structure to prevent new frames being added while we're reading this one
      pthread_mutex_lock(&lock);

      // Copy the next frame out ready to transmit
      memcpy(&next_frame, frame_buf[reader], sizeof(vospi_frame_t));

      // Unlock data structure
      pthread_mutex_unlock(&lock);

      // Move the reader ahead
      reader = (reader + 1) & (FRAME_BUF_SIZE - 1);

      // Produce a linear list of pixel values
      uint16_t pix_values[LEP_HEIGHT * LEP_WIDTH];
      uint16_t offset = 0, max = 0, min = UINT16_MAX;
      for (uint8_t seg = 0; seg < VOSPI_SEGMENTS_PER_FRAME; seg ++) {
        for (uint8_t pkt = 0; pkt < VOSPI_PACKETS_PER_SEGMENT_NORMAL; pkt ++) {
          for (uint8_t sym = 0; sym < VOSPI_PACKET_SYMBOLS; sym += 2) {
            pix_values[offset] = next_frame.segments[seg].packets[pkt].symbols[sym] << 8 |
              next_frame.segments[seg].packets[pkt].symbols[sym + 1];

            if (pix_values[offset] > max) {
              max = pix_values[offset];
            }

            if (pix_values[offset] < min) {
              min = pix_values[offset];
            }

            offset ++;
          }
        }
      }

      uint16_t range = max - min;

      // Minimum range
      if (range < MIN_AGC_RANGE) {
        range = MIN_AGC_RANGE;
      }

      // Scale the values appropriately
      for (uint16_t index = 0; index < LEP_HEIGHT * LEP_WIDTH; index ++) {
        pix_values[index] = (uint16_t)(((double)pix_values[index] - min) / range * 254.0);
      }

      // Make sure our thread doesn't advance too fast to avoid blocking waiting for frames
      usleep(1000);

      // Draw the frame to the fb
      uint16_t fb_offset = 0;
      for (int line = 0; line < LEP_HEIGHT; line ++) {
        for(int col = 0; col < LEP_WIDTH; col ++) {
          fb_ptr[line_length * line + (col * 3)] = fc_map[pix_values[fb_offset]][2];
          fb_ptr[line_length * line + (col * 3) + 1] = fc_map[pix_values[fb_offset]][1];
          fb_ptr[line_length * line + (col * 3) + 2] = fc_map[pix_values[fb_offset]][0];
          fb_offset ++;
        }
      }
    }

    munmap(fb_ptr, screen_size);
}

/**
 * Main entry point for the Framebuffer example.
 */
int main(int argc, char *argv[])
{
  pthread_t get_frames_thread, draw_frames_to_fb_thread;

  // Set the log level
  log_set_level(LOG_INFO);

  // Setup semaphores
  sem_init(&count_sem, 0, 0);

  // Check we have enough arguments to work
  if (argc < 2) {
    log_error("Can't start - SPI device file path must be specified.");
    exit(-1);
  }

  // Allocate space to receive the segments in the circular buffer
  log_info("preallocating space for segments...");
  for (int frame = 0; frame < FRAME_BUF_SIZE; frame ++) {
    frame_buf[frame] = malloc(sizeof(vospi_frame_t));
    for (int seg = 0; seg < VOSPI_SEGMENTS_PER_FRAME; seg ++) {
      frame_buf[frame]->segments[seg].packet_count = VOSPI_PACKETS_PER_SEGMENT_NORMAL;
    }
  }

  log_info("Creating get_frames_from_device_thread thread");
  if (pthread_create(&get_frames_thread, NULL, get_frames_from_device, argv[1])) {
    log_fatal("Error creating get_frames_from_device thread");
    return 1;
  }

  log_info("Creating draw_frames_to_fb_thread thread");
  if (pthread_create(&draw_frames_to_fb_thread, NULL, draw_frames_to_fb, "/dev/fb0")) {
    log_fatal("Error creating draw_frames_to_fb_thread thread");
    return 1;
  }

  pthread_join(get_frames_thread, NULL);
  pthread_join(draw_frames_to_fb_thread, NULL);
}
