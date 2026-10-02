from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from read import read_data

class Sensitivity:
    '''
    docstring
    '''

    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str,
                bits: int, samples: int, calibration_field: float, field_uncertainty: float):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = (2**bits)-1
        self.samples = samples
        self.field = calibration_field
        self.field_uncertainty = field_uncertainty

        self.calibration_data = None
        self.nulls = None
        self.nulls_uncertainties = None
        self.stds = None
        self.sens_frame = None
        self.sens_uncertainties_frame = None
        self.sensitivities = None
        self.uncertainty_in_sens = None

        self.get_parameters()

    def get_parameters(self) -> None:
        '''
        ds
        '''

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

        self.current_comparison()

    def current_comparison(self) -> None:
        '''
        docstring
        '''

        self.perform_calibration()

    def perform_calibration(self) -> None:
        '''
        do the calibration and get the sensitivities and the uncertainties in sens
        '''
        
        uncertainty_in_sensor = 0.5
        
        self.calibration_data = read_data(self.port, self.filename, self.samples)
        uncertainty_sen_frame = self.calibration_data
        
        self.sensitivities = [0] * self.number
        self.uncertainty_in_sens = [0] * self.number
        
        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        for x in range(self.number):
        
            average_sen_data = uncertainty_sen_frame[uncertainty_sen_frame.columns[x+1]].mean()
            reading_uncertainty = ((np.sqrt(((uncertainty_in_sensor)**2)+(self.stds[x])**2))/average_sen_data[x])**2
            rooted = np.sqrt(reading_uncertainty+vcc_uncertainty)
        
            average_voltage_value = (self.calibration_data[self.calibration_data.columns[x+1]]*self.vcc/self.bits).mean()
        
            uncertainty_in_volt = rooted*average_voltage_value
            uncertainty_in_volt_nulls = (np.sqrt(((uncertainty_in_volt)**2)+((self.nulls_uncertainties[x])**2)))
        
            self.calibration_data[self.calibration_data.columns[x+1]] = self.calibration_data[self.calibration_data.columns[x+1]]*self.vcc / self.bits
            self.calibration_data[self.calibration_data.columns[x+1]] -= self.nulls[x]
        
            third = ((uncertainty_in_volt_nulls)/(self.calibration_data[self.calibration_data.columns[x+1]].mean()))**2
            fourth = ((self.field_uncertainty)/self.field)**2
            rooted2 = np.sqrt(third+fourth)
        
            self.sensitivities[x] = ((self.calibration_data[self.calibration_data.columns[x+1]].mean())/self.field)*1000
            self.uncertainty_in_sens[x] = rooted2*self.sensitivities[x]

        self.saves_sens()

    def saves_sens(self) -> None:
        '''
        docstring
        '''
        path = Path(__file__).parent
        output1 = path/'sens.csv'
        output2 = path/'uncertainties.csv'

        with open(output1, 'a', encoding ='utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.sensitivities)

        with open(output2, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(self.uncertainty_in_sens)
