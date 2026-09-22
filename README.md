----------------------------------------------------------------------------------------------------------------

# Hall Effect Sensor Project

This repository contains all the information about the hall effect sensor array. The first stage of the project is starting with a basic version of the project. I will start with a few hall effect sensors and construct a working circuit with working software. The end goal of this project is to create a live magnetic field map using hall effect sensors and integrate that into MatchID software to visualise the magnetic field strength distributions across a sample undergoing deformation. The project consists of hardware (circuit design and experimental setup) and software (arduino code and python software) that collect data from the sensors and turn it into useful data.

------------------------------------------------------------------------------------------------------------------------
## Repository structure
```
.gitignore
LICENSE
README.md
hardware /
|---- CAD_design.md                         # explanation of the CAD design
|---- circuit_design.md                     # explanation of the circuit design
|---- equipment.md                          # equipment used for this project
|---- overview.md                           # general overview of how the experimental setup will work
software /
|---- overview.md                           # details how the arduino and python code work
|---- src/
|     |---- arduino_code/                   # contains all modules of arduino code
|           |---- arduino_code_1/
|                 |---- arduino_code_1.ino  
|           |---- arduino_code_4/
|                 |---- arduino_code_4.ino  
|           |---- arduino_code_8/
|                 |---- arduino_code_8.ino  
|     |---- python_code/                    # contains all modules of python code 
|           |---- calibration.py
|           |---- calibration_script.py
|           |---- conversion.py
|           |---- conversion_script.py
|           |---- read.py
|           |---- uncertainty.py
```


There is more information about each stage of the project in their respective folders, both `software/` and `hardware/` have a file called `overview.md` that goes into more details about each file in that directory and what they do. 
