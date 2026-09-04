# okay so in this python file
# - need to take the data from the arduino - thats step 1
# - want to save that data into a csv file
# - need to calculate magnetic susceptibility (this will be done by knowing value of actual field and comparing it to average values of volatges outputted and scaling up)
# - will then convert those voltages to magnetic field strengths


# okay so first imports
from serial.tools import list_ports
import serial
import pandas as pd
import numpy as np

#to find out what port the arduino is connected to
ports = list_ports.comports()
for port in ports:
    print(port)

arduino_port = "COM3" #replace with whatever the name of the port is
baud_rate = 9600 
fileName = "analogue-data.csv" # name of csv file generated - can be changed
samples = 100 #how many data measurements you want to take
print_labels = False


ser = serial.Serial(arduino_port, baud_rate)
print('Connected to Arduino port' + arduino_port)
file = open(fileName, "w") # can use "a" for append (will reprint headings), research what is best 
print("Created file")

line = 0

while line <= samples:
    if print_labels:
        if line == 0:
            print("Printing Column Headers")
        else:
            print("Line " + str((line) + ": writing..."))

    getData = str(ser.readline())
    data = getData[0:][:-2]
    print(data)

    file = open(fileName, "a")

    file.write(data + "\n")
    line = line+1

print("data collection complete! ")
file.close()

# it is possible that with this we wont need the arduino code as well? honestly not completely sure but maybe thats a question for monday?

#now we want to convert this data which is currently stored in "analog-data.csv"

#so we are going to have a bunch of voltages in this csv, can read this and just make a dataframe. Im also going to need like real time measurements of the magnetic fields 
# from another device as well

dataframe = pd.read_csv("analog-data.csv")
df = dataframe

#so for like each sensor i will know what the value is meant to be, so do i take the average of each sensor

def calibration(number: int, df: np.ndarray):
    # this to be used when in the helmholtz coils to calibrate the sensors
    number_of_sensors = number

    field_strength = 0.5*10**-3 # (actual field strength in T)

    for i in range(number_of_sensors):
        sensor_average = np.array()  #make an array of the size of the number of sensors i think
        #then want to calculate the average for each using the i index
        #hopefully you can remeber what i want this to do on monday
        # do the same for the calculation of magnetic susceptibility - all in the for loop
        # and then same for the creation of the new columns
        # might be better to have a different dataframe for voltage and one for magnetic field strength
    sensor1_average = df['voltage S1'].mean() #this will be a number in V
    sensor2_average = df['voltage S2'].mean()
    sensor3_average = df['voltage S3'].mean()

    #okay now need to compare all these values to the actual recorded one

    magnetic_susceptibility1 = (sensor1_average)/(field_strength)
    magnetic_susceptibility2 = (sensor2_average)/(field_strength)
    magnetic_susceptibility3 = (sensor3_average)/(field_strength)

    # so i have three different magnetic susceptibilities for each sensor (might want to make that a for loop if gonna have lots of sensors tho)

    df['field_strength1'] = df['voltage1'] * magnetic_susceptibility1