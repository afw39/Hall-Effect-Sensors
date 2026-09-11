from calibration import calibration_read
from calibration import Calibrate
import numpy as np

def find_null_voltage(field: float, number: int, port) -> np.array:
    '''
    docstring
    '''
    calibration_df = calibration_read(port)
    x = Calibrate(calibration_df, number, field)
    null_values = x.null_voltages()
    return null_values
