import json
from pathlib import Path
import pandas as pd
# so will have a json file coming in

path_json = Path(__file__).parent
output_json = path_json/'json.json'

with open(output_json, encoding='utf-8') as f:
    sensor_data = json.load(f)

# so now json is loaded in under sensor_data as a python object
# dunno what a python object is but my json is one now

# so need to link the column index to the sensor number in the json
# then can use that to link the direction to the column number
# and separate them that way - THATS THE PLAN!

# okay so we know what we are doing - but idk how to do that

# we need a data frame first, lets just use an example csv?
data_path = Path(__file__).resolve().with_name('example.csv')
data = pd.read_csv(data_path)
number_of_sensors = 12

for sensor in sensor_data['sensors']:
    # need to somehow link the sensor number to the column
    # or like maybe in the json need to put the number not as a str
    # so can use like a for loop or something
    for i in range(number_of_sensors):
        data[data.column[i]] = number[i]
        # but not like this, but i need to link them somehow
        # if its the ith column and the number is i:
            if sensor_data["direction"] == "x":
                # append this column to the x data frame?

