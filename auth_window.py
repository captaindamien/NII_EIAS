import sys
from os import path
from base import read_users
from main import MainWindow
from static import set_text, set_title_font
from PyQt5 import QtWidgets, QtGui
from ui.auth_window import Ui_AuthWindow
import hashlib


class AuthWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AuthWindow, self).__init__()
        self.setFixedSize(282, 201)
        # Инициализация окон
        self.ui_4 = Ui_AuthWindow()
        self.ui_4.setupUi(self)
        self.ui = MainWindow()
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Подключение кнопок
        self.ui_4.pushButton.clicked.connect(self.user_auth)
        # Подключение нажатия Enter
        self.ui_4.pushButton.setAutoDefault(True)
        self.ui_4.lineEdit.returnPressed.connect(self.ui_4.pushButton.click)
        self.ui_4.lineEdit_2.returnPressed.connect(self.ui_4.pushButton.click)
        # Отображение звездочек для ввода пароля
        self.ui_4.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # Текст по окну
        self.setWindowTitle('Авторизация')
        set_text(self.ui_4.label, 'Введите имя пользователя')
        set_text(self.ui_4.label_2, 'Введите пароль')
        set_text(self.ui_4.label_3, '')
        set_title_font(self.ui_4.label_3)
        set_text(self.ui_4.pushButton, 'Вход')
        self.ui_4.pushButton.setStyleSheet("""
                                           background-color: #b2edbf;
                                           """)

    # Отображение основного окна
    def show_main_window(self):
        self.ui.show()
        self.close()

    # Отработка авторизации пользователя
    def user_auth(self):
        # Чтение данных из таблицы users
        all_users = read_users()
        username = self.ui_4.lineEdit.text()
        password = self.ui_4.lineEdit_2.text()

        # Делает хеш из введенных данных
        password = password.encode()
        salt = 'fbuz'.encode()
        pw_hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

        # Проверка логина и хеша пароля с базой
        for base_row in all_users:
            if username == base_row[1] and pw_hash.hex() == base_row[2]:
                self.show_main_window()
                break
        else:
            set_text(self.ui_4.label_3, 'Неверный логин или пароль')
            self.ui_4.label_3.setStyleSheet("""
                                            color: #ed1818;
                                            """)


app = QtWidgets.QApplication([])
# Оформление всего приложения
app.setStyle('Fusion')
application = AuthWindow()
application.show()

sys.exit(app.exec())
