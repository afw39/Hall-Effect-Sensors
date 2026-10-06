# for finding the null voltage, shouldn't be too dissimilar? should be outputting the same thing every time

#from pathlib import Path
import numpy as np
import pandas as pd
from read import read_data

class Nulls:
    '''
    doc
    '''
    def __init__(self, number: int, port: str, vcc: float, filename: str, bits: int, samples: int = 400):
        # not going to do uncertainties yet - will see how its going to work first
        self.number = number
        self.port = port
        self.vcc = vcc
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.data = None


    def find_parameters(self) -> None:
        '''
        docstring
        '''
        self.data = read_data(self.port, self.filename, self.samples)


        # okay so we have the data now
        # we need to have some kind of key so that we know what arduino pin/address
        # will relate to each column of the data being imported so that we can separate them
        # by address and then calibrate against that value from that - will think about this later

        # for the null voltage, this shouldn't be an issue but it probably will be for the
        # sensitivity
        # but it still is an issue that we know where each sensor is i think?

        # would be great if could store the value for each sensor in rows organised via 
        # which direction they are pointing. 

        self.null_frame = pd.DataFrame(np.zeros((2, self.number)), dtype = float)
        self.null_voltages = np.empty(self.number)

        for i in range(self.number):
            self.null_voltages[i] = (self.data[self.data.columns[i+1]]*self.vcc/self.bits).mean()



