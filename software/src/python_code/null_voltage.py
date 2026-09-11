from read import read_data
from calibration import Calibrate
import numpy as np

def find_null_voltage(field: float, number: int, port: str, vcc: float, filename: str) -> np.array:
    '''
    docstring
    '''
    calibration_df = read_data(port,filename)
    x = Calibrate(calibration_df, number, field, vcc)
    null_values = x.null_voltages()
    return null_values

def sensor_sensitivities(number: int, sen_data_1: np.array, sen_data_2: np.array) -> np.array:
    '''
    docstring
    '''
    sensor_sensitivity = np.empty(number)
    for i in range(number):
        sensor_sensitivity[i] = (sen_data_1[i] + sen_data_2) / 2
    return sensor_sensitivity
