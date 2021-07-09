import requests
import json
import os
import sys
import datetime
import configparser
from os import path
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from ui.form_window import Ui_FormWindow
from PyQt5.QtGui import QRegExpValidator


def set_text(form, text):
    form.setText(text)


def validator(form, form_range):
    serial_regex = QRegExp("^" + form_range)
    serial_validator = QRegExpValidator(serial_regex)
    form.setValidator(serial_validator)


class FormWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FormWindow, self).__init__()
        self.setFixedSize(1260, 790)
        # Инициализация окна
        self.ui_2 = Ui_FormWindow()
        self.ui_2.setupUi(self)
        # Пути до папок
        self.json_dir = path.join(path.dirname(__file__), 'json')
        # Привязка кнопок
        self.ui_2.pushButton.clicked.connect(self.from_form_to_json)
        # Валидации
        validator(self.ui_2.lineEdit_15, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # 10 цифр номера телефона
        validator(self.ui_2.lineEdit_17, "(?:[1-2])")
        # Текст по окну
        set_text(self.ui_2.label, 'Название организации-заказчика *')
        set_text(self.ui_2.label_2, 'ОГРН организации-заказчика *')
        set_text(self.ui_2.label_3, 'Дата заказа *')
        self.ui_2.dateEdit.setCalendarPopup(True)
        self.ui_2.dateEdit.setDate(datetime.datetime.now())
        set_text(self.ui_2.label_5, 'Информация о заказчике')
        self.ui_2.label_5.setAlignment(Qt.AlignCenter)
        self.ui_2.label_5.setStyleSheet("""
                                      font-weight: 900;
                                      """)
        set_text(self.ui_2.label_6, 'Информация об услуге')
        self.ui_2.label_6.setAlignment(Qt.AlignCenter)
        self.ui_2.label_6.setStyleSheet("""
                                      font-weight: 900;
                                      """)
        set_text(self.ui_2.label_8, 'Код заказываемой услуги *')
        set_text(self.ui_2.label_9, 'Название услуги *')
        set_text(self.ui_2.label_7, 'Тип сертифицированной тест-системы')
        set_text(self.ui_2.label_11, 'Дата взятия биоматериала *')
        self.ui_2.dateEdit_2.setCalendarPopup(True)
        self.ui_2.dateEdit_2.setDate(datetime.datetime.now())
        set_text(self.ui_2.label_10, 'Дата готовности результата исследования *')
        self.ui_2.dateEdit_3.setCalendarPopup(True)
        self.ui_2.dateEdit_3.setDate(datetime.datetime.now())
        set_text(self.ui_2.label_12, 'Результат *')
        self.ui_2.comboBox.addItem('0 - не обнаружено')
        self.ui_2.comboBox.addItem('1 - обнаружено')
        self.ui_2.comboBox.addItem('2 - сомнительно')
        self.ui_2.comboBox.addItem('3 - брак')
        set_text(self.ui_2.label_14, 'Тип исследования')
        set_text(self.ui_2.label_13, 'Значение результата')
        set_text(self.ui_2.label_15, 'Информация о пациенте')
        self.ui_2.label_15.setAlignment(Qt.AlignCenter)
        self.ui_2.label_15.setStyleSheet("""
                                      font-weight: 900;
                                      """)
        set_text(self.ui_2.label_17, 'Фамилия *')
        set_text(self.ui_2.label_18, 'Имя *')
        set_text(self.ui_2.label_16, 'Отчество *')
        set_text(self.ui_2.label_20, 'Пол (1 - муж., 2 - жен.) *')
        set_text(self.ui_2.label_19, 'Дата рождения *')
        self.ui_2.dateEdit_4.setCalendarPopup(True)
        self.ui_2.dateEdit_4.setDate(datetime.datetime.now())
        set_text(self.ui_2.label_21, 'Контактный телефон (ввод без 8)')
        set_text(self.ui_2.label_22, 'Адрес электронной почты')
        set_text(self.ui_2.label_23, 'Тип документа удостоверяющего личность *')
        self.ui_2.comboBox_2.addItem('Паспорт гражданина РФ')
        self.ui_2.comboBox_2.addItem('Свидетельство о рождении')
        self.ui_2.comboBox_2.addItem('Вид на жительство')
        self.ui_2.comboBox_2.addItem('Заграничный паспорт')
        set_text(self.ui_2.label_27, 'Серия документа удостоверяющего личность *')
        set_text(self.ui_2.label_25, 'Номер документа удостоверяющего личность *')
        set_text(self.ui_2.label_24, 'СНИЛС *')
        set_text(self.ui_2.label_26, 'Полис ОМС *')
        set_text(self.ui_2.label_52, 'Адрес регистрации пациента')
        self.ui_2.label_52.setAlignment(Qt.AlignCenter)
        self.ui_2.label_52.setStyleSheet("""
                                      font-weight: 900;
                                      """)
        set_text(self.ui_2.label_40, 'Область')
        set_text(self.ui_2.label_41, 'Район')
        set_text(self.ui_2.label_42, 'Город')
        set_text(self.ui_2.label_43, 'Улица')
        set_text(self.ui_2.label_45, 'Дом')
        set_text(self.ui_2.label_46, 'Строение')
        set_text(self.ui_2.label_44, 'Квартира')
        set_text(self.ui_2.label_53, 'Адрес фактического проживания пациента')
        self.ui_2.label_53.setAlignment(Qt.AlignCenter)
        self.ui_2.label_53.setStyleSheet("""
                                      font-weight: 900;
                                      """)
        set_text(self.ui_2.label_47, 'Область')
        set_text(self.ui_2.label_48, 'Район')
        set_text(self.ui_2.label_49, 'Город')
        set_text(self.ui_2.label_50, 'Улица')
        set_text(self.ui_2.label_54, 'Дом')
        set_text(self.ui_2.label_55, 'Строение')
        set_text(self.ui_2.label_51, 'Квартира')

    # Создание уникального номера для отправки
    def generate_unique_number(self):
        # Чтение конфига config.ini
        for section in self.config.sections():
            if self.config.has_option(section, 'transfer_number'):
                transfer_number = self.config.get(section, 'transfer_number')
                return f'FBUZ49-{self.datetime_now.strftime("%H:%M:%S-%d.%m.%Y")}-{transfer_number}'

    def read_json(self):
        with open(path.join(self.json_dir, 'new_test_data.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)
            python_json_dict = python_json_data[0]  # Получает словарь

            return python_json_dict

    def write_json(self, data):
        with open(path.join(self.json_dir, 'new_test_data.json'), 'w', encoding='utf-8') as json_file:
            python_json_dict = str(data).replace("'", '\"')
            print(python_json_dict)
            json.dump(f"[{python_json_dict}]", json_file, ensure_ascii=False)

    def from_form_to_json(self):
        organization_name = self.ui_2.lineEdit.text()
        organization_ogrn = self.ui_2.lineEdit_3.text()
        order_date = self.ui_2.dateEdit.text()

        service_code = self.ui_2.lineEdit_2.text()
        service_name = self.ui_2.lineEdit_7.text()
        test_system = self.ui_2.lineEdit_6.text()
        biomaterial_date = self.ui_2.dateEdit_2.text()
        ready_date = self.ui_2.dateEdit_3.text()
        result = self.ui_2.comboBox.currentText()
        service_type = self.ui_2.lineEdit_12.text()
        result_value = self.ui_2.lineEdit_11.text()

        patient_surname = self.ui_2.lineEdit_10.text()
        patient_name = self.ui_2.lineEdit_14.text()
        patient_patronymic = self.ui_2.lineEdit_13.text()
        patient_gender = self.ui_2.lineEdit_17.text()
        patient_birthday = self.ui_2.dateEdit_4.text()
        patient_phone = self.ui_2.lineEdit_15.text()
        patient_email = self.ui_2.lineEdit_18.text()
        patient_document_type = self.ui_2.comboBox_2.currentText()
        patient_document_serial = self.ui_2.lineEdit_22.text()
        patient_document_number = self.ui_2.lineEdit_20.text()
        patient_snils = self.ui_2.lineEdit_21.text()
        patient_oms = self.ui_2.lineEdit_23.text()

        registration_region = self.ui_2.textEdit.toPlainText()
        registration_district = self.ui_2.textEdit_4.toPlainText()
        registration_town = self.ui_2.lineEdit_36.text()
        registration_street = self.ui_2.textEdit_5.toPlainText()
        registration_house = self.ui_2.lineEdit_37.text()
        registration_building = self.ui_2.lineEdit_41.text()
        registration_apartment = self.ui_2.lineEdit_38.text()

        fact_region = self.ui_2.textEdit_2.toPlainText()
        fact_district = self.ui_2.textEdit_6.toPlainText()
        fact_town = self.ui_2.lineEdit_39.text()
        fact_street = self.ui_2.textEdit_7.toPlainText()
        fact_house = self.ui_2.lineEdit_40.text()
        fact_building = self.ui_2.lineEdit_43.text()
        fact_apartment = self.ui_2.lineEdit_42.text()

        python_json_dict = self.read_json()

        python_json_dict['order']['name'] = organization_name
        python_json_dict['order']['ogrn'] = organization_ogrn
        python_json_dict['order']['orderDate'] = order_date

        python_json_dict['order']['serv'][0]['code'] = service_code
        python_json_dict['order']['serv'][0]['Name'] = service_name
        python_json_dict['order']['serv'][0]['testSystem'] = test_system
        python_json_dict['order']['serv'][0]['biomaterDate'] = biomaterial_date
        python_json_dict['order']['serv'][0]['readyDate'] = ready_date
        python_json_dict['order']['serv'][0]['result'] = result[0]
        python_json_dict['order']['serv'][0]['type'] = service_type
        python_json_dict['order']['serv'][0]['value'] = result_value

        python_json_dict['order']['patient']['surname'] = patient_surname
        python_json_dict['order']['patient']['name'] = patient_name
        python_json_dict['order']['patient']['patronymic'] = patient_patronymic
        python_json_dict['order']['patient']['gender'] = patient_gender
        python_json_dict['order']['patient']['birthday'] = patient_birthday
        python_json_dict['order']['patient']['phone'] = patient_phone
        python_json_dict['order']['patient']['email'] = patient_email
        python_json_dict['order']['patient']['documentType'] = patient_document_type
        python_json_dict['order']['patient']['documentNumber'] = patient_document_number
        python_json_dict['order']['patient']['documentSerNumber'] = patient_document_serial
        python_json_dict['order']['patient']['snils'] = patient_snils
        python_json_dict['order']['patient']['oms'] = patient_oms

        python_json_dict['order']['patient']['address']['regAddress']['town'] = registration_town
        python_json_dict['order']['patient']['address']['regAddress']['house'] = registration_house
        python_json_dict['order']['patient']['address']['regAddress']['region'] = registration_region
        python_json_dict['order']['patient']['address']['regAddress']['building'] = registration_building
        python_json_dict['order']['patient']['address']['regAddress']['district'] = registration_district
        python_json_dict['order']['patient']['address']['regAddress']['appartament'] = registration_apartment
        python_json_dict['order']['patient']['address']['regAddress']['streetName'] = registration_street

        python_json_dict['order']['patient']['address']['factAddress']['town'] = fact_town
        python_json_dict['order']['patient']['address']['factAddress']['house'] = fact_house
        python_json_dict['order']['patient']['address']['factAddress']['region'] = fact_region
        python_json_dict['order']['patient']['address']['factAddress']['building'] = fact_building
        python_json_dict['order']['patient']['address']['factAddress']['district'] = fact_district
        python_json_dict['order']['patient']['address']['factAddress']['appartament'] = fact_apartment
        python_json_dict['order']['patient']['address']['factAddress']['streetName'] = fact_street

        self.write_json(python_json_dict)
