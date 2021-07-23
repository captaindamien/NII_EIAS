import sqlite3

connect = sqlite3.connect('patients.db')
cursor = connect.cursor()


def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS patients(userid INTEGER PRIMARY KEY AUTOINCREMENT, organization_name TEXT,
                   organization_ogrn TEXT, order_date TEXT, service_code TEXT, service_name TEXT, test_system TEXT,
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


def from_tuple_to_patients_table(patient_tuple):
    cursor.execute("INSERT INTO patients(organization_name, organization_ogrn, order_date, service_code,"
                   "service_name, test_system, biomaterial_date, ready_date, result, service_type, result_value,"
                   "patient_surname, patient_name, patient_patronymic, patient_gender, patient_birthday, patient_phone,"
                   "patient_email, patient_document_type, patient_document_serial, patient_document_number,"
                   "patient_snils, patient_oms, registration_town, registration_house, registration_region,"
                   "registration_building, registration_district, registration_apartment, registration_street,"
                   "fact_town, fact_house, fact_region, fact_building, fact_district, fact_apartment, fact_street)"
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
                   "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", patient_tuple)

    connect.commit()


def create_user(login, password):
    users = [(login, password)]
    cursor.executemany("INSERT INTO users(username, password) VALUES (?, ?);", users)

    connect.commit()


def read_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def find_transfers_date():
    pass


def find_patients():
    pass