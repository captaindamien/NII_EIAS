import os
import re
from os import path
from PyQt5 import QtWidgets, QtCore, QtGui
from ui.all_jsons import Ui_JsonsWindow
import requests
import json
import configparser
from static import set_text


class JsonsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(JsonsWindow, self).__init__()
        self.setFixedSize(362, 350)
        # Инициализация окон
        self.ui_3 = Ui_JsonsWindow()
        self.ui_3.setupUi(self)
        # Пути до папок
        self.result_dir = path.join(path.dirname(__file__), 'result')
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.config_dir = path.join(path.dirname(__file__), 'config')
        self.json_dir = path.join(path.dirname(__file__), 'json')
        # Список всех файлов в папке result
        self.files = os.listdir(self.result_dir)
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'))
        # Добавляем только дату из имени файла
        self.reformat_filename()
        # Добавление списка в listView
        self.model = QtCore.QStringListModel(self)
        self.model.setStringList(self.files)
        self.ui_3.listView.setModel(self.model)
        self.ui_3.listView.setWordWrap(True)
        # Подключение кнопок
        self.ui_3.pushButton.clicked.connect(self.logging_transfer)
        self.ui_3.pushButton_2.clicked.connect(self.close_window)
        self.ui_3.pushButton_3.clicked.connect(self.refresh)
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle('Выбор документа для отправки')
        set_text(self.ui_3.pushButton, 'Отправить')
        self.ui_3.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        set_text(self.ui_3.pushButton_2, 'Отмена')
        self.ui_3.pushButton_2.setStyleSheet("""
                                             background-color: #f7c8c8;
                                             """)
        set_text(self.ui_3.pushButton_3, 'Обновить')
        self.ui_3.pushButton_3.setStyleSheet("""
                                             background-color: #d6dfff;
                                             """)

    # Закрытие окна
    def close_window(self):
        self.close()

    # Обновление списка
    def refresh(self):
        self.files = os.listdir(self.result_dir)
        self.reformat_filename()
        self.model.setStringList(self.files)

    def logging_transfer(self):
        date = self.get_date_for_transfer()
        # Открытие json файла
        with open(path.join(self.result_dir, f'FBUZ49-{date}.json'), 'r', encoding='utf-8') as read_file:
            json_file = json.load(read_file)
            python_json = json.loads(json_file)

        patient_list = []

        for patients_dict in python_json:
            surname = f"{patients_dict['order']['patient']['surname']}"
            name = f"{patients_dict['order']['patient']['name']}"
            patronymic = f"{patients_dict['order']['patient']['patronymic']}"
            patient = f'{surname} {name} {patronymic}'
            patient_list.append(patient)

        transfer_json = self.transfer_data()

        # Добавление ошибок
        for elements in range(len(patient_list)):
            if transfer_json['body'][int(elements)]['status'] == 'error':
                # Вставка элементов в каждый 2
                patient_list.insert(elements * 3 + 1, f"{transfer_json['body'][int(elements)]['message']}")
                # Вставка элементов в каждый 3
                patient_list.insert(elements * 3 + 2, '-----------------------------------------------')
            elif transfer_json['body'][int(elements)]['status'] == 'ok'\
                    or transfer_json['body'][int(elements)]['status'] == '':
                patient_list.insert(elements * 3 + 1, f"Успешно!")
                patient_list.insert(elements * 3 + 2, '-----------------------------------------------')

        self.model.setStringList(patient_list)

    # Добавляем только дату из имени файла
    def reformat_filename(self):
        for el in range(len(self.files)):
            new_el = re.search(r'-\d\d-\d\d-\d\d\d\d', self.files[el])
            new_el = new_el[0][1:]
            self.files[el] = new_el

    def get_date_for_transfer(self):
        return self.ui_3.listView.currentIndex().data()

    # Получение и отправка данных в API
    def transfer_data(self):
        date = self.get_date_for_transfer()
        # Открытие json файла
        with open(path.join(self.result_dir, f'FBUZ49-{date}.json'), 'r', encoding='utf-8') as read_file:
            json_file = json.load(read_file)

        depart_number = ''
        token = ''
        # Чтение конфига
        for section in self.config.sections():
            if self.config.has_section('json_data'):
                if self.config.has_option(section, 'depart_number'):
                    depart_number = self.config.get(section, 'depart_number')
            if self.config.has_section('transfer_data'):
                if self.config.has_option(section, 'token'):
                    token = self.config.get(section, 'token')

        login = {'depart number': depart_number,
                 'token': token
                 }

        # Получение нового токена
        response = requests.post('https://result.crie.ru/api/v2/order/get-depart-token',
                                 login)

        response_json = response.json()
        response_token = response_json['body']['token']

        # Отправка данных в api
        transfer_info = {'depart number': depart_number,
                         'token': response_token,
                         'json': json_file}

        transfer = requests.post('https://result.crie.ru/api/v2/order/ext-orders-package',
                                 transfer_info)
        transfer_json = transfer.json()

        return transfer_json
