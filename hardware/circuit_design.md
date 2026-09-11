# Circuit design 

## Initial circuit design

The initial circuit is designed to accommodate 1 sensor. Comprises of 1 sensor, 1 capacitor, an arduino nano, a breadboard, and jumper wires. 

<img width="531" height="636" alt="image" src="https://github.com/user-attachments/assets/3a5a7906-1f46-4c14-9a49-0222277bb1ae" />

The sensors VCC pin needs to connect to the Arduino 5 V pin, the GND to the GND and the OUT pin connects to an analogue pin on the Arduino. This circuit design can be used to accommodate many more sensors as well, they will be placed in parallel to each other, each sensor needs its own capacitor and will need its OUT pin to go into a separate analogue PIN on the Arduino. The Arduino nano has 8 output pins so any more sensors than this, will need multiple arduinos. 

Have used a circuit simulator to simulate what it will look like for firstly 1 sensor and then for 2 sensors:
<img width="480" height="584" alt="image" src="https://github.com/user-attachments/assets/57ff9dcb-5307-4815-9fcc-294ae4cc6f97" />

<img width="439" height="532" alt="image" src="https://github.com/user-attachments/assets/78d840ca-11ca-4a92-a55a-d8b3412b1bc2" />
