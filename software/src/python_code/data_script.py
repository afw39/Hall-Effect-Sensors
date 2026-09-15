from read import read_data
from convert import Convert
from python_code.calibration_script import sensitivities, null_voltages

PORT = 'COM3'
NUMBER = 4
VCC = 5

# to read it, save dataframe as reading of the csv
data =  read_data(PORT, 'arduino-data.csv')

# convert the data
x = Convert(data, NUMBER, null_voltages, VCC, sensitivities)
data = x.adc_to_volts()
data = x.field_strength()
print(data)
