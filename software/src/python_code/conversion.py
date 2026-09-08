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
import serial
import csv

ser = serial.Serial('COM3', 9600)

# puts data into csv file called 'arduino-data.csv'
with open('arduino-data.csv', 'w', newline = '') as csvfile:
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

# saving the csv as a dataframe cause i know how to modify dataframes better than csvs
data = pd.read_excel("arduino-data.xlsx")
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
NUMBER = 2 # number of sensors
KNOWN_FIELD_1 = 0.001 # in mT


class Convert:
    '''
    docstring
    '''

    def __init__(self, data: pd.DataFrame, vcc: float, number: int):
        self.data = data
        self.number = number
        self.vcc = vcc
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
        # need to find a way to calculate the null voltage - will just read it off sensor, for now using VCC /2
        self.null = self.vcc / 2

    def calibrate(self, known_field_1: float) -> np.array:
        '''
        docstring
        '''

        # only need to use this to get values for the sensitivites

        self.sensitivity = np.empty(self.number)

        # will call this function and put in the field strength of known field
        for i in range(self.number):
            # will need to do this for each sensor (hence the for loop)
            self.sensitivity[i] = (self.data[self.data.columns[i+1]] - self.null).mean() / known_field_1

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

def main(data: pd.DataFrame, vcc: float, number: int, field: float):
    '''
    docstring
    '''
    x = Convert(data, vcc, number)
    x.adc_to_voltages()
    x.null_voltage()
    x.calibrate(field)
    dataframe = x.convert()

    print(dataframe.head(5))

    return dataframe

if __name__ == '__main__':
    main(data, VCC, NUMBER, KNOWN_FIELD_1)


# okay this works! yay. now will upload this all and tidy up