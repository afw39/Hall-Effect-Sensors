import time
from pathlib import Path
from csv import writer
import pandas as pd
import numpy as np
from read import read_data
from uncertainty import StandardDeviation


class Calibration:
    '''
    making one thing so that can run each time for a field with a new input
    field value and save calibration parameters in file/dataframe that keeps getting added to
    '''

    def __init__(self, number: int, port: str, vcc: float,
                      filename: str, vcc_un: float, bits: int, samples: int = 200, delay: int = 100):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.samples = samples
        self.delay = delay
        self.vcc_un = vcc_un
        self.bits = bits
        self.num = 2**(self.bits) - 1
        self.average_null = None
        self.null_values = None
        self.calibration_df = None
        self.null_voltages_averaged = None
        self.calibration_data = None
        self.uncertainty_sen_frame = None
        self.sensitivities = None
        self.uncertainty_in_nulls = None
        self.stds = None
        self.averaged_sen_uncertainties = None
        self.sensitivities_averaged_frame = None
        self.uncertainty_in_sens = None

        self.find_null_voltage()
    

    def check_current(self):
        '''
        can check the field that should be produced against the value of the field inputted
        can output a warning message if they are super different to see what is up with that
        and if the coils are working properly. for the actual calibration should go off of the
        actual field produced rather than the expected field as they wion't be exactly the same
        '''

    def find_null_voltage(self) -> None:
        '''
        same as before I think
        '''
        null_frame = pd.DataFrame(np.zeros((3, self.number)), dtype = float)
        self.average_null = pd.DataFrame(np.zeros((2, self.number)), dtype = float)

        for i in range(3):
            self.calibration_df = read_data(self.port,self.filename, self.samples)
            self.null_values = [0] * self.number
            for x in range(self.number):
                self.null_values[x] = (self.calibration_df[self.calibration_df.columns[x+1]] * self.vcc / self.num).mean()

            null_frame.iloc[i] = self.null_values
            if i+1 < 3:
                time.sleep(10)

        self.null_voltages_averaged = np.empty(self.number)
        for i in range(self.number):
            self.null_voltages_averaged[i] = null_frame[null_frame.columns[i]].mean()

        self.average_null.iloc[0] = self.null_voltages_averaged
        self.get_stds()

    def get_stds(self) -> None:
        '''
        same as before
        '''
        x = StandardDeviation(number = self.number, port = self.port, filename = 'standard-deviation.csv', samples = 1000)
        self.stds = x.calc_standard_deviation()

        stds_df = pd.DataFrame(self.stds)

        script_dir_std = Path(__file__).parent
        output_file_std = script_dir_std/'std.csv'
        stds_df.to_csv(output_file_std, index = False)

        self.uncertainty_in_null()

    def uncertainty_in_null(self) -> list:
        '''
        same as before as well
        '''
        average_sensor_data = [0] * self.number
        self.uncertainty_in_nulls = [0] * self.number
        uncertainty_in_sensor = 0.5
        second = (self.vcc_un/self.vcc)**2

        for i in range(self.number):
            average_sensor_data[i] = self.calibration_df[self.calibration_df.columns[i+1]].mean()
            first = ((np.sqrt((uncertainty_in_sensor)**2 + (self.stds[i])**2))/average_sensor_data[i])**2
            squared = first + second
            rooted = np.sqrt(squared)
            self.uncertainty_in_nulls[i] = rooted * self.null_voltages_averaged[i]

        self.average_null.iloc[1] = self.uncertainty_in_nulls
        null_output_file = (Path(__file__).parent)/'nulls.csv'
        self.average_null.to_csv(null_output_file, index = False)


    def perform_calibration(self, calibration_field: float, uncertainty_in_field: float) -> None:
        '''
        this will be different
        going to take the return of this and save that as a variable in the running script
        then will pass those variables into a function to hopefully put them in a csv
        '''

        self.sensitivities_averaged_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)
        self.averaged_sen_uncertainties = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        uncertainty_in_sensor = 0.5

        self.calibration_data = read_data(self.port, self.filename, self.samples)
        self.uncertainty_sen_frame = self.calibration_data

        average_sen_data = [0] * self.number
        self.sensitivities = [0] * self.number
        uncertainty_in_volt = [0] * self.number
        uncertainty_in_volt_nulls = [0] * self.number
        self.uncertainty_in_sens = [0] * self.number

        second = (self.vcc_un/self.vcc) ** 2
        for x in range(self.number):

            average_sen_data[x] = self.uncertainty_sen_frame[self.uncertainty_sen_frame.columns[x+1]].mean()
            first = ((np.sqrt((uncertainty_in_sensor)**2 + (self.stds[x])**2))/average_sen_data[x])**2
            rooted = np.sqrt(first + second)

            average_voltage_value = (self.calibration_data[self.calibration_data.columns[x+1]] * self.vcc / self.num).mean()

            uncertainty_in_volt[x] = rooted * average_voltage_value
            uncertainty_in_volt_nulls[x] = (np.sqrt(((uncertainty_in_volt[x])**2)+ ((self.uncertainty_in_nulls[x])**2)))

            self.calibration_data[self.calibration_data.columns[x+1]] = self.calibration_data[self.calibration_data.columns[x+1]] * self.vcc / self.num
            self.calibration_data[self.calibration_data.columns[x+1]] -= self.null_voltages_averaged[x]

            third = ((uncertainty_in_volt_nulls[x])/(self.calibration_data[self.calibration_data.columns[x+1]].mean()))**2
            fourth = ((uncertainty_in_field)/calibration_field)**2
            rooted2 = np.sqrt(third+fourth)

            self.sensitivities[x] = ((self.calibration_data[self.calibration_data.columns[x+1]].mean()) / calibration_field) * 1000
            self.uncertainty_in_sens[x] = rooted2 * self.sensitivities[x]

        self.make_callable_csv()


    def make_callable_csv(self) -> None:
        '''
        docstring
        '''
        path = Path(__file__).parent
        output1 = path/'uncertainties.csv'
        output2 = path/'sens.csv'

        with open(output1, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.uncertainty_in_sens)

        with open(output2, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.sensitivities)
