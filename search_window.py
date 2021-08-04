from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QComboBox
from ui.search_window import Ui_SearchWindow
from base import find_transfers_date, find_patients, find_patient_info, find_patient_combobox_info
from static import set_text
from change_window import ChangeWindow


class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setFixedSize(362, 410)
        # Инициализация окон
        self.ui_5 = Ui_SearchWindow()
        self.ui_2 = ChangeWindow()
        self.ui_5.setupUi(self)
        self.add_combobox()
        # Модель для listView
        self.model = QtCore.QStringListModel(self)
        self.ui_5.listView.setEnabled(False)
        self.ui_5.listView.setWordWrap(True)
        self.ui_5.listView.setStyleSheet("""
                                         background-color: #e0e0e0;
                                         """)
        # Подключение кнопок
        self.ui_5.pushButton_4.clicked.connect(self.search_result)
        self.ui_5.pushButton_2.clicked.connect(self.close_window)
        self.ui_5.pushButton.clicked.connect(self.show_change_window)
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

    def show_change_window(self):
        self.ui_2.show()

        patient = self.get_patient_for_change()
        patient = patient.split('\n')

        line_edits = self.ui_2.findChildren(QLineEdit)
        combo_boxes = self.ui_2.findChildren(QComboBox)
        date = self.ui_5.comboBox.currentText()

        patient_info = find_patient_info(patient[0], patient[1], patient[2], patient[3], date)
        box_info = find_patient_combobox_info(patient[0], patient[1], patient[2], patient[3], date)

        flag = 0
        for item in line_edits:
            item.setText(str(patient_info[0][flag]))
            flag += 1

        flag = 0
        for box in combo_boxes:
            box.setCurrentText(str(box_info[0][flag]))

    def close_window(self):
        self.close()

    def get_patient_for_change(self):
        return self.ui_5.listView.currentIndex().data()

    def add_combobox(self):
        date_list = find_transfers_date()
        combo_date_list = ['Все записи']

        for element in date_list:
            combo_date_list.append(element[0])

        combo_date_list = set(combo_date_list)

        for element in list(sorted(combo_date_list, reverse=True)):
            self.ui_5.comboBox.addItem(element)

    def search_result(self):
        self.ui_5.listView.setEnabled(True)
        self.ui_5.listView.setStyleSheet("""
                                             background-color: #fff;
                                             """)
        patients = find_patients(self.ui_5.comboBox.currentText())

        patients_list = []
        for el in range(len(patients)):
            patients_list.append(f'{str(patients[el][0])}\n'
                                 f'{str(patients[el][1])}\n'
                                 f'{str(patients[el][2])}\n'
                                 f'{str(patients[el][3])}\n')
        # Добавление списка в listView
        self.model.setStringList(patients_list)
        self.ui_5.listView.setModel(self.model)
