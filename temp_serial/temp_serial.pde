const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  
  if (Serial.read()==0x00){
  // read the analog in value:
    sensorValue = analogRead(analogInPin);            

    //Serial.write(highByte(sensorValue));      
    // can get away with just sending low byte for low temperatures
    Serial.write(lowByte(sensorValue));      

  }
  delay(500);                     
}
