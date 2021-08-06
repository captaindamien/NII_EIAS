from os import path
from PyQt5 import QtWidgets, QtGui
from static import set_text, set_title_font
from ui.error_window import Ui_ErrorWindow


class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ErrorWindow, self).__init__()
        self.setFixedSize(330, 100)
        # Инициализация окон
        self.ui_7 = Ui_ErrorWindow()
        self.ui_7.setupUi(self)
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Текст по окну
        self.setWindowTitle(' ')
        set_text(self.ui_7.label, 'Ошибка')
        set_title_font(self.ui_7.label)
