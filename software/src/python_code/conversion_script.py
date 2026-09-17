from conversion import Conversion

y = Conversion(port = '/dev/ttyACM0', filename = 'data.csv', number = 4, vcc = 3.3, samples = 16)

print(y.data)

# y.data is a dataframe containing a running timestamp and field strengths for each sensor 
# (need to work out units of everything being calculated asap)


