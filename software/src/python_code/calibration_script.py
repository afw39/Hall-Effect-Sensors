''' runs the calibration, currents entered in A, magnetic fields entered in mT, radius in m'''
from calibration import Calibration

x = Calibration(number=8, port='/dev/ttyUSB0', vcc=5.0,
                filename='calibration-data.csv', vcc_un=0.05, samples=50, delay=1)

x.convert_currents(currents = [0.1, 2, 4], current_uncertainties=0.005,
                   number_of_turns=100, radius_of_coils=1)
