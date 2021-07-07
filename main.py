import requests
import json

depart_number = 100149
token = '020996D1-75CC-16E6-09A0-8D1AE3C4463F'

login = {'depart number': depart_number,
         'token': token
         }

# Получение нового токена
response = requests.post('https://result.crie.ru/api/v2/order/get-depart-token',
                         login)

response_json = response.json()
response_token = response_json['body']['token']

# Открытие json файла
with open("new_test_data.json", "r", encoding='utf-8') as read_file:
    json_file = json.load(read_file)

# Отправка данных в api
transfer_info = {'depart number': depart_number,
                 'token': response_token,
                 'json': json_file}

transfer = requests.post('https://result.crie.ru/api/v2/order/ext-orders-package',
                         transfer_info)
transfer_json = transfer.json()

# Проверки
print('Данные из json файла')
print(json_file)
print('Данные учетной записи:')
print(login)
print('Полученный json от api:')
print(response_json)
print('Подставляю полученный token в post:')
print(transfer_json)
