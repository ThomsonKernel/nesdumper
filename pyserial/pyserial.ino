#define BAUD 115200

void setup(){
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD);
}

void loop(){
  if (!Serial.available())return;
  switch(Serial.read()){
    case '0': digitalWrite(LED_BUILTIN,LOW); break;
    case '1': digitalWrite(LED_BUILTIN,HIGH); break;
    case '2': Serial.write(digitalRead(2)); break;
  }
}

