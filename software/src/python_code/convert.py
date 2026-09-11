import pandas as pd
import numpy as np

class Convert:
    '''
    class is gonna do most of the same that calibrate does but kind of
    backwards and it is gonna use actual data from one field
    '''
    def __init__(self, data: pd.DataFrame, number: int, null_voltages: np.array, vcc: float, sensitivities: np.array):
       self.data = data
       self.number = number
       self.nulls = null_voltages
       self.vcc = vcc
       self.sensitivities = sensitivities

    def adc_to_volts(self) -> pd.DataFrame:
        '''
        converts the adc (0-1023) into voltages and subtracts the null voltages from them
        '''
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 1023
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.nulls[i]
        return self.data

    def field_strength(self) -> pd.DataFrame:
        '''
        multiplies the voltages by the sensitivity values found in the calibration step 
        '''
        for i in range(self.number):
            self.data[f'field_strength_sensor_{i+1}'] = self.data[self.data.columns[i+1]] / self.sensitivities[i]
        return self.data
       