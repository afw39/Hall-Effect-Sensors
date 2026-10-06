# for finding the null voltage, shouldn't be too dissimilar? should be outputting the same thing every time

#from pathlib import Path
#import numpy as np
#import pandas as pd
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


    def read_data(self) -> None:
        '''
        docstring
        '''
        self.data = read_data(self.port, self.filename, self.samples)