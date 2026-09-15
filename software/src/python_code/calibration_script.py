from calibrate import Calibrate
from read import read_data
from null_voltage import find_null_voltage, sensor_sensitivities
import numpy as np

NUMBER = 4
FIELDS = ([0, 6, 8]) # put these in in mT
VCC = 5
PORT = 'COM3'
SAMPLES = 200

# to find null voltage of sensors - will return array of null voltages for each sensor
if FIELDS[0] == 0:
    null_voltages = np.empty(NUMBER)
    null_voltages = find_null_voltage(FIELDS[0], NUMBER, PORT, VCC, 'null-voltage-data.csv', SAMPLES)
print('press enter when the null_voltage has been calculated and the experiment has been moved into a field ')
input()

# calibration one
calibration_one_df = read_data(PORT, 'calibration-data-1.csv', SAMPLES)
x = Calibrate(calibration_one_df, NUMBER, FIELDS[1], VCC)
sensitivity_data_1 = x.calibrate()

# so this will contact the arduino - im hoping all the other functions that are within classes/functions of other scripts that have 
# been imported will still run even if those scripts haven't been called directly

# same for the finding the null voltage, that is going to run and read the data, i think we need like a delay
# maybe can set it up to have an input that says, press enter when you have it set up in the next field?

# for the second calibration, like this will try and read at the same time, am going to need to give this some kind of a delay so that
# i can set up the experiment in a different field

print('press enter when the first calibration field has been read and the setup is in the second field ')
input()

# calibration two
calibration_two_df = read_data(PORT, 'calibration-data-2.csv', SAMPLES)
y = Calibrate(calibration_two_df, NUMBER, FIELDS[2], VCC)
sensitivity_data_2 = y.calibrate()

# to get the array of averaged sensitivities
sensitivities = sensor_sensitivities(NUMBER, sensitivity_data_1, sensitivity_data_2)

# lowkey have no idea if this will work or not but i guess we are going to find out this week
