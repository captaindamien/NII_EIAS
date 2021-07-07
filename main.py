import requests
import json

NII_key = {'depart number': 100149,
           'token': '020996D1-75CC-16E6-09A0-8D1AE3C4463F'
           }

# Получение нового токена
response = requests.get('https://result.crie.ru/api/v2/order/get-depart-token',
                        NII_key)
response_json = response.json()
response_token = response_json['body']['token']

print(response_json)

with open("test_data.json", "w") as write_file:
    json.dump(response_json, write_file)

json_file = "[{\"order\": {\"number\": \"TEST1\", \"depart\": \"100434\", \"laboratoryName\": \"ООО ТЕСТ\", " \
            "\"laboratoryOgrn\": \"1183443000146\", \"name\": \"ТЕСТ\", \"ogrn\": \"00000000000\", \"orderDate\": " \
            "\"2021-05-24\", \"serv\": [{\"code\": \"13001\", \"name\": \"ТЕСТ\", \"testSystem\": \"\", " \
            "\"biomaterDate\": \"2021-05-24\", \"result\": 0, \"type\": 1, \"value\": 0}], \"patient\": {\"surname\": " \
            "\"ТЕСТОВ\", \"name\": \"ТЕСТ\", \"patronymic\": \"ТЕСТОВИЧ\", \"gender\": 1, \"birthday\": " \
            "\"1969-07-04\", \"phone\": \"1234567890\", \"email\": \"\", \"documentType\": \"Паспорт гражданина РФ\", " \
            "\"documentNumber\": \"111111\", \"documentSerNumber\": \"1122\", \"snils\": \"11111111111\", " \
            "\"oms\": \"1111111111111111\", \"address\": {\"regAddress\": {\"town\": \"\", \"house\": \"\", " \
            "\"region\": \"Волгоградская область\", \"building\": \"\", \"district\": \"\", \"appartament\": \"\", " \
            "\"streetName\": \"\"}, \"factAddress\": {\"town\": \"\", \"house\": \"\", \"region\": \"Волгоградская " \
            "область\", \"building\": \"\", \"district\": \"\", \"appartament\": \"\", \"streetName\": \"\"}}}}}] "

transfer_info = {'depart number': 100149,
                 'token': response_token,
                 'json': json_file}

transfer = requests.post('https://result.crie.ru/api/v2/order/ext-orders-package',
                         transfer_info)
transfer_json = transfer.json()

print(transfer_json)
