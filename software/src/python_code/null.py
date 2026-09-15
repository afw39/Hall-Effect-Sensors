# just using this script for the next couple weeks to find null voltage
# no calibration can be done for a couple weeks

# from calibrate import Calibrate
#from read import read_data
from null_voltage import find_null_voltage #, sensor_sensitivities
import numpy as np

NUMBER = 4
FIELD = 0 # put these in in mT
VCC = 3.3
PORT = '/dev/ttyACM0'

# to find null voltage of sensors - will return array of null voltages for each sensor
null_voltages = np.empty()
null_voltages = find_null_voltage(FIELD, NUMBER, PORT, VCC, 'null-voltage-data.csv')

print(null_voltages)