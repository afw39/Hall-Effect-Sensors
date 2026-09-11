import pandas as pd
import numpy as np

class Convert:
    '''
    Converts data from Arduino into magnetic field strengths

    Attributes:
        data (pd.DataFrame): data collected by and read from Arduino
        number (int): number of sensors
        null_voltages (np.array): array of null voltages, one for each sensor, collected in calibration
        vcc (float): VCC value of arduino
        sensitivities (np.array): array of sensitivity values for each sensor, collected in calibration

    Methods:
        adc_to_volts() -> pd.DataFrame:
            converts the ratiometric sensor readings into voltages and subtracts the null voltages
        field_strength() -> pd.DataFrame:
            converts the voltages into field strength using the sensitivities

    '''
    def __init__(self, data: pd.DataFrame, number: int, null_voltages: np.array, vcc: float, sensitivities: np.array):
       self.data = data
       self.number = number
       self.nulls = null_voltages
       self.vcc = vcc
       self.sensitivities = sensitivities

    def adc_to_volts(self) -> pd.DataFrame:
        '''
        converts the ADC Arduino readings into voltages and subtracts the null voltages
        Args:
            None
        Returns:
            data (pd.DataFrame): contains experimental data, now converted to voltages
        '''
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 1023
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.nulls[i]
        return self.data

    def field_strength(self) -> pd.DataFrame:
        '''
        multiplies the voltages by the sensitivity values found in the calibration step 
        Args:
            None
        Returns:
            data (pd.DataFrame): contains voltages and field strengths from experiment
        '''
        for i in range(self.number):
            self.data[f'field_strength_sensor_{i+1}'] = self.data[self.data.columns[i+1]] / self.sensitivities[i]
        return self.data
       