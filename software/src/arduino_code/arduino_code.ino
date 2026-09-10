const float VCC = 5.00;
const int sensor1= A0;
const int sensor2 = A1;

int data1, data2;

String dataLabel1 = "sensor1";
String dataLabel2 = "sensor2";

void setup() {
  Serial.begin(9600);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}

void loop(){

  // can add a like while millis < x for a timed sample intake, or can do a while samples < x as well if want to
  
  if(label){
    Serial.print("time_ms");
    Serial.print(",");
    Serial.print(dataLabel1);
    Serial.print(",");
    Serial.println(dataLabel2);
  }

  data1 = analogRead(sensor1);
  data2 = analogRead(sensor2);
  // printing the data as reading_1, reading_2 under the dataLabel headings above
  Serial.print(millis());
  Serial.print(",");
  Serial.print(data1);
  Serial.print(",");
  Serial.println(data2);

  delay(500); // takes one reading every 500 ms
}

// should work for as many sensors as i need, can print them all in a line separated by commas, read them into python
// as a csv and then do it from there
// will produce something like this
// time_ms      sensor1     sensor2
//       0       680          703    
//     500       702          689
//    1000       695          688
//    1500       687          694
//    2000       793          707
 
