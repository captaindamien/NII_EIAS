from os import path
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from ui.open_window import Ui_OpenWindow
from form_window import FormWindow
from transfer_window import JsonsWindow
from search_window import SearchWindow
from about_us import AboutUs
from static import set_text, set_title_font
from base import find_transfers_date
from PyQt5.QtWidgets import QComboBox


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(521, 310)
        # Инициализация окон
        self.ui = Ui_OpenWindow()
        self.ui_2 = FormWindow()
        self.ui_3 = JsonsWindow()
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
        set_text(self.ui.label_2, 'v.1.0.0')
        set_text(self.ui.pushButton, 'Заполнение формы')
        set_text(self.ui.pushButton_4, 'Импорт из эксель файла (Не доступно)')
        self.ui.pushButton_4.setEnabled(False)
        set_text(self.ui.pushButton_2, 'Просмотреть / Изменить ранее внесенные данные')
        set_text(self.ui.pushButton_3, 'Отправить отчет в ЕИАС')
        self.ui.pushButton_3.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)
        self.ui.pushButton_3.setIcon(QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        self.ui.pushButton_3.setIconSize(QSize(35, 35))
        set_text(self.ui.pushButton_5, 'О проекте')

    # Обработка нажатия для октрытия сторонних окон
    def init_handlers(self):
        self.ui.pushButton.clicked.connect(self.show_form_window)
        self.ui.pushButton_3.clicked.connect(self.show_all_jsons_window)
        self.ui.pushButton_2.clicked.connect(self.show_search_window)
        self.ui.pushButton_5.clicked.connect(self.show_about_us)

    def show_about_us(self):
        self.ui_8.show()

    # Открытие окна конфигов
    def show_form_window(self):
        self.ui_2.show()

    def show_all_jsons_window(self):
        self.ui_3.show()

    # Добавление элементов в comboBox окна search_window и отображение его
    def show_search_window(self):
        date_list = find_transfers_date()
        combo_date_list = ['Все записи']

        for element in date_list:
            combo_date_list.append(element[0])

        combo_date_list = set(combo_date_list)

        combo_boxes = self.ui_5.findChildren(QComboBox)

        for item in combo_boxes:
            item.clear()

        for item in combo_boxes:
            for element in list(sorted(combo_date_list, reverse=True)):
                item.addItem(element)

        self.ui_5.show()
