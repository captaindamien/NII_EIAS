import requests
import json
import sys
import datetime
import configparser
from os import path
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from ui.open_window import Ui_OpenWindow
from form_window import FormWindow
from static import set_text, set_title_font


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(522, 250)
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
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'))
        # Привязка кнопок
        self.ui.pushButton_3.clicked.connect(self.transfer_data)
        # Текст по окну
        set_text(self.ui.label, 'Внести данные пациента')
        set_title_font(self.ui.label)
        set_text(self.ui.pushButton, 'Вручную')
        set_text(self.ui.pushButton_4, 'Импорт из эксель файла (Не доступно)')
        self.ui.pushButton_4.setEnabled(False)
        set_text(self.ui.pushButton_2, 'Просмотреть ранее внесенные данные (Не доступно)')
        self.ui.pushButton_2.setEnabled(False)
        set_text(self.ui.pushButton_3, 'Отправить отчет в ЕИАС')
        self.ui.pushButton_3.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        self.ui.pushButton_3.setIcon(QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        self.ui.pushButton_3.setIconSize(QSize(35, 35))

    # Обработка нажатия для октрытия сторонних окон
    def init_handlers(self):
        self.ui.pushButton.clicked.connect(self.show_form_window)

    # Открытие окна конфигов
    def show_form_window(self):
        self.ui_2.show()

    # Получение и отправка данных в API
    def transfer_data(self):
        # Открытие json файла
        with open(path.join(self.json_dir, 'new_test_data.json'), 'r', encoding='utf-8') as read_file:
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
application = MainWindow()
application.show()

sys.exit(app.exec())
