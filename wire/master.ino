#include <Wire.h>
#define BAUD 115200
#define SLAVE_ADDRESS 0x08

void setup(){
  Serial.begin(BAUD);
  Wire.begin();
}

void loop(){
  if (!Serial.available())return;
  slave(Serial.read());
}
void slave(int c){
  Wire.beginTransmission(SLAVE_ADDRESS);
  Wire.write(c);
  Wire.endTransmission();
}
