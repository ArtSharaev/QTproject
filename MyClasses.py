"""
Библиотека с 5 классами, которые работают с файлами
"""

import csv
import sqlite3
from random import choice


class StringGenerator:
    """Класс-генератор рандомного куска предложения"""
    def __init__(self, file):
        self.file = file  # файл с текстом, где куча предложений

    def get(self):
        """Функция-вылавливатель рандомного предложения"""
        with open(self.file, encoding='utf-8') as text:  # открываем
            text = text.read()  # считываем
        t = text.split('. ')  # делим на предложения
        string = list(choice(t).strip() + '.')
        # рандомное предложение делим на символы
        while '\n' in string:  # убираем символы переноса строки
            string[string.index('\n')] = ' '
        if len(string) < 33:
            return ''.join(string)
        ind = 32
        while string[ind] != ' ':
            ind -= 1
        string = string[:ind]
        return ''.join(string)  # возвращаем часть предложение


class AccountWorker:
    """Класс работы с акаунтами (CSV)"""
    def __init__(self, file):
        """Подаём файл, с которым будем работать"""
        self.file = file

    def log_in(self, login, password):
        """Функция проверки наличия пользователя с этими данными"""
        with open(self.file, encoding='cp1251') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            if [login, password] in reader:  # сама проверка
                return True
            return False

    def unique_login(self, login):
        """Функция проверки уникальности логина"""
        with open(self.file, encoding='cp1251') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for account in reader:  # сама проверка
                if account[0] == login:
                    return False
            return True

    def create_account(self, login, password):
        """Функция создания аккаунта"""
        with open(self.file, 'a', newline='', encoding='cp1251') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=',', quotechar='"')
            if not self.log_in(login, password):
                # если такого пользователя еще не было
                writer.writerow([login, password])  # создаем аккаунт
                return True
            return False

    def get_all(self):
        """Функция достаёт все аккаунты из csv файла"""
        with open(self.file, encoding='cp1251') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            accounts = []
            for account in reader:  # сама проверка
                accounts.append(account)
            return accounts


class FileWorker:
    """Класс для работы с файлом"""
    def __init__(self, file):
        self.file = file

    def get(self):
        with open(self.file, encoding='utf-8') as text:  # открываем
            if self.file == 'current-theme.txt':
                theme = text.read()[0]
                return theme
            elif self.file == 'current-account.txt':
                line = text.readline()
                if line == '':
                    return False  # достаем
                return line.split(' ')

    def set(self, value):
        with open(self.file, 'w', encoding='utf-8') as text:  # открываем
            text.write(value)  # записываем


class StatisticWorker:
    """Класс для работы со статистиками (SQL)"""
    def __init__(self, file):
        self.file = file

    def add_statistic(self, login, password, best_score, medium_score,
                      total_time, total_sym_count):
        """Функия добавляет аккаунт и статистику в БД"""
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        cur.execute(f"""
            INSERT INTO accounts(account) VALUES ('{login + password}')""")
        cur.execute(f"""
                INSERT INTO statistics(best_score, medium_score, total_time,
                total_sym_count)
                VALUES ({best_score}, {medium_score},
                          {total_time}, {total_sym_count})""")
        con.commit()
        con.close()

    def change_statistic(self, login, password, best_score, medium_score,
                         total_time, total_sym_count):
        """Функция обновления статистики"""
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        id = cur.execute(f"""SELECT account_id FROM accounts
        WHERE account='{login + password}'""").fetchall()
        id = id[0][0]
        cur.execute(f"""
        UPDATE statistics
        SET best_score = {best_score}, medium_score = {medium_score}, total_time = {total_time}, total_sym_count = {total_sym_count}
        WHERE id = {id}
        """)
        con.commit()
        con.close()

    def get_statistic(self, login, password):
        """Функция получения статистики какого-то аккаунта"""
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        id = cur.execute(f"""SELECT account_id FROM accounts
            WHERE account='{login + password}'""").fetchall()
        id = id[0][0]
        arr = cur.execute(f"""
        SELECT * FROM statistics
            WHERE id = {id}
        """).fetchall()
        ok = []
        for elem in arr[0]:
            ok.append(elem)
        con.close()
        return ok[1:]


def dict_sorting(dictionary, cutoff=False, isreversed=False):
    """Функция сортировки словарей"""
    arr = sorted(dictionary, key=lambda x: dictionary[x])
    if isreversed:  # развернуть словарь
        arr.reverse()
    if cutoff:  # срез
        arr = arr[:cutoff]
    d = dict()  # словарь на выходе
    for elem in arr:
        d[elem] = dictionary[elem]
    return d
