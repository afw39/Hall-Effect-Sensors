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
|           |---- calib_script.py    # script to run for calibrating sensors
|           |---- calibrate.py       # does the calibration calculations, determines the sensitivities and null_voltages of the sensors
|           |---- convert.py         # converts the data from ratiometric outputs to field strengths, uses null voltages and sensitivities found in calibrate.py and calib_script.py       
|           |---- data_script.py     # script to run to convert arduino data
|           |---- null_voltage.py    # contains methods for finding the null voltages and sensitivities used in calibrate.py
|           |---- read.py            # contains method for reading in data from arduino into csv, imported and used in many files
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
The structure of the code is confusing as there is a lot of classes, methods and even variables imported from other files. This is necessary as in order to run the calibration for multiple fields, the first calibration must be done using one data file and then another time using another data file for a second field strength for the second calibration. It was easier to put functions such as `read_data`, which reads the arduino data, saves it in a csv and then converts it to a dataframe, in their own file to be easily imported to any file that needs them. 

The null voltages and sensitivities will only need to be found once, at the beginning, during the calibration steps, however the null voltages must be found first and used to calculate the sensitivities. Both these properties need to be used and included in calculations for every data conversion process forward. They are saved as arrays in the `calib_script.py` where the calibration initiates and then imported to be used in the data conversion

### Key classes and methods:
#### Classes: 
scripts contains a class for sensor calibration and data conversion
- `Calibrate`: class inside of `calibrate.py` contains methods to calculate the null voltage and sensitivity of each sensor being calibrated, `null_voltages()` and `calibrate()`. This class is where the actual calculation happens to calibrate the sensor
- `Convert`: class inside of `convert.py` contains methods that convert the experimental ratiometric data from the sensors into voltages in `adc_to_voltages()` and then into field strengths in `field_strength()`. Again this is the actual calculation

#### Methods:
scripts contain many important methods:
- `read_data(port: str, filename: str)`: this method is used in many scripts, this is how the scripts get the data from teh arduino. This takes inputs of what port the arduino is connected to and what name the data should be saved under. It reads it in using the serial library and writes it to a csv file before converting it in a pandas dataframe for data processing. only method found in `read.py`
- `find_null_voltage(field: float, number: int, port: str, vcc: float, filename: str)`: this method has no actual calculations, simply applies the method `null_voltages()` inside of the `Calibrate` class. This method uses the `read_data()` method to get the dataframe and then calibrates it. This method is then imported into the `calib_script.py` script, the function exists in a different script so that there is minimal code in the `calib_script.py`
- `sensor_sensitivities(number: int, sen_data_1: np.array, sen_data_2: np.array)`: this method is a simple method that takes the two arrays of sensitivities for the sensors (1 array per calibration field) and finds the average for each sensor, the return of this function is an array that is then used as the sensitivities of the sensors going forward

After the data has been through the `Convert` class, the dataframe looks like this (performed with 4 sensors in the circuit):
<img width="1870" height="162" alt="image" src="https://github.com/user-attachments/assets/540f7c54-473e-4cb4-af4a-fbcc221fb5bf" />
