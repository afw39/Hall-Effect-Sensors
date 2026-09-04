const int hallPin = A0; // connects the pin A0 to the hall effect sensor
const int TimeDelay = 1000; // set a time interval of data collection to 1 per second (in ms)

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // serial communication started - sends one bit at a time sequentially
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue = analogRead(hallPin); // reads/gives values between 0-1023 based on voltage
  Serial.print('Voltage value: ');
  Serial.println(sensorValue); // prints voltage outputted at regular time intervals
  delay(TimeDelay); // waits the time delay before taking another reading


// this will hopefully be sufficient for one sensor at least and might have to ammend it for multiple, cant really run it right now cause
// its not actaully hooked up to an arduino so we will see how this goes.