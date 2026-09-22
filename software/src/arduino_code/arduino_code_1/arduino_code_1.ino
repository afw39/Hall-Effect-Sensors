
const float VCC = 3.3;
const int sensor1= A0;
const int sensor2 = A1;


int data1, data2;

String dataLabel1 = "sensor1";
String dataLabel2 = "sensor2";


void setup() {
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  Serial.println("time_ms, sensor1, sensor2");
}

void loop(){
 
  data1 = analogRead(sensor1);
  data2 = analogRead(sensor2);

  Serial.print(millis());
  Serial.print(",");
  Serial.print(data1);
  Serial.print(",");
  Serial.println(data2);

  delay(500); 
}
