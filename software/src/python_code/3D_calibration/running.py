from sensors import Nulls, Calib, Convert

x = Nulls(6, '/dev/ttyUSB0', 5.0, 0.05, 'calibrate.csv', 10, samples = 10)

y = Calib(6, '/dev/ttyUSB0', 5, 0.05, 'sensitivity_data.csv', 10, samples = 10)

z = Convert('/dev/ttyUSB0', 'conversion.csv', 6, 5, 0.05, 10)
