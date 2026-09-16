from calibration import Calibration

x = Calibration(field = 0, number =4, port = '/dev/ttyACM0', vcc = 3.3, 
                filename = 'calibration-data.csv',samples = 50, delay = 1)
x.find_null_voltage()
x.perform_calibration(fields = [2, 6], filename = 'calib-data.csv')
x.make_callable_csv()
