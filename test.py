import os
from os import path
import json

result_dir = path.join(path.dirname(__file__), 'result')


with open(path.join(result_dir, f'FBUZ49-22-07-2021.json'), 'r', encoding='utf-8') as read_file:
    json_file = json.load(read_file)
    python_json = json.loads(json_file)
    for patients_dict in python_json:
        print(f"{patients_dict['order']['patient']['surname']}"
              f"{patients_dict['order']['patient']['name']}"
              f"{patients_dict['order']['patient']['patronymic']}")