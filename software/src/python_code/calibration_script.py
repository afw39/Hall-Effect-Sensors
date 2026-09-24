from calibration import Calibration

x = Calibration(number = 8, port = '/dev/ttyUSB0', vcc = 5.0,
                filename = 'calibration-data.csv', vcc_un = 0.05, samples = 50, delay = 1)
x.perform_calibration(fields = [0.2, 0.6], fields_uncertainty = 0.005) # input fields in mT

# okay so i kind of want to have the input of this to just be the current fed through the coils, will have to add a little method
# in the calibration class for doing this calculation - will be better than having to do it by hand every time?

# so will finish that this afternoon after lunch and then also work out what multiplexer is going to do
# and how the grove shield is going to fit into the experimental design
# then tomorrow the plan is def get a solid idea of what the live feed version of the magentic camera is
# can start thinking of the setup of the pre-recorded version but it will probably be fine
