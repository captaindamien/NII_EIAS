from os import path
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from ui.open_window import Ui_OpenWindow
from form_window import FormWindow
from transfer_window import JsonsWindow
from search_window import SearchWindow
from static import set_text, set_title_font


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(522, 250)
        # Инициализация окон
        self.ui = Ui_OpenWindow()
        self.ui_2 = FormWindow()
        self.ui_3 = JsonsWindow()
        self.ui_5 = SearchWindow()
        self.ui.setupUi(self)
        # Подключение других окон
        self.init_handlers()
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle('Отправка данных в ЕИАС')
        set_text(self.ui.label, 'Внести данные пациента')
        set_title_font(self.ui.label)
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

    # Обработка нажатия для октрытия сторонних окон
    def init_handlers(self):
        self.ui.pushButton.clicked.connect(self.show_form_window)
        self.ui.pushButton_3.clicked.connect(self.show_all_jsons_window)
        self.ui.pushButton_2.clicked.connect(self.show_search_window)

    # Открытие окна конфигов
    def show_form_window(self):
        self.ui_2.show()

    def show_all_jsons_window(self):
        self.ui_3.show()

    def show_search_window(self):
        self.ui_5.show()
