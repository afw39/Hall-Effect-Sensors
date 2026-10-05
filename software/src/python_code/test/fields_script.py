from conversion import Conversion

x = Conversion(port = '/dev/ttyUSB0', filename = 'data.csv', number = 8,
               vcc = 5, vcc_un = 0.05, bits = 10, samples = 200)
