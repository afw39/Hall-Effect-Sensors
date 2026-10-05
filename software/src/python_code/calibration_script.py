''' runs the calibration, currents entered in A, magnetic fields entered in mT, radius in m'''
from calibration_new import Calibration

x = Calibration(number=8, port='/dev/ttyUSB0', vcc=5.0, filename='calibration-data.csv',
                vcc_un=0.05, bits = 10, samples=50, delay=1)

#x.convert_currents(currents = [0.1, 2, 4], current_uncertainties=0.005,
# number_of_turns=100, radius_of_coils=1)

x.perform_calibration(calibration_field = 70, uncertainty_in_field = 0.05)

# so like wanna run this script once, then wanna run the perform calibration
# a couple more times probs (maybe need to put this in a different script,
# but cant do that cause i need the variables in the code)

# issue is, if i run this script over and over its going to do the nulls all over again and everything.
# one option is to make the outputs likethe returns

# but if i hashtag the Calibration start bit idk if its going to like it. Might need to make it a separate class?

# maybe i just run the whole thing for every new field - not sure it will make a difference?
