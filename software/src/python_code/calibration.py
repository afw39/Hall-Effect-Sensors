import numpy as np
import pandas as pd

class Calibrate:
    '''
    Calibrates the hall effect sensor, scalable to any number of sensors.
    Determines sensitivity and null voltage of sensors to be used in data processing

    Attributes:
        dataframe (pd.DataFrame): the calibration data frame
        number (int): number of sensors
        field (float): known value of calibration field
        vcc (float): VCC of Arduino

    Methods:
        null_voltages() -> np.array: calculates the null voltage (voltage outputted when field is 0)
        calibrate() -> np.array: determines the sensitivity of each sensor in a field
        
    '''
    def __init__(self, dataframe: pd.DataFrame, number: int, field: float, vcc: float) -> np.array:
        self.number = number
        self.data = dataframe
        self.field = field
        self.vcc = vcc
        self.null_values = None
        self.sensitivities = None

    def null_voltages(self) -> np.array:
        '''
        docstring
        '''
        self.null_values = np.empty(self.number)
        null = np.empty(self.number)
        for i in range(self.number):
            null[i] = (self.data[self.data.columns[i+1]] * self.vcc / 1023).mean()
            self.null_values = self.null_values.append(null[i])
        return self.null_values

    def calibrate(self):
        '''
        docstring
        '''
        sensitivity = np.empty(self.number)
        self.sensitivities = np.empty(self.number)
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.null_values
            sensitivity[i] = (self.data[self.data.columns[i+1]].mean()) / self.field
            self.sensitivities = self.sensitivities.append(sensitivity[i])
        return self.sensitivities
