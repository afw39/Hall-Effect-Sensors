from calibration import Calibration

x = Calibration(number = 2, port = '/dev/ttyACM0', vcc = 3.3,
                filename = 'calibration-data.csv',samples = 50, delay = 1)
x.perform_calibration(fields = [2, 6])
