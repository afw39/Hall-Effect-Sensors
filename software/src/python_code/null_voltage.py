from read import read_data
from calibration import Calibrate
import numpy as np

def find_null_voltage(field: float, number: int, port: str, vcc: float, filename: str) -> np.array:
    '''
    calculates the systematic error/null voltage of each sensor in the array
    Args:
        field (float): value of magnetic field sensors are in (always 0)
        number (int): number of sensors
        port (str): computer port that the arduino is connected to
        vcc (float): VCC value of arduino
        filename (str): file name that the calibration data is stored under
    Returns:
        null_values (np.array): array of values of null voltages, same shape as number of sensors
    '''
    calibration_df = read_data(port,filename)
    x = Calibrate(calibration_df, number, field, vcc)
    null_values = x.null_voltages()
    return null_values

def sensor_sensitivities(number: int, sen_data_1: np.array, sen_data_2: np.array) -> np.array:
    '''
    calculates the sensitivities of any number of sensors in a known field
    Args:
        number (int): number of sensors used
        sen_data_1 (np.array): array of sensitivities for each sensor from first calibration field used
        sen_data_2 (np.array): array of sensitivities for each sensor from second calibration field used
    Returns:
        sensor_sensitivity (np.array): average of both sensitivities in both fields for each sensor
    '''
    sensor_sensitivity = np.empty(number)
    for i in range(number):
        sensor_sensitivity[i] = (sen_data_1[i] + sen_data_2) / 2
    return sensor_sensitivity
