#ifndef TELEMETRY_H
#define TELEMETRY_H
#include "vospi.h"
#include <stdint.h>

#define LEPTON_WORD(buf, i) buf[i] << 8 | buf[i + 1]
#define LEPTON_DWORD(buf, i) LEPTON_WORD(buf, i + 2) << 16 | LEPTON_WORD(buf,i)
#define LEPTON_QWORD(buf, i) LEPTON_DWORD(buf, i + 4) << 32 | LEPTON_DWORD(buf,i)

typedef struct {

 uint16_t pixel0;
  uint16_t pixel2;
  uint16_t pixel4;
  uint16_t pixel6;
  uint16_t pixel8;
  uint16_t pixel10;
  uint16_t pixel12;
  uint16_t pixel14;
  uint16_t pixel16;
  uint16_t pixel18;
  uint16_t pixel20;
  uint16_t pixel22;
  uint16_t pixel24;
  uint16_t pixel26;
  uint16_t pixel28;
  uint16_t pixel30;
  uint16_t pixel32;
  uint16_t pixel34;
  uint16_t pixel36;
  uint16_t pixel38;
  uint16_t pixel40;
  uint16_t pixel42;
  uint16_t pixel44;
  uint16_t pixel46;
  uint16_t pixel48;
  uint16_t pixel50;
  uint16_t pixel52;
  uint16_t pixel54;
  uint16_t pixel56;
  uint16_t pixel58;
  uint16_t pixel60;
  uint16_t pixel62;
  uint16_t pixel64;
  uint16_t pixel66;
  uint16_t pixel68;
  uint16_t pixel70;
  uint16_t pixel72;
  uint16_t pixel74;
  uint16_t pixel76;
  uint16_t pixel78;
  uint16_t pixel80;
  uint16_t pixel82;
  uint16_t pixel84;
  uint16_t pixel86;
  uint16_t pixel88;
  uint16_t pixel90;
  uint16_t pixel92;
  uint16_t pixel94;
  uint16_t pixel96;
  uint16_t pixel98;
  uint16_t pixel100;
  uint16_t pixel102;
  uint16_t pixel104;
  uint16_t pixel106;
  uint16_t pixel108;
  uint16_t pixel110;
  uint16_t pixel112;
  uint16_t pixel114;
  uint16_t pixel116;
  uint16_t pixel118;
  uint16_t pixel120;
  uint16_t pixel122;
  uint16_t pixel124;
  uint16_t pixel126;
  uint16_t pixel128;
  uint16_t pixel130;
  uint16_t pixel132;
  uint16_t pixel134;
  uint16_t pixel136;
  uint16_t pixel138;
  uint16_t pixel140;
  uint16_t pixel142;
  uint16_t pixel144;
  uint16_t pixel146;
  uint16_t pixel148;
  uint16_t pixel150;
  uint16_t pixel152;
  uint16_t pixel154;
  uint16_t pixel156;
  uint16_t pixel158;
  
} telemetry_data_t;

telemetry_data_t parse_telemetry_packet(vospi_packet_t* packet);

#endif
