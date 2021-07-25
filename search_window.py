from os import path
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
from ui.search_window import Ui_SearchWindow
from base import find_transfers_date, find_patients, find_patient_info
from static import set_text, set_title_font
from form_window import FormWindow


class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setFixedSize(362, 410)
        # Инициализация окон
        self.ui_5 = Ui_SearchWindow()
        self.ui_2 = FormWindow()
        self.ui_5.setupUi(self)
        self.add_combobox()
        # Модель для listView
        self.model = QtCore.QStringListModel(self)
        self.ui_5.listView.setEnabled(False)
        self.ui_5.listView.setStyleSheet("""
                                         background-color: #e0e0e0;
                                         """)
        # Подключение кнопок
        self.ui_5.pushButton_4.clicked.connect(self.search_result)
        self.ui_5.pushButton_2.clicked.connect(self.close_window)
        self.ui_5.pushButton.clicked.connect(self.show_form_window)
        # Текст по окну
        set_text(self.ui_5.label, 'Выберите дату')
        set_text(self.ui_5.pushButton_4, 'Поиск')
        self.ui_5.pushButton_4.setStyleSheet("""
                                             background-color: #d6dfff;
                                             """)
        set_text(self.ui_5.pushButton, 'Просмотр')
        self.ui_5.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        set_text(self.ui_5.pushButton_2, 'Отмена')
        self.ui_5.pushButton_2.setStyleSheet("""
                                             background-color: #f7c8c8;
                                             """)

    def show_form_window(self):
        patient = self.get_patient_for_change()
        patient = patient.split(' ')
        date = self.ui_5.comboBox.currentText()
        patient_info = find_patient_info(patient[0], patient[1], patient[2], date)
        line_edits = self.ui_2.findChildren(QLineEdit)

        self.ui_2.show()
        print(patient_info[0])
        for item in line_edits:
            for element in patient_info[0]:
                item.setText(element[3])
            break

    def close_window(self):
        self.close()

    def get_patient_for_change(self):
        return self.ui_5.listView.currentIndex().data()

    def add_combobox(self):
        date_list = find_transfers_date()
        combo_date_list = []

        for element in date_list:
            combo_date_list.append(element[0])

        for element in list(set(combo_date_list)):
            self.ui_5.comboBox.addItem(element)

    def search_result(self):
        self.ui_5.listView.setEnabled(True)
        self.ui_5.listView.setStyleSheet("""
                                             background-color: #fff;
                                             """)
        patients = find_patients(self.ui_5.comboBox.currentText())
        print(patients)
        patients_list = []
        for el in range(len(patients)):
            patients_list.append(f'{str(patients[el][0])} {str(patients[el][1])} {str(patients[el][2])}')
        print(patients_list)
        # Добавление списка в listView
        self.model.setStringList(patients_list)
        self.ui_5.listView.setModel(self.model)
