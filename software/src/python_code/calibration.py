import time
from pathlib import Path
import pandas as pd
import numpy as np
from read import read_data

class Calibration:
    '''
    Class for calibrating the sensors, calculates the calibration
    parameters of the null voltage and the sensitivity of each
    sensor

    Attributes 
        number (int): number of sensors present in the array
        port (str): name of the computer port the arduino is linked to
        vcc (float): value of the VCC output from the arduino
        filename (str): csv filename the data is stored in
        samples (int): how many data samples each reading takes
        delay (int): the time between calibration recordings 

    Methods:
        find_null_voltage() -> pd.DataFrame:
            computes and stores null voltages for each sensor in the array
        perform_calibration() -> pd.DataFrame:
            computes and stores the average value for sensitivity for each sensor
    '''

    def __init__(self, number: int, port: str, vcc: float,
                      filename: str, samples: int = 200, delay: int = 100):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.samples = samples
        self.delay = delay
        self.average_null = None
        self.null_values = None
        self.calibration_df = None
        self.null_voltages_averaged = None
        self.sensitivities = None
        self.sensitivities_averaged_frame = None
        self.calibration_data = None

        self.find_null_voltage()

    def find_null_voltage(self) -> None:
        '''
        method that computes the null voltage for each sensor in the array,
        takes an average and saves them to an empty data frame
        Args:
            None
        Returns:
            None
        '''
        null_frame = pd.DataFrame(np.zeros((3, self.number)), dtype = float)
        self.average_null = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        for i in range(3):
            self.calibration_df = read_data(self.port,self.filename, self.samples)
            self.null_values = [0] * self.number
            null = [0] * self.number
            for x in range(self.number):
                null[x] = (self.calibration_df[self.calibration_df.columns[x+1]] * self.vcc / 4095).mean()
                self.null_values[x] = (null[x])

            null_frame.iloc[i] = self.null_values
            if i+1 < 3:
                time.sleep(10)

        self.null_voltages_averaged = np.empty(self.number)
        for i in range(self.number):
            self.null_voltages_averaged[i] = null_frame[null_frame.columns[i]].mean()

        self.average_null.iloc[0] = self.null_voltages_averaged


    def perform_calibration(self, fields: np.array) -> None:
        '''
        uses the null voltages calculated previously and calculates the average
        sensitivity of each sensor using known values of the calibration field strengths
        sensitivities are calculated in units of mV/T
        Args:
            fields (np.array): array containing the values of each calibration field strength 
        Returns:
            None 
        '''
        sensitivity_frame = pd.DataFrame(np.zeros((len(fields), self.number)), dtype = float)
        self.sensitivities_averaged_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        print(f'you have {self.delay} seconds until the data starts to be recorded again')
        time.sleep(self.delay)
   
        how_many_fields = len(fields)
        sensitivities_averaged = np.empty(self.number)

        # im not sure in here the data has been converted yet??? where do i do the (* vcc / 4095) nowhere??
    
        for i in range(how_many_fields):
            self.calibration_data = read_data(self.port, self.filename, self.samples)

            self.sensitivities = [0] * self.number
            for x in range(self.number):
                self.calibration_data[self.calibration_data.columns[x+1]] = self.calibration_data[self.calibration_data.columns[x+1]] * self.vcc / 4095
                self.calibration_data[self.calibration_data.columns[x+1]] -= self.null_voltages_averaged[x]
                self.sensitivities[x] = (self.calibration_data[self.calibration_data.columns[x+1]].mean()) / fields[i]
                self.sensitivities[x] = self.sensitivities[x] * 1000000

            sensitivity_frame.iloc[i] = self.sensitivities
            if i+1 == how_many_fields:
                print('data recording complete...')
                
            else:
                print(f'the data will start recording again in {self.delay} seconds...')
            time.sleep(self.delay)

        for i in range(self.number):
            sensitivities_averaged[i] = sensitivity_frame[sensitivity_frame.columns[i]].mean()

        self.sensitivities_averaged_frame.iloc[0] = sensitivities_averaged

        self.make_callable_csv()


    def make_callable_csv(self) -> None:
        '''
        combines the two data frames containing null voltages and sensitivities for 
        each sensor into one to convert that to a csv. This is done so that the values
        can be accessed during the actual data recording by calling on the csv
        Args:
            None
        Returns:
            None
        '''
        combined_df = pd.concat([self.average_null, self.sensitivities_averaged_frame])
        script_dir = Path(__file__).parent
        output_file = script_dir/'combined-data.csv'
        combined_df.to_csv(output_file, index = False)
