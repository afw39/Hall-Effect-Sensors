from pathlib import Path
import pandas as pd
import numpy as np
from read import read_data


class Conversion:
    '''
    class for converting the raw data read from the hall effect sensors and the Arduino into useful data 
    (field strengths for each sensor and time stamps). Uses the null voltage and sensitivity values 
    calulated during the calibration steps.

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
            reads the csv file where the calibration parameters (null voltages/sensitivity/uncertainties) are stored 
            and saves them as arrays so that they can be used in this class for the conversion
        into_voltage() -> None: 
            multiplies the numbers outputted by the sensors to convert them into voltages,
            and subtracts the null voltage for each sensor off of that sensors readings. Calculates the 
            uncertainty in the voltage at this stage for each sensor
        field_strengths() -> pd.DataFrame: 
            converts the voltages into field strengths by dividing by the sensitivity and calculates the
            associated uncertainty with each field measurement
        display_uncertainty() -> None: 
            uses the calculated fractional uncertainty and applies it to each value of the field
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
        self.nulls_uncertainties = None
        self.sensitivities_uncertainties = None
        self.stds = None
        self.sensor_uncertainty = None
        self.voltage_uncertainty = None
        self.field_uncertainty = None

        self.run()

    def get_params(self) -> None:
        '''
        reads the csv in containing the sensitivities and null voltages, converts them back to arrays
        to be used in the next methods. Also reads in the values calculated previously for the 
        uncertainties in each sensors measurement of the null voltage and sensitivity
        Args: 
            None
        Returns:
            None
        '''

        csv_path = Path(__file__).resolve().with_name("combined-data.csv")
        csv_path_std = Path(__file__).resolve().with_name('std.csv')

        dataframe = pd.read_csv(csv_path)
        self.stds = pd.read_csv(csv_path_std)

        self.nulls = np.empty(self.number)
        self.sensitivities = np.empty(self.number)
        self.nulls_uncertainties = np.empty(self.number)
        self.sensitivities_uncertainties = np.empty(self.number)
        self.nulls = dataframe.iloc[0].to_numpy()
        self.sensitivities = dataframe.iloc[1].to_numpy()
        self.nulls_uncertainties = dataframe.iloc[2].to_numpy()
        self.sensitivities_uncertainties = dataframe.iloc[3].to_numpy()


    def into_voltage(self) -> None:
        '''
        method for converting the numeric outputs from the sensors into voltages
        the null voltages for each sensor are also subtracted from the data here. 
        Calculates the uncertainty associated with each voltage
        Args:
            None
        Returns:
            None
        '''

        self.data = read_data(self.port, self.filename, self.samples)
        self.voltage_uncertainty = [0] * self.number

        for i in range(self.number):
            self.sensor_uncertainty = np.sqrt(0.25 + self.stds.iloc[i, 0])
            average_reading = self.data[self.data.columns[i+1]].mean()

            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / 1023

            average_voltage_1 = self.data[self.data.columns[i+1]].mean()
            readings = self.sensor_uncertainty / average_reading
            vcc = 0.05 / 5.0
            rooted = np.sqrt((readings)**2 + (vcc)**2)
            v1_uncertainty = average_voltage_1 * rooted

            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.nulls[i]

            self.voltage_uncertainty[i] = np.sqrt((self.nulls_uncertainties[i])**2 + (v1_uncertainty)**2)

    def field_strengths(self) -> pd.DataFrame:
        '''
        method for converting the voltages into field strengths using the calculated sensitivity
        values for each sensor from the calibration steps. field strengths are calculated in mT.
        calculates the uncertainty of each field strength measurement
        Args:
            None
        Returns:
            self.data (pd.DataFrame): data frame that now contains the time stamp and the field strengths 
            felt by each sensor in the array
        '''

        self.field_uncertainty = [0] * self.number

        for i in range(self.number):

            voltage = (self.voltage_uncertainty[i]/self.data[self.data.columns[i+1]].mean())**2

            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] / (self.sensitivities[i] / 1000)
            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * 1000

            sensitivity = (self.sensitivities_uncertainties[i]/self.sensitivities.mean())**2
            self.field_uncertainty[i] =  np.sqrt((sensitivity + voltage))
    
            if i == 0:
                self.data.rename(columns={self.data.columns[0]: 'time/s'}, inplace = True)

            self.data.rename(columns={self.data.columns[i+1]:f'field_strength_S{i+1}/mT'}, inplace = True)

        self.data[self.data.columns[0]] = self.data[self.data.columns[0]].astype(float)

        self.data['time/s'] = self.data['time/s'] / 1000

        return self.data

    def display_uncertainty(self) -> None:
        '''
        converts the relative uncertainties for the field strengths into absolute uncertainties and 
        displays them in the output
        Args:
            None
        Returns:
            None
        '''

        field_display = self.data.copy()
        relative_uncertainties = [0] * self.number

        for i in range(self.number):
            column = field_display.columns[i+1]

            relative_uncertainties[i] = self.field_uncertainty[i]

            field_display[column] = field_display[column].apply(lambda x: f'{x:.3f} ± {abs(x*relative_uncertainties[i]):.3f}')

        print(field_display)


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
        self.display_uncertainty()