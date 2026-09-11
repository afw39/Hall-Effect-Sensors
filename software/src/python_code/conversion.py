# okay we starting fresh - going to code this for just 1 sensor and see how that goes
# if i have the code functionally doing what i want, then can ammend it for more sensors
# main ideas:
 # - need to get arduino data into a csv file somehow - think this is done
 # - need to convert from ADC to voltages
 # - get reading of/calculate the null voltage ( should be approx 2.5V )
 # - then find the sensitivity of sensor
 # - then convert the voltages to field strengths

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import csv
from pathlib import Path

#ser = serial.Serial('COM3', 9600)

# puts data into csv file called 'arduino-data.csv'
def open_csv(ser):
    '''
    docstring
    '''
    with open('arduino-data.csv', 'w', newline = '', encoding = 'utf-8') as csvfile:
        writer = csv.writer(csvfile)
        #saves the headings
        header = ser.readline().decode().strip()
        #splits them by commas into cells
        writer.writerow(header.split(","))

        # read the rest of the data and split them by commas
        while True:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(',')
                writer.writerow(values)
                print(values)
    # closes the file
    ser.close()

#open_csv(ser)

# saving the csv as a dataframe cause i know how to modify dataframes better than csvs

script_dir = Path(__file__).parent
excel_file = script_dir / "arduino-data.xlsx"

data = pd.read_excel(excel_file)
data.to_csv("arduino-data.csv", index = False)

# okay i think that this is actually going to read in the data!
# so currently, this csv file will look like this
#
# time        sensor1           sensor2
# 0            789               775
# 500          843               812
# 1000         797               804
# 1500         802               786
#
# and so on. Need to first convert these numbers into voltages, will have to get the VCC of the Arduino - for now this is 
# going to be 5.0V, can measure it with a multimeter at a later time, for now will just use it as a constant

VCC = 5.0 # VCC of arduino
NUMBER = 4 # number of sensors
KNOWN_FIELD_1 = 0.001 # in mT


class Convert:
    '''
    docstring
    '''

    def __init__(self, dataframe: pd.DataFrame, vcc: float, number: int):
        self.data = dataframe
        self.number = number
        self.vcc = vcc
        self.fields = None
        self.null = None
        self.sensitivity = None


    def adc_to_voltages(self) -> pd.DataFrame:
        '''
        docstring
        '''

        #converting from number to voltage
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 1023

        return self.data

    def null_voltage(self) -> None:
        '''
        docstring
        '''
        # maybe this is another thing, like the calibration that should be a separate thing like will calculate it based off readings 
        # from the arduino where the field is 0 and then get a sensitivity reading from that

        # like i should put this is the calibration module so that i can enter the fields i want to calibrate against in an array
        # and if that field value is 0 then i can do the null voltage
        # so will just say like
        #for field in fields:
        #    if field == 0:
        #        self.null_voltage = calculation for null

        # then can save the null voltage as the voltage outputted whem field is zero.



        # need to find a way to calculate the null voltage - will just read it off sensor, for now using VCC /2
        self.null = self.vcc / 2

        # maybe a way to do it in the future is do it physically, using a multimeter
        # store the values in here:
        #    self.null = np.empty(self.number)

        # -- need to do the actual null calculation now

        # then can use them like this when subtracting them
        #    self.data[self.data.columns[i+1] - self.null[i]]

        # maybe should then convert the voltages that i currently have into the actual like change in voltage? 

        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.null

        # if have array of different null voltages for each sensor will just make above statement self.null[i]

    def calibrate(self, known_field_1: float) -> np.array:
        '''
        docstring
        '''

        # only need to use this to get values for the sensitivites

        self.sensitivity = np.empty(self.number)

        # will call this function and put in the field strength of known field
        for i in range(self.number):
            # will need to do this for each sensor (hence the for loop)
            self.sensitivity[i] = (self.data[self.data.columns[i+1]]).mean() / known_field_1

            # so now i should have one sensitivity for each sensor, stored in the self.sensitivity array
        return self.sensitivity
    
    def convert(self) -> pd.DataFrame:
        '''
        docstring
        '''

        # now will multiply the voltages for each sensor by the sensitivity into a new column each for field

        for i in range(self.number):
            self.data[f"field_strength_sensor_{i+1}"] = self.data[self.data.columns[i+1]] / self.sensitivity[i]

        return self.data

# okay i think this has been successful. this should do what we need it to.I want to test it but will have to run it using a fake dataframe.

def main(dataframe: pd.DataFrame, vcc: float, number: int, field: float):
    '''
    docstring
    '''
    x = Convert(dataframe, vcc, number)
    x.adc_to_voltages()
    x.null_voltage()
    x.calibrate(field)
    dataframe = x.convert()

    print(dataframe.head(5))

    return dataframe

if __name__ == '__main__':
    main(data, VCC, NUMBER, KNOWN_FIELD_1)


# okay this code completely works using the fake csv, will have to hope that it works from extracting the data from the Arduino
# this is the output from `.head(5)`
#      time_ms      sensor1     sensor2    field_strength_sensor_1     field_strength_sensor_2
# 0          0     3.856305    3.787879                   0.002727                    0.002723
# 1        500     4.120235    3.968719                   0.002913                    0.002853
# 2       1000     3.895406    3.929619                   0.002754                    0.002825
# 3       1500     3.919844    3.841642                   0.002772                    0.002762
# 4       2000     3.807429    3.875855                   0.002692                    0.002786
# 
# so i guess i would want to just send the field strengths from each sensor to the software/DAQ and plot them against time. 
# if I had a constant field, then could just take an average reading over all the sensors and plot that against time
#
# i should also add like an actual calculation of the null voltage ( maybe could do something like an initial estimate of the
# null voltage and use that to recalculate that and use the new value going forward )
# i would need to do like a calculation where the software recognises when theres no field - but I can't actually calculate the 
# field without knowing what the null voltage is. 
# 
# 
# going to add some quick plot code to plot the field strength recorded by each sensor against time, will plot both these 
# lines on the same axis

def plot(dataframe: pd.DataFrame, number: int) -> None:
    '''
    docstring
    '''
    colors = ('orange', 'blue', 'green', 'purple', 'red', 'pink')
    fig = plt.figure(figsize = (13, 6))
    ax = fig.add_subplot(1,1,1)

    for i in range(number):
        ax.plot(dataframe[dataframe.columns[0]], dataframe[dataframe.columns[number+i+1]], color = colors[i], label = f'sensor {i+1} fields')

    ax.set_ylabel('Field strength recorded by sensors / T')
    ax.set_xlabel('Time since data collection began / ms')
    ax.set_title('Field strength vs time ')
    ax.legend(loc = 3, prop = {'size': 9})

    plt.show()

plot(data, NUMBER)
