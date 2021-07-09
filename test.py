import json
from os import path
import re

json_dir = path.join(path.dirname(__file__), 'json')


def read_json():
    with open(path.join(json_dir, 'new_test_data.json'), 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        python_json_data = json.loads(json_data)
        python_json_dict = python_json_data[0]

        python_json_dict['order']['patient']['address']['regAddress']['town'] = "ХУЕСТОВ"

        print(python_json_dict)

    with open(path.join(json_dir, 'new_test_data.json'), 'w', encoding='utf-8') as json_file:
        python_json_dict = str(python_json_dict).replace("'", '\"')
        print(python_json_dict)
        json.dump(f"[{python_json_dict}]", json_file, ensure_ascii=False)


read_json()
