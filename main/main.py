#Import required modules
# from services import ThermalPlot, PiCam, LED, Relay
import PiCam, ThermalPlot
import startcam
import logging
import threading

if __name__ == "__main__":

    def thread_function(input):
        if input == 0:
            startcam.startthermal() #first to execute
        elif input == 1:
            PiCam.RaspCam() #second to execute
        return

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(2):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,),daemon=True)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)




    
    
    
    

