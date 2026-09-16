from perform_calib import find_null_voltage, perform_calibration

null_voltages = find_null_voltage(field = 0, number = 4, port = '/dev/ttyACM0', vcc = 3.3, 
                                  filename = 'null-voltage-data.csv', samples = 100, rows = 3)
print(null_voltages)

# other issue i have is that I am going to need the values for sensitivity and null_voltages 
# saved somewhere permenantly so that they can be accessed
# maybe if i save them as a dataframe, then I can convert them into two csvs in the python_code folder 
# (using the Path library) and then I can like use that
# in other scripts, I'll just call on them, CHILL CHILL CHILL, well i'll call on them and then convert 
# them back into dataframes probs

sensor_sensitivities = perform_calibration(nulls = null_voltages, delay = 1, fields = [3.4, 5.6, 8], 
                                           port = '/dev/ttyACM0', filename = 'calibration-data.csv', samples = 100, number = 4, vcc = 3.3)

print(sensor_sensitivities)

# for actual data reading, maybe i should append to the csv each time so i can see all the data - not sure if I acc want it or not

# maybe this is when you are actually meant to use classes? 
# do these functions need returns?? maybe to get the csv but also maybe not