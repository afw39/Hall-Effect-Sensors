import pandas as pd
import numpy as np
from read import read_data


class Conversion:
    '''
    docstring
    '''

    def __init__(self, port: str, filename: str, number: int, vcc: float, samples: int = 200):
        self.port = port
        self.filename = filename
        self.number = number
        self.vcc = vcc
        self.samples = samples
        self.nulls = None
        self.sensitivities = None
        self.data = None

        self.run()

    def get_params(self) -> None:
        '''
        reads the csv in containing the sensitivities and null voltages, converts them back to arrays
        to be used in the next methods
        Args: 
            None
        Returns:
            self.nulls (np.array): array of length self.number containing null voltage of each sensor,
                calculated during the calibration steps
            self.sensitivities (np.array): array containing the average sensitivity of each sensor,
                calculated during calibration
        '''

        dataframe = pd.read_csv('combined-data.csv')

        self.nulls = np.empty(self.number)
        self.sensitivities = np.empty(self.number)
        self.nulls = dataframe.iloc[0].to_numpy()
        self.sensitivities = dataframe.iloc[1].to_numpy()

    def into_voltage(self) -> None:
        '''
        method for converting the numeric outputs from the sensors into voltages
        the null voltages for each sensor are also subtracted from the data here
        Args:
            None
        Returns:
            None
        '''

        self.data = read_data(self.port, self.filename, self.samples)
        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 4095
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.nulls[i]

    def field_strengths(self) -> pd.DataFrame:
        '''
        docstring
        '''

        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] / self.sensitivities[i]
            if i == 0:
                self.data.rename(columns={self.data.columns[0]: 'time/ms'}, inplace = True)
            self.data.rename(columns={self.data.columns[i+1]:f'field_strength_sensor_{i+1}'}, inplace = True)

        return self.data

    def run(self):
        '''
        docstring
        '''

        self.get_params()
        self.into_voltage()
        self.field_strengths()
