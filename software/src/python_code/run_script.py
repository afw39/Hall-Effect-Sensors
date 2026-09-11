# so here i am gonna import the classes for calibration and data conversion and then i can run them separately, idea is i 
# will run the calibration and  then the returns of that will be the null voltage and the sensitivity for each sensor
# then i will pass them through as parameters for the conversion. 
import pandas as pd
import numpy as np
from calibration import Calibrate
from calibration import calibration_read
from convert import Convert
from convert import read
from null_voltage import find_null_voltage

FIELD = 0
NUMBER = 4
PORT = 'COM3'

# to find null voltage of sensors - will return array of null voltages for each sensor

if FIELD == 0:
    null_voltages = find_null_voltage(FIELD, NUMBER, PORT)

















# this needs to be done just once - initialises the dataframe
# maybe need to have an if statement like if this already exists don't run again or something like that
columns = ['field'] + [f'sensor_{i+1}_sensitivity' for i in range(NUMBER)]
row = [FIELD] + sensitivities
# add that row and columns to dataframe
sensitivity_data = pd.DataFrame(columns = columns)
sensitivity_data.loc[len(sensitivity_data)] = row


# when running again - need to load the exisiting data
sensitivity_data = pd.read_csv("sensitivity_results.csv")
row = [FIELD] + sensitivities 
sensitivity_data.loc[len(sensitivity_data)] = row
sensitivity_data.to_csv('sensitivity_results.csv', index = False)


# i think i need to have maybe two scripts that I run, like 1 for finding the null voltage and for making the dataframe and one 
# for the adding of rows to the dataframe