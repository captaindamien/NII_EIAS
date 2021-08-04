from os import path
import os

a = 'Z:\\!База\\1 Системы\\Сетевой комплекс\\8. ОЛА\\Схемы Ола\\Схемы от Киреева 25.06.2020'
b = 'Z:\\!База\\1 Системы\\Сетевой комплекс\\8. ОЛА\\Схемы Ола\\reestr.txt'
files = os.listdir(a)
print(files)

with open(b, 'w', encoding='utf-8') as file:
    for element in files:
        file.write(f'{element[:-4]}\n')
