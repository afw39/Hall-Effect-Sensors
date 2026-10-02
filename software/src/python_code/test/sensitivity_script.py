from sens import Sensitivity

x = Sensitivity(number = 8, port = '/dev/ttyUSB0', vcc = 5, vcc_un = 0.05, 
                filename = 'calibration.csv', bits = 16, samples = 400, calibration_field = 50, field_uncertainty = 0.005)
