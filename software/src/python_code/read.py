import csv
from pathlib import Path
import serial
import pandas as pd


def read_data(port: str, filename: str) -> pd.DataFrame:
    '''
    Uses the serial library to get the data from the arduino, saves it as a csv file.
    Args:
        port (str): computer port that the arduino is connected to
    Retuns:
        df (pd.DataFrame): the dataframe that the arduino data is stored in
    '''
    ser = serial.Serial(port, 9600)
    script_dir = Path(__file__).parent
    csv_file = script_dir / filename

    with open(csv_file, 'w', newline = '', encoding = 'utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        header = ser.readline().decode().strip()
        writer.writerow(header.split(","))

        while True:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(',')
                writer.writerow(values)
                print(values)
    # closes the file
    ser.close()

    df = pd.read_csv(csv_file)
    return df
