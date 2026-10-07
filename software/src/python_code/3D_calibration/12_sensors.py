# imports
from pathlib import Path
from csv import writer
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



        # so we will say that this data looks like this: (except will be for 12 sensors)
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


class Calib_3D:
    '''ds'''

    def __init__(self, number: int, port: str, vcc: float, vcc_uncertainty: float, filename: str, bits: int, samples: int=400):
        self.number = number # must be divisible by 3
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_uncertainty
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.nulls = None
        self.data = None
        self.data2 = None
        self.stds = None
        self.nulls_uncertainties = None
        self.sensitivity_frame = None
        self.uncertainty = None 
        self.data = None

        self.get_nulls()

    def get_nulls(self):
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

    def perform_calibration(self, field: np.array, field_uncertainty: float=0.05) -> None:
        '''
        ds
        '''
        sensor_uncertainty = 0.5
        self.data = read_data(self.port, self.filename, self.samples)

        self.data2 = self.data.copy()

        sensitivities = np.empty(self.number)
        uncertainty = np.empty(self.number)
        self.sensitivity_frame = pd.DataFrame(((3, self.number/3)))

        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        x=0
        while x < 3: # when x=0, calibrates the x sensors, when x=1, calibrates the y sensors and when x=2,
            # calibrates the z sensors
            for i in range((self.number/3)-1):
                self.data[self.data.columns[(3*i)+x+1]] = self.data[self.data.columns[(3*i)+x+1]] * self.vcc / self.bits
                self.data[self.data.columns[(3*i)+x+1]] -= self.nulls[(3*i)+x]
                sensitivities[i] = (((self.data[self.data.columns[(3*i)+x+1]]).mean())/field[x])*1000

                average_count = self.data2[self.data2.columns[(3*i)+x+1]].mean()
                count_uncertainty = ((np.sqrt(((sensor_uncertainty)**2)+(self.stds[(3*i)+x])**2))/average_count)**2
                average_voltage = (self.dat2[self.data2.columns[(3*i)+x+1]]*self.vcc / self.bits).mean()
                uncertainty_in_voltage = average_voltage*(np.sqrt(count_uncertainty+vcc_uncertainty))
                uncertainty_in_voltage_nulls = (np.sqrt(((uncertainty_in_voltage)**2)+((self.nulls_uncertainties[(3*i)+x])**2)))
                self.data2[self.data2.columns[(3*i)+1+x]] = self.data2[self.data2.columns[(3*i)+1+x]]-self.nulls[(3*i)+x]
                uncertainty_in_null_total = ((uncertainty_in_voltage_nulls)/(self.data2[self.data2.columns[(3*i)+x+1]].mean()))**2
                uncertainty_in_field_total = (field_uncertainty[x]/field[x])**2
                uncertainty[i] = (np.sqrt(uncertainty_in_null_total+uncertainty_in_field_total))*sensitivities[i]

            self.sensitivity_frame.iloc[2*x] = sensitivities
            self.sensitivity_frame.iloc[(2*x)+1] = uncertainty
            x+=1

            #then to extract this data, will need to know how many calibration fields are gonna be used
            # need to save these to csvs inside this loop

        self.save_sens()

    def save_sens(self) -> None:
        '''ds'''

        path = Path(__file__).parent
        output_x = path/'x_sens.csv'
        output_y = path/'y_sens.csv'
        output_z = path/'z_sens.csv'
        output_un_x = path/'x_sens_un'
        output_un_y = path/'y_sens_un'
        output_un_z = path/'z_sens_un'

        sens_x = self.sensitivity_frame.iloc[0]
        sens_y = self.sensitivity_frame.iloc[2]
        sens_z = self.sensitivity_frame.iloc[4]

        sens_un_x = self.sensitivity_frame.iloc[1]
        sens_un_y = self.sensitivity_frame.iloc[3]
        sens_un_z = self.sensitivity_frame.iloc[5]

        with open(output_x, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_x)
        with open(output_y, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_y)
        with open(output_z, 'a', encoding = 'utf-8', newline = '')as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_z)
        with open(output_un_x, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writer(sens_un_x)
        with open(output_un_y, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_un_y)
        with open(output_un_z, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_un_z)

        # so will have a separate csv file now for each sensitivity direction and
        # each uncertainty in sensitivity direction.
        # every time this code runs it will append to the csv
        # then when these are wanting to be used in the actual data conversion can 
        # take an average of each column in each csv

class Convert_3D:
    '''ds'''
    def __init__(self, port: str, filename: str, number: int, vcc: float, vcc_un: float, bits: int, samples: int = 200):
        self.port = port
        self.filename = filename
        self.number = number
        self.vcc = vcc
        self.vcc_un = vcc_un
        self.bits = (2**bits)-1
        self.samples = samples

    
        self.data = None  
        self.sensitvities = None
        self.uncertainty_sensitivity = None
        self.nulls = None
        self.nulls_uncertainty = None
        self.stds = None

        self.get_params()      

    def get_params(self) -> None:
        '''
        ds
        '''

        sensitivity_x_path = Path(__file__).resolve().with_name('x_sens.csv')
        sensitivity_y_path = Path(__file__).resolve().with_name('y_sens.csv')
        sensitivity_z_path = Path(__file__).resolve().with_name('z_sens.csv')

        sensitivity_uncertainty_x_path = Path(__file__).resolve().with_name('x_sens_un')
        sensitivity_uncertainty_y_path = Path(__file__).resolve().with_name('y_sens_un')
        sensitivity_uncertainty_z_path = Path(__file__).resolve().with_name('z_sens_un')

        sensitivity_x_frame = pd.read_csv(sensitivity_x_path)
        sensitivity_y_frame = pd.read_csv(sensitivity_y_path)
        sensitivity_z_frame = pd.read_csv(sensitivity_z_path)

        sensitivity_un_x_frame = pd.read_csv(sensitivity_uncertainty_x_path)
        sensitivity_un_y_frame = pd.read_csv(sensitivity_uncertainty_y_path)
        sensitivity_un_z_frame = pd.read_csv(sensitivity_uncertainty_z_path)

        sens_x = np.empty(self.number/3)
        sens_y = np.empty(self.number/3)
        sens_z = np.empty(self.number/3)

        sens_un_x = np.empty(self.number/3)
        sens_un_y = np.empty(self.number/3)
        sens_un_z = np.empty(self.number/3)

        for i in range((self.number/3) - 1):
            sens_x[i] = sensitivity_x_frame[sensitivity_x_frame.columns[i]].mean()
            sens_y[i] = sensitivity_y_frame[sensitivity_y_frame.columns[i]].mean()
            sens_z[i] = sensitivity_z_frame[sensitivity_z_frame.columns[i]].mean()
            sens_un_x[i] = sensitivity_un_x_frame[sensitivity_un_x_frame.columns[i]].mean()
            sens_un_y[i] = sensitivity_un_y_frame[sensitivity_un_y_frame.columns[i]].mean()
            sens_un_z[i] = sensitivity_un_z_frame[sensitivity_un_z_frame.columns[i]].mean()

        sensitivity = np.empty(self.number)
        uncertainty_sensitivity = np.empty(self.number)

        for i in range(self.number):
            if i%3 == 0: # x sensor
                sensitivity[i] = sens_x[i/3]
                uncertainty_sensitivity[i] = sens_un_x[i/3]
            elif i%3 == 1: # y sensor
                sensitivity[i] = sens_y[(i-1)/3]
                uncertainty_sensitivity[i] = sens_un_y[(i-1)/3]
            elif i%3 == 2: # z sensor
                sensitivity[i] = sens_z[(i-2)/3]
                uncertainty_sensitivity[i] = sens_un_z[(i-2)/3]

        self.sensitvities = sensitivity
        self.uncertainty_sensitivity = uncertainty_sensitivity
            
        self.nulls = np.empty(self.number)
        self.nulls_uncertainty = np.empty(self.number)
        self.stds = np.empty(self.number)

        nulls_path = Path(__file__).resolve().with_name('nulls.csv')
        stds_path = Path(__file__).resolve().with_name('stds.csv')
        nulls_and_uncertainties = pd.read_csv(nulls_path)
        self.nulls = nulls_and_uncertainties.iloc[0].to_numpy()
        self.nulls_uncertainty= nulls_and_uncertainties.iloc[1].to_numpy()
        stds_df = pd.read_csv(stds_path)
        self.stds = stds_df.iloc[0].to_numpy()

        # okay now i think i have all of them! hopefully all still in the same order...

        self.data = read_data(self.port, self.filename, self.samples)

    

        

               





