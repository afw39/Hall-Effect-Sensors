import pandas as pd
import numpy as np
from read import read_data


class Conversion:
    '''
    class for converting the raw data read from the hall effect sensors and the Arduino into useful data (field
    strengths for each sensor and time stamps). Uses the null voltage and sensitivity values calulated during
    the calibration steps.

    Attributes:
        port (str): the port of the computer that the arduino/hall effect sensor array is plugged in to
        filename (str): the name of the csv file that stores the data being read - is converted to a 
            pandas dataframe for easier manipulation
        number (int): the number of sensors in the array - provides information for how many iterations 
            are required
        vcc (float): the VCC (voltage output) of the arduino into the sensors
        samples (int): the number of data samples taken 
    
    Methods:
        get_params() -> None: 
            reads the csv file where the calibration parameters are stored and saves them
            as arrays so that they can be used in this class for the conversion
        into_voltage() -> None: 
            multiplies the numbers outputted by the sensors to convert them into voltages,
            and subtracts the null voltage for each sensor off of that sensors readings
        field_strengths() -> pd.DataFrame: 
            converts the voltages into field strengths by dividing by the sensitivity
        run() -> None: 
            method for running the other methods in the class
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
            None
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
        method for converting the voltages into field strengths using the calculated sensitivity
        values for each sensor from the calibration steps
        Args:
            None
        Returns:
            self.data (pd.DataFrame): data frame that now contains the time stamp and the field strengths felt 
            by each sensor in the array
        '''

        for i in range(self.number):
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] / self.sensitivities[i]
            if i == 0:
                self.data.rename(columns={self.data.columns[0]: 'time/ms'}, inplace = True)
            self.data.rename(columns={self.data.columns[i+1]:f'field_strength_sensor_{i+1}'}, inplace = True)

        return self.data

    def run(self):
        '''
        method for running the methods within this class. This method is called in the 
        `__init__()` method and allows the class to be called from outside only once
        Args:
            None
        Returns:
            None
        '''

        self.get_params()
        self.into_voltage()
        self.field_strengths()
