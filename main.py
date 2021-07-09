import requests
import json
import os
import sys
import datetime
import configparser
from os import path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from ui.open_window import Ui_OpenWindow
from form_window import FormWindow
from ui.form_window import Ui_FormWindow


def set_text(form, text):
    form.setText(text)


class main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.setFixedSize(522, 295)
        # Инициализация окон
        self.ui = Ui_OpenWindow()
        self.ui_2 = FormWindow()
        self.ui.setupUi(self)
        # Подключение других окон
        self.init_handlers()
        # Дата в реальном времени
        self.datetime_now = datetime.datetime.now()
        # Пути до папок
        self.config_dir = path.join(path.dirname(__file__), 'config')
        self.json_dir = path.join(path.dirname(__file__), 'json')
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'))
        # Метод на чтение конфига
        self.read_config()
        # Привязка кнопок
        self.ui.pushButton_3.clicked.connect(self.transfer_data)
        # Текст по окну
        set_text(self.ui.pushButton, 'Внести данные пациента')
        set_text(self.ui.pushButton_2, 'Просмотреть ранее внесенные данные')
        set_text(self.ui.pushButton_3, 'Отправить отчет в ЕИАС')

    # Обработка нажатия для октрытия сторонних окон
    def init_handlers(self):
        self.ui.pushButton.clicked.connect(self.show_form_window)

    # Открытие окна конфигов
    def show_form_window(self):
        self.ui_2.show()

    # Метод на чтение конфига
    def read_config(self):
        with open(path.join(self.config_dir, 'config.ini')) as config:
            all_info = config.read()

    def transfer_data(self):
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
        with open(path.join(self.json_dir, 'new_test_data.json'), 'r', encoding='utf-8') as read_file:
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


app = QtWidgets.QApplication([])
# Оформление всего приложения
app.setStyle('Fusion')
application = main_window()
application.show()

sys.exit(app.exec())
