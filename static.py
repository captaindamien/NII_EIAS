import datetime
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
import configparser
from os import path
from random import randint

config_dir = path.join(path.dirname(__file__), 'config')
config = configparser.RawConfigParser()
config.read(path.join(config_dir, 'config.ini'), encoding='utf-8')


def set_text(form, text):
    form.setText(text)


def set_title_font(form):
    form.setAlignment(Qt.AlignCenter)
    form.setStyleSheet("""
                       font-weight: 900;
                       """)


def set_date_format(form):
    form.setCalendarPopup(True)
    form.setDate(datetime.datetime.now())
    form.setDisplayFormat("yyyy-MM-dd")


def validator(form, form_range):
    serial_regex = QRegExp("^" + form_range)
    serial_validator = QRegExpValidator(serial_regex)
    form.setValidator(serial_validator)


def get_organization():
    for section in config.sections():
        if config.has_section('organization_data'):
            if config.has_option(section, 'name'):
                name = config.get(section, 'name')
                return name


def generate_unique_number():
    name = get_organization()
    rand_int = randint(1, 9)
    return f'{name}-{datetime.datetime.now().strftime("%d-%m,%H-%M-%S")}-{rand_int}{rand_int}{rand_int}'


def generate_filename():
    name = get_organization()
    return f'{name}-{datetime.datetime.now().strftime("%d-%m-%Y")}'
