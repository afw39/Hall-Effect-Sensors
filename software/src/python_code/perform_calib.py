import time
import numpy as np
import pandas as pd
from read import read_data
from calibrate import Calibrate

def find_null_voltage(field: float, number: int, port: str, vcc: float,
                      filename: str, samples: int = 200, rows: int = 3) -> pd.DataFrame:
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
    null_frame = pd.DataFrame(np.zeros((rows, number)), dtype = float)
    average_null = pd.DataFrame(np.zeros((1, number)), dtype = float)

    for i in range(rows):
        calibration_df = read_data(port,filename, samples)
        x = Calibrate(calibration_df, number, field, vcc)
        null_values = x.null_voltages()
        null_frame.iloc[i] = null_values
        time.sleep(10)

    null_voltages_averaged = np.empty(number)
    for i in range(number):
        null_voltages_averaged[i] = null_frame[null_frame.columns[i]].mean()

    average_null.iloc[0] = null_voltages_averaged

    return average_null

def perform_calibration(nulls: np.array, delay: int, fields: np.array, port: str, 
                        filename: str, samples: int, number: int, vcc: float) -> pd.DataFrame:
    '''
    performs the calibration steps by calling on relevant methods and classes from other scripts
    Args:
        delay (int): time delay between sets of data recording (time for sensor array to be moved and set up in new stable field)
        fields (np.array): array containing the values of the fields in order that the hall sensors will be calibrated against
        port (str): the port of the computer that the Arduino is connected to
        filename (str): the name of the file that the calibration data will be saved to 
        samples (int): how many measurements are recorded for each field
        number (int): how many sensors are in the array 
        vcc (float): the VCC of the Arduino
    Returns:
        sensitivities_averaged (array): array of an averaged value for sensitivity, one for each sensor
    '''

    sensitivity_frame = pd.DataFrame(np.zeros((len(fields), number)), dtype = float)
    sensitivities_averaged_frame = pd.DataFrame(np.zeros((1, number)), dtype = float)

    print(f'you have {delay} seconds until the data starts to be recorded again')
    time.sleep(delay)
   
    how_many_fields = len(fields)
    sensitivities_averaged = np.empty(number)

    
    for i in range(how_many_fields):
        calibration_data = read_data(port, filename, samples)
        x = Calibrate(calibration_data, number, fields[i], vcc)
        sensitivity_data = x.calibrate(nulls)
        sensitivity_frame.iloc[i] = sensitivity_data
        print(f'the data will start recording again in {delay} seconds')
        time.sleep(delay)

    for i in range(number):
        sensitivities_averaged[i] = sensitivity_frame[sensitivity_frame.columns[i]].mean()

    sensitivities_averaged_frame.iloc[0] = sensitivities_averaged

    return sensitivities_averaged_frame
