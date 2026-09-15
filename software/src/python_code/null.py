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
SAMPLES = 200
READINGS = 3

# to find null voltage of sensors - will return array of null voltages for each sensor
for i in range(READINGS):
    null_voltages = np.empty(NUMBER)
    null_voltages = find_null_voltage(FIELD, NUMBER, PORT, VCC, 'null-voltage-data.csv', SAMPLES)


print(null_voltages)


# OKAYYYYY this is working whoop whoop, going to now try and get the values of null voltage to be 
# the average of three different readings? going to chuck it in a loop

# okay so plan is, stop and start recording 3 times and therefore get 3 values of the null voltage
# per sensor 

# so If i can save each list of hall effect sensors in the ith row of a dataframe, and print out
# that data frame that would be ideal.