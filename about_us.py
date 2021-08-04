from os import path
from PyQt5 import QtWidgets, QtGui
from ui.about_us import Ui_AboutUs
from static import set_text, set_title_font
import configparser


class AboutUs(QtWidgets.QMainWindow):
    def __init__(self):
        super(AboutUs, self).__init__()
        self.setFixedSize(623, 190)
        # Инициализация окон
        self.ui = Ui_AboutUs()
        self.ui.setupUi(self)
        # Пути до папок
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.config_dir = path.join(path.dirname(__file__), 'config')
        # Иконка окна
        self.setWindowIcon(QtGui.QIcon(path.join(self.img_dir, 'gosuslugi_5.png')))
        # Чтение конфига
        self.config = configparser.RawConfigParser()
        self.config.read(path.join(self.config_dir, 'config.ini'), encoding='utf-8')
        self.laboratory_name = ''
        for section in self.config.sections():
            if self.config.has_section('json_data'):
                if self.config.has_option(section, 'laboratory_name'):
                    self.laboratory_name = self.config.get(section, 'laboratory_name')
        # Текст по окну
        self.setWindowTitle('О проекте')
        set_text(self.ui.label, f'Проект разработан для {self.laboratory_name}\n'
                                f'в целях передачи результатов лабораторных исследований на COVID-19 в эл. виде')
        set_title_font(self.ui.label)
        set_text(self.ui.label_3, f'Над ПО работали:\n'
                                  f'Разработчик - Карпушин Е.Ю.\n'
                                  f'Менеджер - Карпушина А.А.\n'
                                  f'QA-инженер - Карпушин А.Е.\n\n'
                                  f'По всем интересующим вас вопросам можете обращаться на эл. почту'
                                  f' - karpushin@gkres.ru')
        set_title_font(self.ui.label_3)
