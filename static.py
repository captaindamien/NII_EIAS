import datetime
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator


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
