# Software Overview

The software in this project is responsible for taking the data collected by the hall effect sensors and converting it into useful magnetic field strength data. It comprises of arduino software for data collection and python software for converting the raw data into useful data. 

## Structure of software directory
```
software/
|---- README.md
|---- src/
|     |---- arduino_code/
|           |---- arduino_code.ino   # code for data collection
|     |---- python_code/
|           |---- conversion.py      # code for data conversion
```

## Arduino code
This is pretty simple software. Uses the serial monitor to print a time stamp and also the sensor reading for however many sensors is being used. Very customisable and scalable for any number of sensors, will simply create a new column in the code. 
<img width="1076" height="706" alt="image" src="https://github.com/user-attachments/assets/8791c006-0acb-45ad-8cb5-29af59010a5b" />

## Python code
libraries used: pandas, numpy, matplotlib, serial, csv, pathlib
The python code is where most of the data processing will occur, when it recieves the data from the arduino, it reads it and saves it as a csv. This is then converted into a pandas dataframe for easier use. 

When the data arrives it is a table that will look something like this:
```
.......................................
 time        sensor1           sensor2
 0            789               775
 500          843               812
 1000         797               804
 1500         802               786
.......................................
```

### Key classes and methods:
The only class is the `Convert` class, this contains all the methods for data conversion and processing.
- `adc_to_voltages() -> pd.DataFrame` = converts the data style above into voltages, replaces the existing columns with the voltages
- `null_voltage() -> None` = calculates the null voltage of each sensor, this is like a systematic error - its the voltage outputted when there is no magnetic field - usually about half of the value of the VCC. This value is then subtracted off of all voltages
- `calibrate(known_field_1:float) -> np.array` = calibrates the hall effect sensor. Uses a known field strength and takes the voltages from the sensors and uses that to calculate the sensitivity of each sensor. The sensitivity of the sensor is the scale factor to convert between voltages and magnetic field strengths.
- `convert() -> pd.DataFrame` = this is used in unknown fields and uses the previously calculated sensitivity values for each sensor in the calibration method to calculate the field strengths at each sensor location.

The final method which is outside of the `Convert` class:
- `plot(data: pd.DataFrame, number: int) -> None` = produces a plot of magnetic field strength against time in ms for however many sensors there is data for.
This will not be the final visualisation method as the data will be plotted as a live feed into the matchID software in the final project but until then, am using this method to see the data. That is why it is not a method within the `Convert` class.

After the data has been through the `Convert` class, the dataframe looks like this (performed with 4 sensors in the circuit):
<img width="1870" height="162" alt="image" src="https://github.com/user-attachments/assets/540f7c54-473e-4cb4-af4a-fbcc221fb5bf" />
