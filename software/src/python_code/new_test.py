from null_voltage import find_null_voltage

null_voltages = find_null_voltage(field = 0, number = 4, port = '/dev/ttyACM0', vcc = 3.3, 
                                  filename = 'null-voltage-data.csv', samples = 100, rows = 3, cols = 4 )
print(null_voltages)

# these values are averaged over 3 rounds of 200 samples
# with a 10 second gap in between each one


# next step is to do this for calibration. If using the big helmholtz coils, can literally
# just change the current through the coils to change the field strength
# if i know what they are going to be beforehand i can store them in an array like before
# and then just use input() or time.sleep(however long it will take to change the field)
# to make it work in one runthrough (might be able to then loop it for however many fields afterall!)