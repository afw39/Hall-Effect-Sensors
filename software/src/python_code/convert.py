# wanna leave the other one as is so will do this here

# so will have the data being passed through here, will have the null_voltage that was calculated in the other script
# and will have the sensitivity for each sensor stored in an array 

# need to work out how the calibration will work, maybe the calibration script works for 1 field and like appends an empty list for sensitivity 
# and in the example script can put the for loop in to run it for how many fields, so i will just code the calibrate class once and get it to ammend the list? 

import pandas as pd
import numpy as np
import serial
import csv
from pathlib import Path

def read(port: str) -> pd.DataFrame:
    '''
    docstring
    '''
    ser = serial.Serial(port, 9600)
    script_dir = Path(__file__).parent
    csv_file = script_dir / "arduino-data.csv"

    with open(csv_file, 'w', newline = '', encoding = 'utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        header = ser.readline().decode().strip()
        writer.writerow(header.split(","))

        while True:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(',')
                writer.writerow(values)
                print(values)
    # closes the file
    ser.close()

    data = pd.read_csv(csv_file)
    return data


class Convert:
    '''
    docstring
    '''

    def __init__(self, dataframe: pd.DataFrame, vcc: float, number: int, null_voltages: np.array, sensitivities: np.array):
        self.data = dataframe
        self.number = number
        self.vcc = vcc
        self.null_voltages = null_voltages
        self.sensitivities = sensitivities

    def adc_to_voltages(self) -> pd.DataFrame:
        '''
        docstring
        '''
        #converting from number to voltage
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 1023

        return self.data
    
    def convert(self) -> pd.DataFrame:
        '''
        docstring
        '''

        for i in range(self.number):
            self.data[f"field_strength_sensor_{i+1}"] = self.data[self.data.columns[i+1]] / self.sensitivity[i]

        return self.data
