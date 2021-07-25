from base import find_transfer
import os
from os import path
import json
from static import generate_unique_number

json_dir = path.join(path.dirname(__file__), 'json')

with open(path.join(json_dir, 'template.json'), 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    python_json_dict = json.loads(json_data)

python_json_dict = python_json_dict[0]
print(python_json_dict)
transfer_list = find_transfer('25-07-2021')
print(transfer_list)
for el in transfer_list:
    unique_number = generate_unique_number()
    python_json_dict['order']['number'] = unique_number
    python_json_dict['order']['depart'] = '100149'
    python_json_dict['order']['laboratoryName'] = 'ФБУЗ Центр гигиены и эпидемиологии в Магаданской области'
    python_json_dict['order']['laboratoryOgrn'] = '1054900016214'

    python_json_dict['order']['name'] = el[2]
    python_json_dict['order']['ogrn'] = el[3]
    python_json_dict['order']['orderDate'] = el[4]

    python_json_dict['order']['serv'][0]['code'] = el[5]
    python_json_dict['order']['serv'][0]['name'] = el[6]
    python_json_dict['order']['serv'][0]['testSystem'] = el[7]
    python_json_dict['order']['serv'][0]['biomaterDate'] = el[8]
    python_json_dict['order']['serv'][0]['readyDate'] = el[9]
    python_json_dict['order']['serv'][0]['result'] = el[10][0]
    python_json_dict['order']['serv'][0]['type'] = el[11][0]
    python_json_dict['order']['serv'][0]['value'] = el[12]

    python_json_dict['order']['patient']['surname'] = el[13]
    python_json_dict['order']['patient']['name'] = el[14]
    python_json_dict['order']['patient']['patronymic'] = el[15]
    python_json_dict['order']['patient']['gender'] = el[16]
    python_json_dict['order']['patient']['birthday'] = el[17]
    python_json_dict['order']['patient']['phone'] = el[18]
    python_json_dict['order']['patient']['email'] = el[19]
    python_json_dict['order']['patient']['documentType'] = el[20]
    python_json_dict['order']['patient']['documentNumber'] = el[21]
    python_json_dict['order']['patient']['documentSerNumber'] = el[22]
    python_json_dict['order']['patient']['snils'] = el[23]
    python_json_dict['order']['patient']['oms'] = el[24]

    python_json_dict['order']['patient']['address']['regAddress']['town'] = el[25]
    python_json_dict['order']['patient']['address']['regAddress']['house'] = el[26]
    python_json_dict['order']['patient']['address']['regAddress']['region'] = el[27]
    python_json_dict['order']['patient']['address']['regAddress']['building'] = el[28]
    python_json_dict['order']['patient']['address']['regAddress']['district'] = el[29]
    python_json_dict['order']['patient']['address']['regAddress']['appartament'] = el[30]
    python_json_dict['order']['patient']['address']['regAddress']['streetName'] = el[31]

    python_json_dict['order']['patient']['address']['factAddress']['town'] = el[32]
    python_json_dict['order']['patient']['address']['factAddress']['house'] = el[33]
    python_json_dict['order']['patient']['address']['factAddress']['region'] = el[34]
    python_json_dict['order']['patient']['address']['factAddress']['building'] = el[35]
    python_json_dict['order']['patient']['address']['factAddress']['district'] = el[36]
    python_json_dict['order']['patient']['address']['factAddress']['appartament'] = el[37]
    python_json_dict['order']['patient']['address']['factAddress']['streetName'] = el[38]

print(python_json_dict)
