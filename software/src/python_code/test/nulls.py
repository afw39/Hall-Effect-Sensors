from pathlib import Path
import numpy as np
import pandas as pd
from read import read_data

class Nulls:
    '''
    ds
    '''
    def __init__(self, number: int, port: str, vcc: float, filename: str, vcc_un: float, bits: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.bits = bits
        self.filename = filename
        self.samples = samples

        self.levels = ((2**self.bits)-1)

        self.calibration_df = None
        self.null_values = None
        self.stds = None
        self.uncertainties_in_null = None
        self.null_frame = None
        self.std_frame = None

        self.find_params()

    def find_params(self) -> None:
        '''
        calculates the null voltage of each sensor and the standrad deviation of each sensor.
        these values are used in the calculation of the sensitivity of each sensor and in the
        calculation of the uncertainty of each sensor
        '''

        self.calibration_df = read_data(self.port, self.filename, self.samples)
        self.null_frame = pd.DataFrame(np.zeros((2, self.number)), dtype = float)
        self.null_values = [0]*self.number
        self.stds = [0]*self.number
        

        for i in range(self.number):
            mean_entry = (self.calibration_df[self.calibration_df.columns[i+1]]).mean()
            self.null_values[i] = mean_entry * self.vcc / self.levels
            self.stds[i] = (self.calibration_df[self.calibration_df.columns[i+1]]).std(ddof=1)

        self.find_uncertainties_in_null()

    def find_uncertainties_in_null(self)-> None:
        '''
        ds
        '''
        self.uncertainties_in_null = [0]*self.number
        sensor_uncertainty = 0.5
        uncertainty_in_vcc = (self.vcc_uncertainty/self.vcc)**2

        for i in range(self.number):
            average_sensor_reading = (self.calibration_df[self.calibration_df.columns[i+1]]).mean()
            uncertainty_in_reading = ((np.sqrt((sensor_uncertainty)**2+(self.stds[i])**2))/average_sensor_reading)**2
            rooted = np.sqrt(uncertainty_in_reading+uncertainty_in_vcc)
            self.uncertainties_in_null[i] = (rooted*self.null_values[i])

        self.save_values()

    def save_values(self) -> None:
        '''
        ds
        '''
        self.null_frame.iloc[0] = self.null_values
        self.null_frame.iloc[1] = self.uncertainties_in_null

        self.std_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)
        self.std_frame.iloc[0] = self.stds

        file_dir = (Path(__file__).parent)
        output_file_nulls = file_dir/'nulls.csv'
        output_file_stds = file_dir/'stds.csv'

        self.null_frame.to_csv(output_file_nulls, index = False)
        self.std_frame.to_csv(output_file_stds, index = False)
