import sqlite3
import hashlib

connect = sqlite3.connect('patients.db')
cursor = connect.cursor()


# Создание таблицы (запрос из самого файла base)
def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS patients(userid INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,
                   organization_name TEXT, organization_ogrn TEXT, order_date TEXT,
                   service_code TEXT, service_name TEXT, test_system TEXT,
                   biomaterial_date TEXT, ready_date TEXT, result INT, service_type INT, result_value INT,
                   patient_surname TEXT, patient_name TEXT, patient_patronymic TEXT, patient_gender INT,
                   patient_birthday TEXT, patient_phone TEXT, patient_email TEXT, patient_document_type TEXT,
                   patient_document_serial TEXT, patient_document_number TEXT, patient_snils TEXT, patient_oms TEXT,
                   registration_town TEXT, registration_house TEXT, registration_region TEXT, registration_building TEXT,
                   registration_district TEXT, registration_apartment TEXT, registration_street TEXT, fact_town TEXT,
                   fact_house TEXT, fact_region TEXT, fact_building TEXT, fact_district TEXT, fact_apartment TEXT,
                   fact_street TEXT)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, 
                   password TEXT)
    """)


# Добавление колонки (запрос из самого файла base)
def add_column():
    cursor.execute("alter table patients add column 'success' 'INT'")


# Добавление из формы в базу (Запрос из приложения)
def from_tuple_to_patients_table(patient_tuple):
    cursor.execute("INSERT INTO patients(date, organization_name, organization_ogrn, order_date, service_code,"
                   "service_name, test_system, biomaterial_date, ready_date, result, service_type, result_value,"
                   "patient_surname, patient_name, patient_patronymic, patient_gender, patient_birthday, patient_phone,"
                   "patient_email, patient_document_type, patient_document_serial, patient_document_number,"
                   "patient_snils, patient_oms, registration_town, registration_house, registration_region,"
                   "registration_building, registration_district, registration_apartment, registration_street,"
                   "fact_town, fact_house, fact_region, fact_building, fact_district, fact_apartment, fact_street,"
                   "success)"
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
                   "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", patient_tuple)

    connect.commit()


# Добавление отметки об отправке пациента (Запрос из приложения)
def success(patient_id, data):
    sql = """UPDATE patients SET success = ? WHERE userid = ?"""
    cursor.execute(sql, (data, patient_id,))

    connect.commit()


# Создание пользователя (Запрос из файда base)
def create_user(login, password):
    password = password.encode()
    salt = 'fbuz'.encode()
    pw_hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

    users = [(login, pw_hash.hex())]
    cursor.executemany("INSERT INTO users(username, password) VALUES (?, ?);", users)

    connect.commit()


# Поиск для логина и пароля
def read_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Поиск всех пациентов по дате
def find_transfers_date():
    cursor.execute("SELECT date FROM patients")
    return cursor.fetchall()


# Поиск ФИО пациентов по определенной дате
def find_patients(date):
    sql_select_query = """select patient_surname, patient_name, patient_patronymic from patients where date = ?"""
    cursor.execute(sql_select_query, (date,))
    return cursor.fetchall()


# Поиск всех не отправленных пациентов по дате
def find_transfer(date):
    sql_select_query = """select * from patients where success = 0 and date = ?"""
    cursor.execute(sql_select_query, (date,))
    return cursor.fetchall()


def find_patient_info(surname, name, patronymic, date):
    sql_select_query = """SELECT * FROM patients
                          WHERE patient_surname = ? and
                          patient_name = ? and
                          patient_patronymic = ? and
                          date = ?
                          """
    cursor.execute(sql_select_query, (surname, name, patronymic, date,))
    return cursor.fetchall()
