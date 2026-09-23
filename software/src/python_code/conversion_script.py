from conversion import Conversion

y = Conversion(port = '/dev/ttyUSB0', filename = 'data.csv', number = 8, vcc = 5.0, samples = 16)

print(y.data)
