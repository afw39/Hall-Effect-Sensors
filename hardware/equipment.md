# Equipment List

# Initial component order

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
* has 8 analog output pins so when scaling up the project will need multiple sensors

### DAQ
* the DAQ being used is the spec of NI-9219
* will be used to take the data from the arduino and into the computer.

### Others
* Breadboard - ordered two small breadboard, to start with will be using this - gives structure to the array and is handy for testing and constructing circuits
* Jumper wires - ordered a variety of types for whatever i might need them for
* USB cable - will be used to connect the arduino to the DAQ
