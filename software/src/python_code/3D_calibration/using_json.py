import json
from pathlib import Path

path_json = Path(__file__).parent
output_json = path_json / 'sensors.json'

with open(output_json, encoding = 'utf-8') as f:
    sensor_data = json.load(f)

for sensor in sensor_data['sensors']:
    if sensor_data["direction"] == 'x':
        # calibrate x sensor idk

