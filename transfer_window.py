import os
from os import path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QAbstractItemView
from pipenv.vendor.urllib3.exceptions import MaxRetryError

from ui.transfer_window import Ui_TransferWindow
import requests
import json
import configparser
from static import set_text
from time import sleep
from base import find_transfer, success
from static import generate_unique_number, get_organization
from error_window import ErrorWindow


class TransferWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TransferWindow, self).__init__()
        self.setFixedSize(482, 340)
        # Инициализация окон
        self.ui_3 = Ui_TransferWindow()
        self.ui_7 = ErrorWindow()
        self.ui_3.setupUi(self)
        # Пути до папок
        self.result_dir = path.join(path.dirname(__file__), 'result')
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.config_dir = path.join(path.dirname(__file__), 'config')
        self.json_dir = path.join(path.dirname(__file__), 'json')
        self.log_dir = path.join(path.dirname(__file__), 'log')
        # Список всех файлов в папке result
        self.files = os.listdir(self.result_dir)
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'), encoding='utf-8')
        # Берем имя организации для имени файла
        self.date = ''
        self.organization_name = get_organization()
        # Добавление списка в listView
        self.model = QtCore.QStringListModel(self)
        self.ui_3.listView.setModel(self.model)
        self.ui_3.listView.setWordWrap(True)
        self.ui_3.listView.hide()
        # Запрет редактирования элементов listView
        self.ui_3.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Прогрессбар
        self.ui_3.progressBar.hide()
        # Подключение кнопок
        self.ui_3.pushButton.clicked.connect(self.create_json)
        self.ui_3.pushButton_2.clicked.connect(self.close_window)
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle('Выбор даты для отправки')
        set_text(self.ui_3.pushButton, 'Отправить')
        self.ui_3.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        set_text(self.ui_3.pushButton_2, 'Закрыть')
        self.ui_3.pushButton_2.setStyleSheet("""
                                             background-color: #f7c8c8;
                                             """)

    # Закрытие окна
    def close_window(self):
        self.close()

    def show_error_window(self, error):
        label = self.ui_7.findChildren(QLabel)

        for item in label:
            item.setText(error)

        self.ui_7.show()

    def get_date_for_transfer(self):
        date = self.ui_3.calendarWidget.selectedDate()
        return date.toString('dd-MM-yyyy')

    # Чтение json шаблона
    def read_json_template(self):
        with open(path.join(self.json_dir, 'template.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)

            return python_json_data

    def read_json_today(self):
        with open(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json'), 'r', encoding='utf-8')\
                as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)

            return python_json_data

    # Создание и запись json файла
    def write_json(self, data):
        if os.path.exists(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json')):
            json_list = self.read_json_today()
        else:
            json_list = self.read_json_template()

        with open(path.join(self.result_dir,
                            f'{self.organization_name}-{self.date}.json'), 'w', encoding='utf-8') as json_file:
            if json_list[0]['order']['depart'] != '':
                json_list.append(data)
            else:
                json_list = [data]
            python_json = str(json_list).replace("'", '\"')  # Преобразует ковычки к нужному формату

            json.dump(f"{python_json}", json_file, ensure_ascii=False)

    def create_json(self):
        # Берет дату с календаря
        self.date += self.get_date_for_transfer()

        depart_number = ''
        laboratory_name = ''
        laboratory_ogrn = ''

        # Чтение конфига
        for section in self.config.sections():
            if self.config.has_section('json_data'):
                if self.config.has_option(section, 'depart_number')\
                        and self.config.has_option(section, 'laboratory_name')\
                        and self.config.has_option(section, 'laboratory_ogrn'):
                    depart_number = self.config.get(section, 'depart_number')
                    laboratory_name = self.config.get(section, 'laboratory_name')
                    laboratory_ogrn = self.config.get(section, 'laboratory_ogrn')

        if os.path.exists(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json')):
            python_json_dict = self.read_json_today()
        else:
            python_json_dict = self.read_json_template()

        python_json_dict = python_json_dict[0]

        transfer_list = find_transfer(self.date)

        if not transfer_list:
            python_json_dict['order']['patient']['surname'] = 'В базе'
            python_json_dict['order']['patient']['name'] = 'нет пациентов'
            python_json_dict['order']['patient']['patronymic'] = 'для отправки'
            self.write_json(python_json_dict)

        progress = 0
        if transfer_list:
            self.ui_3.progressBar.show()

        for el in range(len(transfer_list)):
            unique_number = generate_unique_number()

            python_json_dict['order']['number'] = unique_number
            python_json_dict['order']['depart'] = depart_number
            python_json_dict['order']['laboratoryName'] = laboratory_name
            python_json_dict['order']['laboratoryOgrn'] = laboratory_ogrn
            python_json_dict['order']['name'] = transfer_list[el][2]
            python_json_dict['order']['ogrn'] = transfer_list[el][3]
            python_json_dict['order']['orderDate'] = transfer_list[el][4]

            python_json_dict['order']['serv'][0]['code'] = transfer_list[el][5]
            python_json_dict['order']['serv'][0]['name'] = transfer_list[el][6]
            python_json_dict['order']['serv'][0]['testSystem'] = transfer_list[el][7]
            python_json_dict['order']['serv'][0]['biomaterDate'] = transfer_list[el][8]
            python_json_dict['order']['serv'][0]['readyDate'] = transfer_list[el][9]
            python_json_dict['order']['serv'][0]['result'] = transfer_list[el][10][0]
            python_json_dict['order']['serv'][0]['type'] = transfer_list[el][11][0]
            python_json_dict['order']['serv'][0]['value'] = transfer_list[el][12]

            python_json_dict['order']['patient']['surname'] = transfer_list[el][13]
            python_json_dict['order']['patient']['name'] = transfer_list[el][14]
            python_json_dict['order']['patient']['patronymic'] = transfer_list[el][15]
            python_json_dict['order']['patient']['gender'] = transfer_list[el][16]
            python_json_dict['order']['patient']['birthday'] = transfer_list[el][17]
            python_json_dict['order']['patient']['phone'] = transfer_list[el][18]
            python_json_dict['order']['patient']['email'] = transfer_list[el][19]
            python_json_dict['order']['patient']['documentType'] = transfer_list[el][20]
            python_json_dict['order']['patient']['documentNumber'] = transfer_list[el][22]
            python_json_dict['order']['patient']['documentSerNumber'] = transfer_list[el][21]
            python_json_dict['order']['patient']['snils'] = transfer_list[el][23]
            python_json_dict['order']['patient']['oms'] = transfer_list[el][24]

            python_json_dict['order']['patient']['address']['regAddress']['town'] = transfer_list[el][25]
            python_json_dict['order']['patient']['address']['regAddress']['house'] = transfer_list[el][26]
            python_json_dict['order']['patient']['address']['regAddress']['region'] = transfer_list[el][27]
            python_json_dict['order']['patient']['address']['regAddress']['building'] = transfer_list[el][28]
            python_json_dict['order']['patient']['address']['regAddress']['district'] = transfer_list[el][29]
            python_json_dict['order']['patient']['address']['regAddress']['appartament'] = transfer_list[el][30]
            python_json_dict['order']['patient']['address']['regAddress']['streetName'] = transfer_list[el][31]

            python_json_dict['order']['patient']['address']['factAddress']['town'] = transfer_list[el][32]
            python_json_dict['order']['patient']['address']['factAddress']['house'] = transfer_list[el][33]
            python_json_dict['order']['patient']['address']['factAddress']['region'] = transfer_list[el][34]
            python_json_dict['order']['patient']['address']['factAddress']['building'] = transfer_list[el][35]
            python_json_dict['order']['patient']['address']['factAddress']['district'] = transfer_list[el][36]
            python_json_dict['order']['patient']['address']['factAddress']['appartament'] = transfer_list[el][37]
            python_json_dict['order']['patient']['address']['factAddress']['streetName'] = transfer_list[el][38]

            self.write_json(python_json_dict)
            sleep(1)

            progress += 100 / len(transfer_list)
            self.ui_3.progressBar.setValue(progress)

        self.logging_transfer()

    def logging_transfer(self):
        # Открытие json файла
        with open(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json'), 'r', encoding='utf-8')\
                as read_file:
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
        status_list = []

        # Передача статусов в лог, если json не пустой
        if patient_list[0] != 'В базе нет пациентов для отправки':
            with open(path.join(self.log_dir, 'console_log.txt'), 'a') as log_file:
                log_file.write(f'{str(transfer_json)}\n\n')

        transfer_list = find_transfer(self.date)

        # Добавление ошибок
        for elements in range(len(transfer_list)):
            if transfer_json['body'][int(elements)]['status'] == 'error':
                # Вставка элементов в каждый 2
                patient_list.insert(elements * 3 + 1, f"{transfer_json['body'][int(elements)]['message']}")
                # Вставка элементов в каждый 3
                patient_list.insert(elements * 3 + 2, '----------------------------------------------'
                                                      '--------------------------')
                status_list.append('error')
            elif transfer_json['body'][int(elements)]['status'] == 'ok'\
                    or transfer_json['body'][int(elements)]['status'] == '':
                patient_list.insert(elements * 3 + 1, f"Успешно!")
                patient_list.insert(elements * 3 + 2, '----------------------------------------------'
                                                      '--------------------------')
                status_list.append('ok')

        for elem in range(len(status_list)):
            if status_list[elem] == 'ok':
                success(transfer_list[elem][0], 1)

        # Скрывает календарь и показывает листвью
        self.ui_3.calendarWidget.hide()
        self.ui_3.listView.show()
        self.model.setStringList(patient_list)
        self.ui_3.pushButton.setEnabled(False)

        if os.path.isfile(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json')):
            os.remove(path.join(self.result_dir, f'{self.organization_name}-{self.date}.json'))

        self.date = ''

    # Получение и отправка данных в API
    def transfer_data(self):
        try:
            date = self.get_date_for_transfer()
            organization_name = get_organization()
            # Открытие json файла
            with open(path.join(self.result_dir, f'{organization_name}-{date}.json'), 'r', encoding='utf-8')\
                    as read_file:
                json_file = json.load(read_file)

            depart_number = ''
            token = ''
            address = ''
            # Чтение конфига
            for section in self.config.sections():
                if self.config.has_section('json_data'):
                    if self.config.has_option(section, 'depart_number'):
                        depart_number = self.config.get(section, 'depart_number')
                if self.config.has_section('transfer_data'):
                    if self.config.has_option(section, 'token') and self.config.has_option(section, 'address'):
                        token = self.config.get(section, 'token')
                        address = self.config.get(section, 'address')

            login = {'depart number': depart_number,
                     'token': token
                     }

            # Получение нового токена
            response = requests.post(f'https://{address}/api/v2/order/get-depart-token',
                                     login)

            response_json = response.json()
            response_token = response_json['body']['token']

            # Отправка данных в api
            transfer_info = {'depart number': depart_number,
                             'token': response_token,
                             'json': json_file}

            transfer = requests.post(f'https://{address}/api/v2/order/ext-orders-package',
                                     transfer_info)
            transfer_json = transfer.json()

            return transfer_json
        # Обработка ConnectionError при отключенном Континент АП
        except requests.exceptions.ConnectionError:
            self.show_error_window('Нет связи с сервером')
            self.close_window()
