# WHOLE OF CALIBRATION IN HERE
# so i need the null voltage results and the sensitivities to be in the same class


import pandas as pd
import time
import numpy as np
from read import read_data

class Calibration:
    '''
    doc
    '''

    def __init__(self, field: float, number: int, port: str, vcc: float,
                      filename: str, samples: int = 200, delay: int = 100):
        self.field = field
        self.number = number
        self.port = port 
        self.vcc = vcc
        self.filename = filename
        self.samples = samples
        self.average_null = None
        self.null_values = None
        self.calibration_df = None
        self.null_voltages_averaged = None # array version for calibration 
        self.delay = delay
        self.sensitivities = None
        self.sensitivities_averaged_frame = None
        self.calibration_data = None

    def find_null_voltage(self) -> pd.DataFrame:
        '''
        docstring
        '''
        null_frame = pd.DataFrame(np.zeros((3, self.number)), dtype = float)
        self.average_null = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        for i in range(3):
            self.calibration_df = read_data(self.port,self.filename, self.samples)
            self.null_values = [0] * self.number
            null = [0] * self.number
            for i in range(self.number):
                null[i] = (self.calibration_df[self.calibration_df.columns[i+1]] * self.vcc / 4095).mean()
                self.null_values[i] = (null[i])

            null_frame.iloc[i] = self.null_values
            time.sleep(10)

        self.null_voltages_averaged = np.empty(self.number)
        for i in range(self.number):
            self.null_voltages_averaged[i] = null_frame[null_frame.columns[i]].mean()

        self.average_null.iloc[0] = self.null_voltages_averaged

        return self.average_null, self.null_voltages_averaged

    def perform_calibration(self, fields: np.array, filename: str):
        '''
        doc
        '''
        sensitivity_frame = pd.DataFrame(np.zeros((len(fields), self.number)), dtype = float)
        self.sensitivities_averaged_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        print(f'you have {self.delay} seconds until the data starts to be recorded again')
        time.sleep(self.delay)
   
        how_many_fields = len(fields)
        sensitivities_averaged = np.empty(self.number)

    
        for i in range(how_many_fields):
            self.calibration_data = read_data(self.port, filename, self.samples)

            self.sensitivities = [0] * self.number
            for i in range(self.number):
                self.data[self.calibration_data.columns[i+1]] = self.calibration_data[self.calibration_data.columns[i+1]] - self.null_voltages_averaged[i]
                self.sensitivities[i] = (self.calibration_data[self.calibration_data.columns[i+1]].mean()) / self.field
        


            sensitivity_frame.iloc[i] = self.sensitivities
            print(f'the data will start recording again in {self.delay} seconds')
            time.sleep(self.delay)

        for i in range(self.number):
            sensitivities_averaged[i] = sensitivity_frame[sensitivity_frame.columns[i]].mean()

        self.sensitivities_averaged_frame.iloc[0] = sensitivities_averaged

        return self.sensitivities_averaged_frame

    def make_callable_csv(self):
        '''
        i guess i want this to combine the two dataframes of null voltages
        and sensitivities to be used for the actual data collection
        '''
