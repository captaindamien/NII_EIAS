import os
import json
from os import path
import re

json_dir = path.join(path.dirname(__file__), 'result')


def read_json():
    with open(path.join(json_dir, 'test.json'), 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        python_json_data = json.loads(json_data)
        print(type(python_json_data))
        print(len(python_json_data))
        exi = os.path.exists(path.join(json_dir, f'tests.json'))
        print(exi)

    with open(path.join(json_dir, 'test.json'), 'w', encoding='utf-8') as json_file:

        python_json_dict = str(python_json_data).replace("'", '\"')
        json.dump(f"{python_json_dict}", json_file, ensure_ascii=False)


read_json()
