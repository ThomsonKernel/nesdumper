#include <Wire.h>
#define BAUD 115200
#define ROMSEL A0
#define PPU_RD A1
#define CIRAM_A10 A2
/////// for I2C ////////
#define SLAVE_ADDRESS 0x20
#define IODIRA 0x00
#define OLATA 0x14
#define ack; Serial.write(0xFF);
static bool standby;
void setup(){
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(ROMSEL,OUTPUT);
  pinMode(PPU_RD,OUTPUT);
  Serial.begin(BAUD);
  Wire.begin();
  write_(IODIRA,0x00,0x00);
  standby=true;
  digitalWrite(ROMSEL,HIGH);
  digitalWrite(PPU_RD,HIGH);
  ack;
}
void loop(){
  if(standby){
    int opecode=Serial.read();
    switch(opecode){
      case -1: led(500); return;
      case CIRAM_A10:
           write_(OLATA,0x04,0x00);
           Serial.write(digitalRead(CIRAM_A10));
           break;
      case ROMSEL: case PPU_RD:
        digitalWrite(opecode,LOW);
        standby=false;
        ack;
    }
  }
  if(Serial.available()<2)return;
  byte upper=Serial.read();
  byte lower=Serial.read();
  write_(OLATA,upper,lower);
  Serial.write(read_());
}

#define MASK B11100000
byte read_(){
  return (PIND&MASK) | (PINB&~MASK);
} 
void write_(byte addr,byte upper,byte lower){
  Wire.beginTransmission(SLAVE_ADDRESS);
  Wire.write(addr);
  Wire.write(upper);
  Wire.write(lower);
  Wire.endTransmission();
}
void led(int microsecond){
  digitalWrite(LED_BUILTIN,HIGH);
  delay(microsecond);
  digitalWrite(LED_BUILTIN,LOW);
  delay(microsecond);
}
