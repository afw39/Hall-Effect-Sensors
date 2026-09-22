# going to try find the standard deviation of the signal outputted
# by the sensors and plot them in a histogram??? (and hope they
# follow a normal distribution)

# steps:
# 1. read data, like 100 samples maybs
# 2. find the mean
# 3. subtract the mean from each data point
# 4. square this result
# 5. average these squares (gets variance)
# 6. square root this average (s.d.)

# not sure how im going to get like loads of standard deviations to plot but will be fine, 
# we can cross that bridge when we get there

import pandas as pd
import matplotlib.pyplot as plt
from read import read_data

sd_data = read_data(port = '/dev/ttyACM0', filename = 'standard-deviation.csv', samples = 4000)

class StandardDeviation:
    '''
    docstring
    '''
    def __init__(self, data:pd.DataFrame, number: int):
        self.data = data
        self.number = number

    def calc_standard_deviation(self) -> list:
        '''
        docstring
        '''
        std = [0] * self.number

        for i in range(self.number):
            cols = self.data[self.data.columns[i+1]]
            std[i] = cols.std(ddof=1)

        return std
    
x = StandardDeviation(data = sd_data, number = 8)
stds = x.calc_standard_deviation()
print(stds)


fig, axs = plt.subplots(2, 4, figsize=(12, 6))

for i in range(8):
    col = sd_data[sd_data.columns[i+1]]

    axs[i//4, i%4].hist(col, bins=20)
    axs[i//4, i%4].set_title(f"Sensor {i+1}")

plt.tight_layout()

plt.show()
