from calibration import Calibrate
from read import read_data
from null_voltage import find_null_voltage, sensor_sensitivities

NUMBER = 4
FIELDS = ([0, 6, 8])
VCC = 5
PORT = 'COM3'

# to find null voltage of sensors - will return array of null voltages for each sensor
if FIELDS[0] == 0:
    null_voltages = find_null_voltage(FIELDS[0], NUMBER, PORT, VCC, 'null-voltage-data.csv')

# calibration one
calibration_one_df = read_data(PORT, 'calibration-data-1.csv')
x = Calibrate(calibration_one_df, NUMBER, FIELDS[1], VCC)
sensitivity_data_1 = x.calibrate()

# calibration two
calibration_two_df = read_data(PORT, 'calibration-data-2.csv')
y = Calibrate(calibration_two_df, NUMBER, FIELDS[2], VCC)
sensitivity_data_2 = y.calibrate()

# to get the array of averaged sensitivities
sensitivities = sensor_sensitivities(NUMBER, sensitivity_data_1, sensitivity_data_2)
