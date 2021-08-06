import os
import json
import datetime
import configparser
from os import path
from PyQt5 import QtWidgets, QtGui
from ui.form_window import Ui_FormWindow
from base import from_tuple_to_patients_table
from static import set_text, set_title_font, set_date_format, validator, generate_filename


class FormWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FormWindow, self).__init__()
        self.setFixedSize(1172, 705)
        # Инициализация окна
        self.ui_2 = Ui_FormWindow()
        self.ui_2.setupUi(self)
        # Дата в реальном времени
        self.datetime_now = datetime.datetime.now()
        # Пути до папок
        self.config_dir = path.join(path.dirname(__file__), 'config')
        self.json_dir = path.join(path.dirname(__file__), 'json')
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.result_dir = path.join(path.dirname(__file__), 'result')
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'), encoding='utf-8')
        # Привязка кнопок
        self.ui_2.pushButton.clicked.connect(self.from_form_to_json)
        self.ui_2.pushButton_3.clicked.connect(self.close_window)
        # Формат даты
        set_date_format(self.ui_2.dateEdit)
        set_date_format(self.ui_2.dateEdit_2)
        set_date_format(self.ui_2.dateEdit_3)
        set_date_format(self.ui_2.dateEdit_4)
        # Формат заголовка
        set_title_font(self.ui_2.label_5)
        set_title_font(self.ui_2.label_6)
        set_title_font(self.ui_2.label_15)
        set_title_font(self.ui_2.label_52)
        set_title_font(self.ui_2.label_53)
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle('Внесение данных вручную')
        set_text(self.ui_2.label, 'Название организации-заказчика *')
        set_text(self.ui_2.label_2, 'ОГРН организации-заказчика *')
        set_text(self.ui_2.label_3, 'Дата заказа *')
        set_text(self.ui_2.label_5, 'Информация о заказчике')
        set_text(self.ui_2.label_6, 'Информация об услуге')
        set_text(self.ui_2.label_8, 'Код заказываемой услуги *')
        set_text(self.ui_2.label_9, 'Название услуги *')
        set_text(self.ui_2.label_7, 'Тип сертифицированной тест-системы')
        set_text(self.ui_2.label_11, 'Дата взятия биоматериала *')
        set_text(self.ui_2.label_10, 'Дата готовности результата исследования *')
        set_text(self.ui_2.label_12, 'Результат *')
        self.ui_2.comboBox.addItem('0 - не обнаружено')
        self.ui_2.comboBox.addItem('1 - обнаружено')
        self.ui_2.comboBox.addItem('2 - сомнительно')
        self.ui_2.comboBox.addItem('3 - брак')
        set_text(self.ui_2.label_14, 'Тип исследования')
        self.ui_2.comboBox_2.addItem('1 - ПЦР COVID, качественное')
        self.ui_2.comboBox_2.addItem('2 - Антитела COVID, качественное IgG')
        self.ui_2.comboBox_2.addItem('3 - Антитела COVID, качественное IgM')
        self.ui_2.comboBox_2.addItem('4 - Антитела COVID, суммарное значение IgG и IgM')
        set_text(self.ui_2.label_13, 'Значение результата')
        set_text(self.ui_2.label_15, 'Информация о пациенте')
        set_text(self.ui_2.label_17, 'Фамилия *')
        set_text(self.ui_2.label_18, 'Имя *')
        set_text(self.ui_2.label_16, 'Отчество *')
        set_text(self.ui_2.label_20, 'Пол (1 - муж., 2 - жен.) *')
        set_text(self.ui_2.label_19, 'Дата рождения *')
        set_text(self.ui_2.label_21, 'Контактный телефон (ввод без 8)')
        set_text(self.ui_2.label_22, 'Адрес электронной почты')
        set_text(self.ui_2.label_23, 'Тип документа удостоверяющего личность *')
        self.ui_2.comboBox_3.addItem('Паспорт гражданина РФ')
        self.ui_2.comboBox_3.addItem('Свидетельство о рождении')
        self.ui_2.comboBox_3.addItem('Вид на жительство')
        self.ui_2.comboBox_3.addItem('Заграничный паспорт')
        set_text(self.ui_2.label_27, 'Серия документа удостоверяющего личность *')
        set_text(self.ui_2.label_25, 'Номер документа удостоверяющего личность *')
        set_text(self.ui_2.label_24, 'СНИЛС *')
        set_text(self.ui_2.label_26, 'Полис ОМС *')
        set_text(self.ui_2.label_52, 'Адрес регистрации пациента')
        set_text(self.ui_2.label_40, 'Область')
        set_text(self.ui_2.label_41, 'Район')
        set_text(self.ui_2.label_42, 'Город')
        set_text(self.ui_2.label_43, 'Улица')
        set_text(self.ui_2.label_45, 'Дом')
        set_text(self.ui_2.label_46, 'Строение')
        set_text(self.ui_2.label_44, 'Квартира')
        set_text(self.ui_2.label_53, 'Адрес фактического проживания пациента')
        set_text(self.ui_2.label_47, 'Область')
        set_text(self.ui_2.label_48, 'Район')
        set_text(self.ui_2.label_49, 'Город')
        set_text(self.ui_2.label_50, 'Улица')
        set_text(self.ui_2.label_54, 'Дом')
        set_text(self.ui_2.label_55, 'Строение')
        set_text(self.ui_2.label_51, 'Квартира')
        set_text(self.ui_2.pushButton, 'Подтвердить')
        self.ui_2.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        set_text(self.ui_2.pushButton_3, 'Отмена')
        self.ui_2.pushButton_3.setStyleSheet("""
                                             background-color: #f7c8c8;
                                             """)

    # Закрытие окна
    def close_window(self):
        self.close()

    # Валидации (Вызывается при нажатии кнопки в main.py)
    def validations(self):
        validator(self.ui_2.lineEdit_11, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # 10 цифр номера телефона
        validator(self.ui_2.lineEdit_10, "(?:[1-2])")  # Пол
        validator(self.ui_2.lineEdit_15, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # СНИЛС
        validator(self.ui_2.lineEdit_16, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # ОМС

    # Чтение json шаблона
    def read_json_template(self):
        with open(path.join(self.json_dir, 'template.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)

            return python_json_data

    def read_json_today(self):
        filename = generate_filename()
        with open(path.join(self.result_dir, f'{filename}.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)

            return python_json_data

    # Создание и запись json файла
    def write_json(self, data):
        filename = generate_filename()

        if os.path.exists(path.join(self.result_dir, f'{filename}.json')):
            json_list = self.read_json_today()
        else:
            json_list = self.read_json_template()

        with open(path.join(self.result_dir, f'{filename}.json'), 'w', encoding='utf-8') as json_file:
            if json_list[0]['order']['depart'] != '':
                json_list.append(data)
            else:
                json_list = [data]
            python_json = str(json_list).replace("'", '\"')  # Преобразует ковычки к нужному формату

            json.dump(f"{python_json}", json_file, ensure_ascii=False)

    # Передача формы в json
    def from_form_to_json(self):
        organization_name = self.ui_2.lineEdit.text()
        organization_ogrn = self.ui_2.lineEdit_2.text()
        order_date = self.ui_2.dateEdit.text()

        service_code = self.ui_2.lineEdit_3.text()
        service_name = self.ui_2.lineEdit_4.text()
        test_system = self.ui_2.lineEdit_5.text()
        biomaterial_date = self.ui_2.dateEdit_2.text()
        ready_date = self.ui_2.dateEdit_3.text()
        result = self.ui_2.comboBox.currentText()
        service_type = self.ui_2.comboBox_2.currentText()
        result_value = self.ui_2.lineEdit_6.text()

        patient_surname = self.ui_2.lineEdit_7.text()
        patient_name = self.ui_2.lineEdit_8.text()
        patient_patronymic = self.ui_2.lineEdit_9.text()
        patient_gender = self.ui_2.lineEdit_10.text()
        patient_birthday = self.ui_2.dateEdit_4.text()
        patient_phone = self.ui_2.lineEdit_11.text()
        patient_email = self.ui_2.lineEdit_12.text()
        patient_document_type = self.ui_2.comboBox_3.currentText()
        patient_document_serial = self.ui_2.lineEdit_13.text()
        patient_document_number = self.ui_2.lineEdit_14.text()
        patient_snils = self.ui_2.lineEdit_15.text()
        patient_oms = self.ui_2.lineEdit_16.text()

        registration_region = self.ui_2.lineEdit_17.text()
        registration_district = self.ui_2.lineEdit_18.text()
        registration_town = self.ui_2.lineEdit_19.text()
        registration_street = self.ui_2.lineEdit_20.text()
        registration_house = self.ui_2.lineEdit_21.text()
        registration_building = self.ui_2.lineEdit_22.text()
        registration_apartment = self.ui_2.lineEdit_23.text()

        fact_region = self.ui_2.lineEdit_24.text()
        fact_district = self.ui_2.lineEdit_25.text()
        fact_town = self.ui_2.lineEdit_26.text()
        fact_street = self.ui_2.lineEdit_27.text()
        fact_house = self.ui_2.lineEdit_28.text()
        fact_building = self.ui_2.lineEdit_29.text()
        fact_apartment = self.ui_2.lineEdit_30.text()

        success = 0
        date = self.datetime_now.strftime("%d-%m-%Y")

        patient_list = [date, organization_name, organization_ogrn, order_date, service_code, service_name, test_system,
                        biomaterial_date, ready_date, result, service_type, result_value, patient_surname, patient_name,
                        patient_patronymic, patient_gender, patient_birthday, patient_phone, patient_email,
                        patient_document_type, patient_document_serial, patient_document_number, patient_snils,
                        patient_oms, registration_town, registration_house, registration_region, registration_building,
                        registration_district, registration_apartment, registration_street, fact_town, fact_house,
                        fact_region, fact_building, fact_district, fact_apartment, fact_street, success]

        from_tuple_to_patients_table(tuple(patient_list))

        self.close()
