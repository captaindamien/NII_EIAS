from os import path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel, QAbstractItemView
from ui.search_window import Ui_SearchWindow
from error_window import ErrorWindow
from base import find_patients, find_patient_info, find_patient_combobox_info, find_all_patients,\
    delete_patient
import datetime
from static import set_text
from change_window import ChangeWindow


class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setFixedSize(362, 460)
        # Инициализация окон
        self.ui_5 = Ui_SearchWindow()
        self.ui_2 = ChangeWindow()
        self.ui_7 = ErrorWindow()
        self.ui_5.setupUi(self)
        # Модель для listView
        self.model = QtCore.QStringListModel(self)
        self.ui_5.listView.setEnabled(False)
        self.ui_5.listView.setWordWrap(True)
        self.ui_5.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования элементов listView
        self.ui_5.listView.setStyleSheet("""
                                         background-color: #e0e0e0;
                                         """)
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Подключение кнопок
        self.ui_5.pushButton.clicked.connect(self.show_change_window)
        self.ui_5.pushButton_2.clicked.connect(self.close_window)
        self.ui_5.pushButton_3.clicked.connect(self.delete_patient)
        self.ui_5.pushButton_4.clicked.connect(self.search_result)
        self.ui_5.pushButton_5.clicked.connect(self.close_window)
        self.ui_5.radioButton.clicked.connect(self.set_disabled)
        self.ui_5.radioButton_2.clicked.connect(self.set_enabled)
        # Radiobutton
        self.ui_5.radioButton.setChecked(True)
        self.ui_5.dateEdit.setEnabled(False)
        # DateEdit
        self.ui_5.dateEdit.setCalendarPopup(True)
        self.ui_5.dateEdit.setDate(datetime.datetime.now())
        self.ui_5.dateEdit.setDisplayFormat("dd-MM-yyyy")
        # Текст по окну
        self.setWindowTitle('Просмотр пациентов в базе')
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        set_text(self.ui_5.label, 'Выберите дату')
        set_text(self.ui_5.pushButton, 'Просмотр')
        self.ui_5.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        set_text(self.ui_5.pushButton_2, 'Отмена')
        self.ui_5.pushButton_2.setStyleSheet("""
                                             background-color: #f7c8c8;
                                             """)
        set_text(self.ui_5.pushButton_3, 'Удалить из базы запись о пациенте')
        self.ui_5.pushButton_3.setStyleSheet("""
                                             background-color: #c48989;
                                             """)
        set_text(self.ui_5.pushButton_4, 'Поиск')
        self.ui_5.pushButton_4.setStyleSheet("""
                                             background-color: #d6dfff;
                                             """)
        set_text(self.ui_5.pushButton_5, 'ОК')
        self.ui_5.pushButton_5.setStyleSheet("""
                                             background-color: #d6dfff;
                                             """)
        set_text(self.ui_5.radioButton, 'Все записи')
        set_text(self.ui_5.radioButton_2, 'По дате')

    def set_enabled(self):
        self.ui_5.dateEdit.setEnabled(True)

    def set_disabled(self):
        self.ui_5.dateEdit.setEnabled(False)

    def show_error_window(self, error):
        label = self.ui_7.findChildren(QLabel)

        for item in label:
            item.setText(error)

        self.ui_7.show()

    def close_window(self):
        self.close()

    def delete_patient(self):
        patient = self.get_patient_for_change()

        if patient:
            patient = patient.split('\n')
            patient = patient[0][4:]

            delete_patient(patient)
            self.search_result()
        else:
            self.show_error_window('Выберите пациента')

    def get_patient_for_change(self):
        return self.ui_5.listView.currentIndex().data()

    def search_result(self):
        self.ui_5.listView.setEnabled(True)
        self.ui_5.listView.setStyleSheet("""
                                         background-color: #fff;
                                         """)
        date = self.ui_5.dateEdit.text()

        if self.ui_5.radioButton.isChecked():
            patients = find_all_patients()
        else:
            patients = find_patients(date)

        patients = sorted(patients, reverse=True)
        patients_list = []

        for el in range(len(patients)):
            if patients[el][5] == 0:
                patients_list.append(f'id: {str(patients[el][0])}\n'
                                     f'Фамилия: {str(patients[el][1])}\n'
                                     f'Имя: {str(patients[el][2])}\n'
                                     f'Отчество: {str(patients[el][3])}\n'
                                     f'Дата рождения: {str(patients[el][4])}\n'
                                     f'Статус: Не отправлен\n')
            elif patients[el][5] == 1:
                patients_list.append(f'id: {str(patients[el][0])}\n'
                                     f'Фамилия: {str(patients[el][1])}\n'
                                     f'Имя: {str(patients[el][2])}\n'
                                     f'Отчество: {str(patients[el][3])}\n'
                                     f'Дата рождения: {str(patients[el][4])}\n'
                                     f'Статус: Отправлен\n')

        # Добавление списка в listView
        self.model.setStringList(patients_list)
        self.ui_5.listView.setModel(self.model)

    def show_change_window(self):
        patient = self.get_patient_for_change()

        if patient:
            patient = patient.split('\n')

            line_edits = self.ui_2.findChildren(QLineEdit)
            combo_boxes = self.ui_2.findChildren(QComboBox)

            patient_id = patient[0][4:]
            patient_surname = patient[1][9:]
            patient_name = patient[2][5:]
            patient_patronymic = patient[3][10:]
            patient_bd = patient[4][15:]

            patient_info = find_patient_info(patient_id, patient_surname, patient_name,
                                             patient_patronymic, patient_bd)
            box_info = find_patient_combobox_info(patient_id, patient_surname, patient_name,
                                                  patient_patronymic, patient_bd)

            flag = 0
            for item in line_edits:
                item.setText(str(patient_info[0][flag]))
                flag += 1

            flag = 0
            for box in combo_boxes:
                box.setCurrentText(str(box_info[0][flag]))

            self.ui_2.show()
        else:
            self.show_error_window('Выберите пациента')
