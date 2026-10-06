'''ds'''

# imports
from pathlib import Path
import numpy as np
import pandas as pd
from read import read_data

class Nulls:
    '''
    doc
    '''
    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str, bits: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.data = None
        self.nulls = None
        self.stds = None
        self.uncertainties = None
        self.null_frame = None
        self.std_frame = None



        # so we will say that this data looks like this:
        # time/ms |  sensor 1  |  sensor 2  |  sensor 3  | 
        # 50      |  512       |  513       |  511       |    
        # 100     |  513       |  514       |  512       |
        # 150     |  514       |  511       |  510       |
        # 200     |  511       |  509       |  512       |
        # ------------------------------------------------
        #
        # so we will say that A0 is sensor 1, in the x direction, A2 is sensor 2 in the y direction,
        # A2 sensor 3 in the z direction so they will have a different field to calibrate against
        # but calculating the null voltage should be the same
            


    def find_parameters(self) -> None:
        '''
        docstring
        '''
        self.data = read_data(self.port, self.filename, self.samples)

        self.nulls = np.empty(self.number)
        self.stds = np.empty(self.number)

        for i in range(self.number):
            mean_value = self.data[self.data.colums[i+1]].mean()
            self.nulls[i] = mean_value * self.vcc / self.bits
            self.stds[i] = (self.data[self.data.columns[i+1]]).std(ddof=1)

        self.uncertainty()

    def uncertainty(self) -> None:
        '''ds'''

        self.uncertainties = np.empty(self.number)
        count_uncertainty = 0.5
        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        for i in range(self.number):
            mean_reading = (self.data[self.data.columns[i+1]]).mean()
            uncertainty_in_reading  = ((np.sqrt((count_uncertainty)**2 + (self.stds[i])**2))/mean_reading)**2
            rooted = np.sqrt(uncertainty_in_reading + vcc_uncertainty)
            self.uncertainties[i] = (rooted*self.nulls[i])

        self.save_values()

    def save_values(self) -> None:
        '''ds'''
        self.null_frame = pd.DataFrame(np.zeros((2, self.number)), dtype = float)
        self.std_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        self.null_frame.iloc[0] = self.nulls
        self.null_frame.iloc[1] = self.uncertainties
        self.std_frame.iloc[0] = self.stds

        file_dir = Path(__file__).parent
        output_file_nulls = file_dir / 'nulls.csv'
        output_file_stds = file_dir / 'stds.csv'

        self.null_frame.to_csv(output_file_nulls, index = False)
        self.std_frame.to_csv(output_file_stds, index = False)
