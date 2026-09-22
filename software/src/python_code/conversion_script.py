from conversion import Conversion

y = Conversion(port = '/dev/ttyACM0', filename = 'data.csv', number = 8, vcc = 3.3, samples = 16)

print(y.data)
