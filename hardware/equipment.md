# Equipment List

## Initial component order

To start with, will make a smaller experimental setup to ensure that the circuit is correct and the software works with it. The components being used for this are as follows:

### Hall effect sensors
* ordered 10 analog hall effect sensors to start with
* the sensors being used for this project are SS495A sensors
* they are ratiometric sensors so output a value between 0 and 1023 rather than directly outputted a voltage. This value is proportional to the voltage outputted and is scaled by the the VCC/1023
* the VCC is 5 V for these sensors
* they measure magnetic field strength/voltages in only one direction at a time

### Capacitors
* the capacitors ordered are 100nF capacitors and they will help with noise reduction of the signal
* these are placed in parallel with the sensors, geographically as close as possible to them
* these might prove obsolete when the DAQ gets involved as that should also help with noise reduction

### Arduino
* using an Arduino nano for this project - is very small so should work well
* has a 5 VDC output which is perfect for the SS495A sensors being used
* has 8 analog output pins so when scaling up the project will need multiplexers

### DAQ
* the DAQ being used is the spec of NI-9219
* will be used to take the data from the arduino and into the computer.

### Others
* Breadboard - ordered two small breadboard, to start with will be using this - gives structure to the array and is handy for testing and constructing circuits
* Jumper wires - ordered a variety of types for whatever i might need them for (30 x male to male, 10 x female to male and 10 x female to female)
* USB cable - will be used to connect the arduino nano to laptop

Everything above was ordered for the initial setup, the circuit is being improved to accommodate many more sensors into the array, the equipment above will all be used in the new setup as well, with the addition of everything below. 

--------------------------------------------------------------------------------------------------------------------------------------

## New component order 

### Wires
* 30 x male to female breadboard jumper wires
* 40 x female to female breadboard jumper wires
* 60 x male to male
* 5 x grove cables
* 10 x grove to male jumper cables
* 10 x grove to female jumper cables

### Sensors/capacitors
* 20 x SS495A Hall Effect Sensors (same as before)
* 20 x 0.1 microF Capacitors (same as before)

### Others
* 1 x extra breadboard for wire channels (might not be necessary)
* 6 x ADS1115 ADC module
* 1 x grove shield for Arduino nano
* 1 x 8-port I2C hub multiplexer



