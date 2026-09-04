// will try this generic code for multiple sensors, will try adap it as much as possible

/*
* display multi-analogue
* collects and prints data from multiple analogue sensors
* use with read-serial.py to create csv files easily
*/

int sensor1 = A0;
int sensor2 = A1;
int sensor3 = A2;
// etc, add however many sensors i have

String dataLabel1 = 'Voltage S1';
