import os
from os import path
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from ui.main_window import Ui_OpenWindow
from form_window import FormWindow
from transfer_window import TransferWindow
from search_window import SearchWindow
from about_us import AboutUs
from static import set_text, set_title_font, validator
from PyQt5.QtWidgets import QComboBox, QLineEdit, QDateEdit, QListView, QCalendarWidget, QPushButton, QProgressBar
import datetime
from excel_transfer import ExcelWindow


# Открытие .docx файла с инструкцией
def show_instructions():
    os.system(f'start {path.join(path.dirname(__file__), "README.docx")}')


# Открытие .docx файла с планами на будущее
def show_roadmap():
    os.system(f'start {path.join(path.dirname(__file__), "Roadmap.docx")}')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(521, 300)
        # Инициализация окон
        self.ui = Ui_OpenWindow()
        self.ui_2 = FormWindow()
        self.ui_3 = TransferWindow()
        self.ui_4 = ExcelWindow()
        self.ui_5 = SearchWindow()
        self.ui_8 = AboutUs()
        self.ui.setupUi(self)
        # Подключение других окон
        self.init_handlers()
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle('Отправка данных в ЕПГУ')
        set_text(self.ui.label, 'Внести данные пациента')
        set_title_font(self.ui.label)
        set_text(self.ui.label_2, 'v.1.1.0')
        set_text(self.ui.pushButton, 'Заполнение формы')
        set_text(self.ui.pushButton_4, 'Импорт из Excel')
        set_text(self.ui.pushButton_2, 'Просмотреть / Изменить данные')
        set_text(self.ui.pushButton_3, 'Отправить данные в ФБУН ЦНИИ')
        self.ui.pushButton_3.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        self.ui.pushButton_3.setIcon(QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        self.ui.pushButton_3.setIconSize(QSize(35, 35))
        set_text(self.ui.pushButton_5, 'О проекте')
        set_text(self.ui.pushButton_6, 'Экспорт в Excel (Скоро)')
        self.ui.pushButton_6.setEnabled(False)
        # set_text(self.ui.pushButton_7, 'Roadmap')
        # set_text(self.ui.pushButton_8, 'Инструкция')

    # Обработка нажатия для октрытия сторонних окон
    def init_handlers(self):
        self.ui.pushButton.clicked.connect(self.show_form_window)
        self.ui.pushButton_3.clicked.connect(self.show_transfer_window)
        self.ui.pushButton_2.clicked.connect(self.show_search_window)
        self.ui.pushButton_5.clicked.connect(self.show_about_us)
        self.ui.pushButton_4.clicked.connect(self.show_excel_window)
        # self.ui.pushButton_7.clicked.connect(show_roadmap)
        # self.ui.pushButton_8.clicked.connect(show_instructions)

    # Открытие окна excel_window
    def show_excel_window(self):
        self.ui_4.refresh()  # Собирает данные с экселя
        self.ui_4.show()

    # Открытие окна "О проекте"
    def show_about_us(self):
        self.ui_8.show()

    # Открытие окна форм
    def show_form_window(self):
        line_edits = self.ui_2.findChildren(QLineEdit)
        combo_boxes = self.ui_2.findChildren(QComboBox)
        date_edits = self.ui_2.findChildren(QDateEdit)

        # Очищение форм
        for item in line_edits:
            item.setText('')
            validator(item, '[a-zA-Z0-9_@_а-яА-Я_\s]+$')
        for box in combo_boxes:
            box.setCurrentIndex(0)
        for date in date_edits:
            date.setDate(datetime.datetime.now())

        self.ui_2.validations()
        self.ui_2.show()

    # Открытие окна transfer_window
    def show_transfer_window(self):
        self.ui_3.delete_files()

        calendar = self.ui_3.findChildren(QCalendarWidget)
        list_view = self.ui_3.findChildren(QListView)
        buttons = self.ui_3.findChildren(QPushButton)
        progress_bar = self.ui_3.findChildren(QProgressBar)

        for cal in calendar:
            cal.show()
        for lst in list_view:
            lst.hide()
        for button in buttons:
            button.setEnabled(True)
        for pb in progress_bar:
            pb.hide()

        self.ui_3.show()

    # Открытие окна просмотра / изменения
    def show_search_window(self):
        self.ui_5.show()
