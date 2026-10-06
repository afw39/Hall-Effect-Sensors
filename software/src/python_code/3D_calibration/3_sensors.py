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



class sensitivity:
    '''ds'''

    def __init__(self,number: int, port: str, vcc: float, vcc_un: float, filename: str, bits: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.nulls = None
        self.data = None
        self.stds = None
        self.nulls_uncertainties = None
        self.sensitivities = None
        self.uncertainty = None

        self.get_params()
    

    def get_params(self) -> None:
        '''ds'''
        self.nulls = np.empty(self.number)
        self.nulls_uncertainties = np.empty(self.number)
        self.stds = np.empty(self.number)

        path_nulls = Path(__file__).resolve().with_name('nulls.csv')
        parameters_df = pd.read_csv(path_nulls)

        path_stds = Path(__file__).resolve().with_name('stds.csv')
        stds_df = pd.read_csv(path_stds)

        self.nulls = parameters_df.iloc[0].to_numpy()
        self.nulls_uncertainties = parameters_df.iloc[1].to_numpy()
        self.stds = stds_df.iloc[0].to_numpy()

        self.perform_calibration(field = [34, 56, 36], field_uncertainty = 0.05)

    def perform_calibration(self, field: np.array, field_uncertainty: float) -> None:
        '''ds'''

        self.data = read_data(self.port, self.filename, self.samples)

        df = self.data.copy()

        uncertainty_in_sensor = 0.5
        field = [34, 56, 34] # x, y, z field values in mT

        self.sensitivities = np.empty(self.number)
        self.uncertainty = np.empty(self.number)

        uncertainty_in_vcc = (self.vcc_uncertainty / self.vcc)

        # going to say that sensor 1 has the x data, sensor 2 has the y and sensor 3 has the z

        for i in range(3): # going to just do with three sensors for now
            average_data = df[df.columns[i+1]].mean()
            reading_uncertainty = ((np.sqrt(((uncertainty_in_sensor)**2)+(self.stds[i])**2))/average_data)**2

            average_voltage_value = df[df.columns[i+1]].mean()
            uncertainty_in_volt = (np.sqrt(reading_uncertainty + uncertainty_in_vcc))*average_voltage_value
            uncertainty_in_volt_nulls = (np.sqrt(((uncertainty_in_volt)**2)+ ((self.nulls_uncertainties[i])**2)))

            self.data[self.data.columns[i+1]] = (self.data[self.data.columns[i+1]] * self.vcc / self.bits) - self.nulls[i]

            third = ((uncertainty_in_volt_nulls)/(self.data[self.data.columns[1]].mean()))**2
            fourth = ((field_uncertainty)/field[i])**2

            self.sensitivities[i] = ((self.data[self.data.columns[i+1]].mean())/field[i])*1000
            self.uncertainty[i] = (np.sqrt(third+fourth))*self.sensitivities[i]

        sens_x, sens_y, sens_z = self.sensitivities[0], self.sensitivities[1], self.sensitivities[2]
        uncertainty_x, uncertainty_y, uncertainty_z = self.uncertainty[0], self.uncertainty[1], self.uncertainty[2]

        # okay so now should have the value of sensitivity and their uncertainty from one calibration field
        # in 3 directions. when i have way more sensors will need a better plan. (should try without the uncertainties first lowkey)

    

        







        


