from calibration import Calibration

x = Calibration(number = 8, port = '/dev/ttyUSB0', vcc = 5.0,
                filename = 'calibration-data.csv', vcc_un = 0.05, samples = 50, delay = 1)
x.perform_calibration(fields = [0.2, 0.6], fields_uncertainty = 0.005) # input fields in mT
