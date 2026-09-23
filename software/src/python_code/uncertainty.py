'''finds the standard deviation and visualises noise analysis of sensor array'''

import matplotlib.pyplot as plt
from read import read_data

class StandardDeviation:
    '''
    Class for finding the standard deviation of each sensor across 'samples' number of sample

    Attributes
        number (int): the number of sensors in the array
        port (str): the port of the computer that the Arduino is connected to
        filename (str): where the data that is read in will be stored
        samples (int): how many samples are taken
    
    Methods
        calc_standard_deviation() -> list: 
            calculates the standard deviation of each column of the dataframe which corresponds
            to each sensors set of data
        plot() -> None:
            plots the distribution of data points for each sensor to visualise the noise
        run() -> None:
            runs the other two methods in the class
    '''
    def __init__(self, number: int, port: str, filename: str, samples: int):
        self.number = number
        self.data = None

        self.data = read_data(port, filename, samples)

    def calc_standard_deviation(self) -> list:
        '''
        calculates the standard deviation for each sensor
        Args:
            None
        Returns:
            std (list): the list of the standard deviations for each sensor
        '''
        std = [0] * self.number

        for i in range(self.number):
            cols = self.data[self.data.columns[i+1]]
            std[i] = cols.std(ddof=1)

        return std

    def plot(self) -> None:
        '''
        plots the noise analysis histograms
        Args:
            None
        Returns:
            None
        '''
        fig, axs = plt.subplots(2,4, figsize = (12,6))

        for i in range(self.number):
            col = self.data[self.data.columns[i+1]]

            axs[i//4, i%4].hist(col, bins = 35)
            axs[i//4, i%4].set_title(f"sensor {i+1}")

        plt.tight_layout()
        plt.show()