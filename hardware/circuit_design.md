# Circuit design 

## Initial circuit design

The initial circuit is designed to accommodate 1 sensor. Comprises of 1 sensor, 1 capacitor, an arduino nano, a breadboard, and jumper wires. 

<img width="531" height="636" alt="image" src="https://github.com/user-attachments/assets/3a5a7906-1f46-4c14-9a49-0222277bb1ae" />

The sensors VCC pin needs to connect to the Arduino 5 V pin, the GND to the GND and the OUT pin connects to an analogue pin on the Arduino. This circuit design can be used to accommodate many more sensors as well, they will be placed in parallel to each other, each sensor needs its own capacitor and will need its OUT pin to go into a separate analogue PIN on the Arduino. The Arduino nano has 8 output pins so any more sensors than this, will need multiple arduinos. 

This is what the 8-sensor array looks like:
<img width="461" height="718" alt="image" src="https://github.com/user-attachments/assets/95391680-1600-4818-a293-6f45fa5313dc" />

<img width="720" height="960" alt="circuit_picture_2" src="https://github.com/user-attachments/assets/953079b6-917d-429e-9380-0d0f079cc0f2" />
<img width="287" height="649" alt="image" src="https://github.com/user-attachments/assets/e027779b-c368-4b6c-880e-10f35751e436" />
