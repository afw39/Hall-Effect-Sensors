''' 
lhfyluyf
'''



from read import read_data
from calibrate import Calibrate
import numpy as np
import pandas as pd
import time

def find_null_voltage(field: float, number: int, port: str, vcc: float, filename: str, samples: int = 200, cols: int = 4, rows: int = 3) -> np.array:
    '''
    calculates the systematic error/null voltage of each sensor in the array by applying the method `null_voltages` from the `Calibrate` class
    Args:
        field (float): value of magnetic field sensors are in (always 0)
        number (int): number of sensors
        port (str): computer port that the arduino is connected to
        vcc (float): VCC value of arduino
        filename (str): file name that the calibration data is stored under
    Returns:
        null_values (np.array): array of values of null voltages, same shape as number of sensors
    '''

    null_frame = pd.DataFrame(np.zeros((rows, cols)), columns = ["sensor1", "sensor2", "sensor3", "sensor4"], dtype = float)

    for i in range(rows):
        calibration_df = read_data(port,filename, samples)
        x = Calibrate(calibration_df, number, field, vcc)
        null_values = x.null_voltages()
        null_frame.iloc[i] = null_values
        time.sleep(10)

    null_voltages_averaged = np.empty(number)
    for i in range(number):
        null_voltages_averaged[i] = null_frame[null_frame.columns[i]].mean()

    return null_voltages_averaged

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
    sensor_sensitivity = [0] * number
    for i in range(number):
        sensor_sensitivity[i] = (sen_data_1[i] + sen_data_2) / 2
    return sensor_sensitivity
