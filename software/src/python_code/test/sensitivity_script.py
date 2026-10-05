from sens import Sensitivity

x = Sensitivity(number = 8, port = '/dev/ttyUSB0', vcc = 5, vcc_un = 0.05,
                filename = 'calibration.csv', bits = 10, samples = 400, calibration_field = 0.01, field_uncertainty = 0.005)

x.current_comparison(current=4, current_uncertainty=0.05, number_of_turns=50, radius_of_coils=1)
