import time
from pathlib import Path
import pandas as pd
import numpy as np
from read import read_data
from uncertainty import StandardDeviation

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
        vcc_un (float): uncertainty in the measurement of the VCC
        samples (int): how many data samples each reading takes
        delay (int): the time between calibration recordings 

    Methods:
        find_null_voltage() -> pd.DataFrame:
            computes and stores null voltages for each sensor in the array
        get_stds() -> None:
            runs the StandardDeviation class and gets those values to use
            in the sensor uncertainties
        uncertainty_in_null() -> list:
            calculates the uncertainty in the values for the null voltage
            for each sensor
        perform_calibration() -> pd.DataFrame:
            computes and stores the average value for sensitivity for each sensor.
            calculates the uncertainty in sensitivity for each sensor in each field
        make_callable_csv() -> None:
            saves the average value of sensitivity, null voltage, and the 
            uncertainties in both to a csv to be read from in conversion.py
    '''

    def __init__(self, number: int, port: str, vcc: float,
                      filename: str, vcc_un: float, samples: int = 200, delay: int = 100):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.samples = samples
        self.delay = delay
        self.vcc_un = vcc_un
        self.average_null = None
        self.null_values = None
        self.calibration_df = None
        self.null_voltages_averaged = None
        self.sensitivities = None
        self.sensitivities_averaged_frame = None
        self.calibration_data = None
        self.uncertainty_sen_frame = None
        self.uncertainty_in_nulls = None
        self.averaged_sen_uncertainties = None
        self.null_uncertainty_df = None
        self.stds = None

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
                null[x] = (self.calibration_df[self.calibration_df.columns[x+1]] * self.vcc / 1023).mean()
                self.null_values[x] = (null[x])

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
        runs the `StandardDeviation` class from the uncertainty.py script and saves the value
        for the standard deviation for each sensor, this is later used when calculating
        the total uncertainty in the sensor readings
        Args:
            None
        Returns:
            None 
        '''
        x = StandardDeviation(number = self.number, port = self.port, filename = 'standard-deviation.csv', samples = 1000)
        stds = x.calc_standard_deviation()
        self.stds = stds

        stds_df = pd.DataFrame(self.stds)

        script_dir_std = Path(__file__).parent
        output_file_std = script_dir_std/'std.csv'
        stds_df.to_csv(output_file_std, index = False)

        self.uncertainty_in_null()

    
    def uncertainty_in_null(self) -> list:
        '''
        calculates the uncertainty in the null voltage measurement and saves that as
        a row in a dataframe
        Args:
            None
        Returns:
            None
        '''

        average_sensor_data = [0] * self.number
        self.uncertainty_in_nulls = [0] * self.number
        self.null_uncertainty_df = pd.DataFrame(np.zeros((1, self.number)), dtype = float)
        uncertainty_in_sensor = 0.5
        second = (self.vcc_un/self.vcc)**2

        for i in range(self.number):
            average_sensor_data[i] = self.calibration_df[self.calibration_df.columns[i+1]].mean()
            first = ((np.sqrt((uncertainty_in_sensor)**2 + (self.stds[i])**2))/average_sensor_data[i])**2
            squared = first + second
            rooted = np.sqrt(squared)
            self.uncertainty_in_nulls[i] = rooted * self.null_voltages_averaged[i]

        self.null_uncertainty_df.iloc[0] = self.uncertainty_in_nulls


    def perform_calibration(self, fields: np.array, fields_uncertainty: float) -> None:
        '''
        uses the null voltages calculated previously and calculates the average
        sensitivity of each sensor using known values of the calibration field strengths
        sensitivities are calculated in units of mV/T. This method also calculates the 
        uncertainty in each sensitivity calculation for each sensor and saves them 
        Args:
            fields (np.array): array containing the values of each calibration field strength 
        Returns:
            None 
        '''
        sensitivity_frame = pd.DataFrame(np.zeros((len(fields), self.number)), dtype = float)
        self.sensitivities_averaged_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)
        uncertainty_in_sen_frame = pd.DataFrame(np.zeros((len(fields), self.number)), dtype = float)
        self.averaged_sen_uncertainties = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        print(f'you have {self.delay} seconds until the data starts to be recorded again')
        time.sleep(self.delay)
   
        how_many_fields = len(fields)
        sensitivities_averaged = np.empty(self.number)
        uncertainty_in_sensor = 0.5
        uncertainties_sensitivity_averaged = [0] * self.number
    
        for i in range(how_many_fields):
            self.calibration_data = read_data(self.port, self.filename, self.samples)
            self.uncertainty_sen_frame = self.calibration_data

            average_sen_data = [0] * self.number
            self.sensitivities = [0] * self.number
            uncertainty_in_volt = [0] * self.number
            uncertainty_in_volt_nulls = [0] * self.number
            uncertainty_in_sens = [0] * self.number
    
            second = (self.vcc_un/self.vcc) ** 2

            for x in range(self.number):
                average_sen_data[x] = self.uncertainty_sen_frame[self.uncertainty_sen_frame.columns[x+1]].mean()
                first = ((np.sqrt((uncertainty_in_sensor)**2 + (self.stds[i])**2))/average_sen_data[x])**2
                rooted = np.sqrt(first + second)

                average_voltage_value = (self.calibration_data[self.calibration_data.columns[x+1]] * self.vcc / 1023).mean()

                uncertainty_in_volt[x] = rooted * average_voltage_value
                uncertainty_in_volt_nulls[x] = (np.sqrt(((uncertainty_in_volt[x])**2)+ ((self.uncertainty_in_nulls[x])**2)))

                self.calibration_data[self.calibration_data.columns[x+1]] = self.calibration_data[self.calibration_data.columns[x+1]] * self.vcc / 1023
                self.calibration_data[self.calibration_data.columns[x+1]] -= self.null_voltages_averaged[x]

                third = ((uncertainty_in_volt_nulls[x])/(self.calibration_data[self.calibration_data.columns[x+1]].mean()))**2
                fourth = ((fields_uncertainty)/fields[i])**2
                rooted2 = np.sqrt(third+fourth)

                self.sensitivities[x] = ((self.calibration_data[self.calibration_data.columns[x+1]].mean()) / fields[i]) * 1000000
                uncertainty_in_sens[x] = rooted2 * self.sensitivities[x]

            sensitivity_frame.iloc[i] = self.sensitivities
            
            uncertainty_in_sen_frame.iloc[i] = uncertainty_in_sens

            if i+1 == how_many_fields:
                print('data recording complete...')
                
            else:
                print(f'the data will start recording again in {self.delay} seconds...')
            time.sleep(self.delay)

        for i in range(self.number):
            sensitivities_averaged[i] = sensitivity_frame[sensitivity_frame.columns[i]].mean()

        for i in range(self.number):
            uncertainties_sensitivity_averaged[i] = uncertainty_in_sen_frame[uncertainty_in_sen_frame.columns[i]].mean()

        self.sensitivities_averaged_frame.iloc[0] = sensitivities_averaged
        self.averaged_sen_uncertainties.iloc[0] = uncertainties_sensitivity_averaged

        self.make_callable_csv()


    def make_callable_csv(self) -> None:
        '''
        combines the two data frames containing null voltages and sensitivities for 
        each sensor and the two dataframes containing the uncertainties for the
        null voltage and sensitivities into one to convert that to a csv. 
        This is done so that the values can be accessed during the actual data 
        recording by reading from the csv
        Args:
            None
        Returns:
            None
        '''
        combined_df = pd.concat([self.average_null, self.sensitivities_averaged_frame, self.null_uncertainty_df, self.averaged_sen_uncertainties])
        print(combined_df)
        script_dir = Path(__file__).parent
        output_file = script_dir/'combined-data.csv'
        combined_df.to_csv(output_file, index = False)
