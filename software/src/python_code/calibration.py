# gonna have a separate script/class for the calibration so that it doesnt like need to be run every time with the normal conversion code

import numpy as np
import pandas as pd
import serial
import csv
from pathlib import Path

# going to use completely separate dataframe i think for the calibration so if need to calibrate the sensors can run this script but it 
# will be completely independent of the data processing script and will be different data as it will come from different fields
# will need to run something for each field value probs???

# so will be reading in data from the arduino again, save as a csv and then a dataframe
# for now will just use an empty dataframe

# want to read in the calibration data
def calibration_read(port: str) -> pd.DataFrame:
    '''
    docstring
    '''
    ser = serial.Serial(port, 9600)
    script_dir = Path(__file__).parent
    csv_file = script_dir / "calibration-data.csv"

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

    calibrate_df = pd.read_csv(csv_file)
    return calibrate_df


class Calibrate:
    def __init__(self, dataframe: pd.DataFrame, number: int, field: float) -> np.array:
        self.number = number
        self.data = dataframe
        self.fields = field
        self.sensitivity = None
        self.null = None

    def null_voltages(self)-> np.array:
        self.null_values = np.empty(self.number)
        for i in range(self.number):
            self.null[i] = (self.data[self.data.columns[i+1]] * 5 / 1023).mean()
            self.null_values = self.null_values.append(self.null[i])
        return self.null_values
         
    

