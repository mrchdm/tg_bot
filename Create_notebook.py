import csv
import os.path

list_header = ['Имя', 'Фамилия', 'Номер телефона']

def create_list():
    if not os.path.exists('notebook.csv'):
        with open('notebook.csv', 'w', encoding='utf-8') as el:
            writer = csv.writer(el, delimiter=';')
            writer.writerow(list_header)