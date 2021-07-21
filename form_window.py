import json
import configparser
from os import path
from PyQt5 import QtWidgets
from ui.form_window import Ui_FormWindow
from static import *


class FormWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FormWindow, self).__init__()
        self.setFixedSize(1260, 750)
        # Инициализация окна
        self.ui_2 = Ui_FormWindow()
        self.ui_2.setupUi(self)
        # Дата в реальном времени
        self.datetime_now = datetime.datetime.now()
        # Пути до папок
        self.config_dir = path.join(path.dirname(__file__), 'config')
        self.json_dir = path.join(path.dirname(__file__), 'json')
        self.result_dir = path.join(path.dirname(__file__), 'result')
        # Открытие файла конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'), encoding='utf-8')
        # Привязка кнопок
        self.ui_2.pushButton.clicked.connect(self.from_form_to_json)
        # Список на отправку
        self.list_of_dicts = []
        # Валидации
        validator(self.ui_2.lineEdit_15, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # 10 цифр номера телефона
        validator(self.ui_2.lineEdit_17, "(?:[1-2])")  # Пол
        validator(self.ui_2.lineEdit_21, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # СНИЛС
        validator(self.ui_2.lineEdit_23, "(?:[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]"
                                         "?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9])")  # ОМС
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
        # Текст по окну
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
        self.ui_2.comboBox_2.addItem('Паспорт гражданина РФ')
        self.ui_2.comboBox_2.addItem('Свидетельство о рождении')
        self.ui_2.comboBox_2.addItem('Вид на жительство')
        self.ui_2.comboBox_2.addItem('Заграничный паспорт')
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

    # Создание уникального номера для отправки
    def generate_unique_number(self):
        return f'FBUZ49-{self.datetime_now.strftime("%d-%m-%Y, %H-%M-%S")}'

    # Чтение json шаблона
    def read_json_template(self):
        with open(path.join(self.json_dir, 'new_test_data.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            python_json_data = json.loads(json_data)
            python_json_dict = python_json_data[0]  # Получает словарь

            return python_json_dict

    # Создание и запись json файла
    def write_json(self, data):
        with open(path.join(self.result_dir, f'test.json'), 'w', encoding='utf-8') as json_file:
            self.list_of_dicts.append(data)
            python_json = str(self.list_of_dicts).replace("'", '\"')  # Преобразует ковычки к нужному формату
            print(python_json)
            json.dump(f"{python_json}", json_file, ensure_ascii=False)

    def json_json(self, data):
        unique_number = self.generate_unique_number()
        with open(path.join(self.result_dir, f'{unique_number}.json'), 'w', encoding='utf-8') as json_file:
            self.list_of_dicts.append(data)
            python_json = str(self.list_of_dicts).replace("'", '\"')  # Преобразует ковычки к нужному формату
            print(python_json)
            json.dump(f"{python_json}", json_file, ensure_ascii=False)

    # Передача формы в json
    def from_form_to_json(self):
        depart_number = ''
        laboratory_name = ''
        laboratory_ogrn = ''

        for section in self.config.sections():
            if self.config.has_section('json_data'):
                if self.config.has_option(section, 'depart_number')\
                        and self.config.has_option(section, 'laboratory_name')\
                        and self.config.has_option(section, 'laboratory_ogrn'):
                    depart_number = self.config.get(section, 'depart_number')
                    laboratory_name = self.config.get(section, 'laboratory_name')
                    laboratory_ogrn = self.config.get(section, 'laboratory_ogrn')

        unique_number = self.generate_unique_number()
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

        python_json_dict = self.read_json_template()

        python_json_dict['order']['depart'] = depart_number
        python_json_dict['order']['laboratoryName'] = laboratory_name
        python_json_dict['order']['laboratoryOgrn'] = laboratory_ogrn
        python_json_dict['order']['number'] = unique_number
        python_json_dict['order']['name'] = organization_name
        python_json_dict['order']['ogrn'] = organization_ogrn
        python_json_dict['order']['orderDate'] = order_date

        python_json_dict['order']['serv'][0]['code'] = service_code
        python_json_dict['order']['serv'][0]['name'] = service_name
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
