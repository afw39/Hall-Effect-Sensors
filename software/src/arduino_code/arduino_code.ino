int sensor1 = A0;
int sensor2 = A1;
int sensor3 = A2;
// will add however many sensors I am using

String dataLabel1 = "voltage S1";
String dataLabel2 = "voltage S2";
String dataLabel3 = "voltage S3";
bool label = true;

int data1, data2, data3;

int freq = 1000; //collect a reading every 1 second (in ms)


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600)
  pinMode(sensor1, INPUT)
  pinMode(sensor2, INPUT)
  pinMode(sensor3, INPUT)

}

void loop() {
  // put your main code here, to run repeatedly:

  while(label){ //runs once
    //enable headers
    Serial.print(dataLabel1);
    Serial.print(",");
    Serial.print(dataLabel2);
    label = false;
  }

  data1 = analogRead(sensor1)
  data2 = analogRead(sensor2)
  data3 = analogRead(sensor3)

   // data in CSV format
   Serial.print(data1);
   Serial.print(",");
   Serial.print(data2);
   Serial.print(",");
   Serial.print(data3);
   delay(freq)


}
