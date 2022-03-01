from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QLineEdit, QRadioButton, QComboBox

from MyClasses import *
from stylesheets import *

# из файла functions достаём все классы
# генератор частей предложений
SGenerator = StringGenerator('text.txt')
# класс работы с акаунтами (CSV)
AccWorker = AccountWorker('accounts.csv')
# класс для работы с темами (txt)
TWorker = FileWorker('current-theme.txt')
# класс для работы с аккаунтом (txt)
AWorker = FileWorker('current-account.txt')
# класс для работы со статистиками (SQL)
SWorker = StatisticWorker("acc-statistics.db")


class MainWindow(QWidget):
    """Класс для главного окна"""

    def __init__(self):
        """Создаём красоту"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Рисуем GUI"""
        # ВСЕ КНОПКИ РАЗНЫЕ, ПОЭТОМУ МНОГО КОПИПАСТЫ
        # заканчиваем с фоном
        self.move(300, 200)
        # координаты от балды, нужны, чтобы окно создавалось на левом мониторе
        self.setWindowTitle('PrintSpeedTest')
        self.all_open_windows = [self]  # список всех открвытых окон
        # главный текст-виджет
        self.main_label = QLabel(self)
        self.main_label.setGeometry(330, 100, 1200, 120)
        self.main_label.setText('Тест скорости набора текста')
        self.main_label.setFont(QtGui.QFont('comic sans ms', 60))
        self.main_label.setAlignment(Qt.AlignCenter)
        # текст-виджет для помощи пользователю
        self.help_label = QLabel(self)
        self.help_label.setGeometry(735, 350, 400, 60)
        self.help_label.setText(' Здравствуйте!')
        self.help_label.setAlignment(Qt.AlignCenter)
        self.help_label.setFont(QtGui.QFont('comic sans ms', 30))
        # поле ввода логина
        self.login_input = QLineEdit(self)
        self.login_input.setGeometry(730, 460, 400, 60)
        self.login_input.setFont(QtGui.QFont('comic sans ms', 30))
        self.login_input.setPlaceholderText('Введите логин')
        self.login_input.setAlignment(Qt.AlignCenter)
        # поле ввода пароля
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(730, 560, 400, 60)
        self.password_input.setFont(QtGui.QFont('comic sans ms', 30))
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setAlignment(Qt.AlignCenter)
        # кнопка войти
        self.enter_account_button = QPushButton(self)
        self.enter_account_button.setGeometry(730, 660, 400, 60)
        self.enter_account_button.setText('Войти!')
        self.enter_account_button.setFont(QtGui.QFont('comic sans ms', 30))
        self.enter_account_button.clicked.connect(self.enter_account)
        #   _________________
        # | Что ты тут забыл? |
        #   =================
        #                       \
        #                        \
        #                         \
        #                          .--.
        #                         |o_o |
        #                         |:_/ |
        #                        //   \ \
        #                       (|     | )
        #                      /'\_   _/`\
        #                      \___)=(___/
        # кнопка зарегистрироваться
        self.create_account_button = QPushButton(self)
        self.create_account_button.setGeometry(730, 760, 400, 60)
        self.create_account_button.setText('Создать аккаунт!')
        self.create_account_button.setFont(QtGui.QFont('comic sans ms', 30))
        self.create_account_button.clicked.connect(self.create_account)
        # текст-виджет для показа ошибки
        self.error_label = QLabel(self)
        self.error_label.setGeometry(730, 860, 400, 120)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setFont(QtGui.QFont('comic sans ms', 30))
        # кнопка генерации предложения
        self.generate_button = QPushButton(self)
        self.generate_button.setGeometry(430, 790, 1000, 90)
        self.generate_button.setText('Начать!')
        self.generate_button.setFont(QtGui.QFont('comic sans ms', 45))
        self.generate_button.clicked.connect(self.start)
        # коробка выбора времени
        self.time_choice_box = QComboBox(self)
        self.time_choice_box.setGeometry(1550, 20, 350, 90)
        self.time_choice_box.setFont(QtGui.QFont('comic sans ms', 45))
        self.time_choice_box.addItems(['30 секунд', '1 минута', '2 минуты',
                                       '3 минуты', '5 минут'])
        self.time_choice_box.activated[str].connect(self.time_box_choice)
        # таймер для обратного отсчёта 1
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_time1)
        # таймер для обратного отсчёта 2
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_time2)
        # поле ввода предложения
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(330, 500, 1200, 90)
        self.text_input.setFont(QtGui.QFont('comic sans ms', 45))
        # текст-виджет для предложений
        self.string_label = QLabel(self)
        self.string_label.setGeometry(330, 300, 1200, 60)
        self.string_label.setAlignment(Qt.AlignCenter)
        self.string_label.setFont(QtGui.QFont('comic sans ms', 30))
        # кнопка настроек
        self.settings_button = QPushButton(self)
        self.settings_button.setGeometry(1625, 950, 230, 60)
        self.settings_button.setText('Настройки')
        self.settings_button.setFont(QtGui.QFont('comic sans ms', 30))
        self.settings_button.clicked.connect(self.show_settings)
        # кнопка выхода из аккаунта
        self.exit_button = QPushButton(self)
        self.exit_button.setGeometry(50, 950, 230, 60)
        self.exit_button.setText('Выйти')
        self.exit_button.setFont(QtGui.QFont('comic sans ms', 30))
        self.exit_button.clicked.connect(self.first_configuration)
        # кнопка зала славы
        self.hof_button = QPushButton(self)
        self.hof_button.setGeometry(50, 950, 230, 60)
        self.hof_button.setText('Зал славы')
        self.hof_button.setFont(QtGui.QFont('comic sans ms', 30))
        self.hof_button.clicked.connect(self.show_hall_of_frame)
        # картинка компа
        self.computer_pixmap = QPixmap('computer.png')
        self.computer_image = QLabel(self)
        self.computer_image.setGeometry(50, 80, 300, 200)
        self.computer_image.setPixmap(self.computer_pixmap)
        # добавляем красоты - стайлщиты
        if TWorker.get() == 'l':  # светлая
            self.setStyleSheet(light_main_window_stylesheet)
        elif TWorker.get() == 'd':  # тёмная
            self.setStyleSheet(dark_main_window_stylesheet)
        self.enter_account_button.setStyleSheet(buttons_stylesheet)
        self.create_account_button.setStyleSheet(buttons_stylesheet)
        self.error_label.setStyleSheet(error_stylesheet)
        self.generate_button.setStyleSheet(buttons_stylesheet)
        self.string_label.setStyleSheet(string_label_stylesheet)
        self.settings_button.setStyleSheet(buttons_stylesheet)
        self.exit_button.setStyleSheet(danger_buttons_stylesheet)
        self.time_choice_box.setStyleSheet(combobox_stylesheet)
        self.hof_button.setStyleSheet(buttons_stylesheet)
        if AWorker.get():  # если пароль и логин уже есть
            self.LOGIN, self.PASSWORD = AWorker.get()[0], AWorker.get()[1]
            self.second_configuration()
        else:
            self.first_configuration()

    def enter_account(self):
        """Войти - привязка к кнопке"""
        login = self.login_input.text()
        password = self.password_input.text()
        if AccWorker.log_in(login, password):
            # ↑ если данные прошли все проверки
            self.LOGIN = login
            self.PASSWORD = password
            self.second_configuration()  # вторая конфигурация окна
            AWorker.set(login + ' ' + password)
            # ↑ запоминаем текущие данные
        else:
            self.error_label.setText('Неверные логин\nили пароль')

    def create_account(self):
        """Создать аккаунт - привязка к кнопке"""
        login = self.login_input.text()
        password = self.password_input.text()
        # проверки формата логина и пароля
        if login == '' or password == '':
            self.error_label.setText('Пустой логин\nили пароль')
        elif ' ' in login or ' ' in password:
            self.error_label.setText('Пробел в логине\nили в пароле')
        elif not AccWorker.unique_login(login):  # проверка уникальности логина
            self.error_label.setText('Этот логин\nуже занят')
        else:
            if AccWorker.create_account(login, password):
                # ↑ если данные прошли все проверки
                self.LOGIN = login
                self.PASSWORD = password
                self.second_configuration()  # вторая конфигурация окна
                AWorker.set(login + ' ' + password)
                # ↑ запоминаем текущие данные
                SWorker.add_statistic(self.LOGIN, self.PASSWORD,
                                      0, 0, 0, 0)  # добавляем статистику в БД
            else:
                self.error_label.setText('Такой пользователь\nуже существует')

    def time_box_choice(self, time):
        """Функция засекает таймер step2 в соответствии с установленным
        временем"""
        if time == '30 секунд':
            self.step2 = 30
        elif time == '1 минута':
            self.step2 = 60
        elif time == '2 минуты':
            self.step2 = 120
        elif time == '3 минуты':
            self.step2 = 180
        elif time == '5 минут':
            self.step2 = 300
        self.last_step2 = self.step2
        # так как step2 будет уменьшаться, создаём переменную,
        # запоминающую предыдущее значение

    def generate_string(self):
        """Функция генерирует преложение и воводит его на экран"""
        self.string = SGenerator.get()
        self.string_label.setText(self.string)

    def start(self):
        """Привязка к кнопке начать"""
        self.sym_count = 0  # обнуляем счётчик набранных символов
        self.generate_button.setEnabled(False)
        self.settings_button.setEnabled(False)
        self.time_choice_box.setEnabled(False)
        self.exit_button.setEnabled(False)
        self.text_input.clear()
        # ↑ кнопки становится некликабельными, поле ввода текста очищается
        self.step1 = 3
        self.main_label.setText('3')
        self.timer1.start(1000)
        # ↑ запускаем первый таймер для обратного отсчёта передначалом теста
        self.text_input.textChanged.connect(self.check_string)
        # ↑ подключаем изменения в поле ввода к обработчику

    def check_string(self):
        """Функция для проверки совпадения текста с
        предложением и отлавливания ошибок"""
        text = self.text_input.text()
        text_len = len(text)
        if self.string[:text_len] != text:  # если пользователь допустил ошибку
            self.text_input.setStyleSheet(error_stylesheet)
        if self.string[:text_len] == text:  # если все правильно
            self.sym_count += 1
            if TWorker.get() == 'l':  # светлая
                self.text_input.setStyleSheet(light_main_window_stylesheet)
            elif TWorker.get() == 'd':  # тёмная
                self.text_input.setStyleSheet(dark_main_window_stylesheet)
            if self.string == text:  # если пользователь написал до конца
                self.text_input.clear()  # очистка
                self.generate_string()  # генерируем новое предложение

    def update_time1(self):
        """Функция обатного отсчета для 1 таймера"""
        self.step1 -= 1  # минус одна секунда
        self.main_label.setText(str(self.step1))  # выводим оставшееся время
        if self.step1 == 0:  # вместо нуля выводим старт
            self.main_label.setText('Старт!')
        if self.step1 < 0:  # отсчет окончен
            self.timer1.stop()  # останавливаем первый таймер
            self.generate_string()  # генерируем новое предложение
            try:
                self.main_label.setText(str(self.step2))
            except AttributeError:
                self.step2 = 30
                self.last_step2 = 30
                self.main_label.setText(str(self.step2))
            # ↑ заводим таймер в соответствии с временем из комбобокса,
            # в противном случае ставим 30 сек
            self.string_label.show()  # виджет с текстом для печати
            self.timer2.start(1000)  # запускаем второй таймер

    def update_time2(self):
        """Функция обатного отсчета для 2 таймера"""
        self.step2 -= 1  # минус одна секунда
        self.main_label.setText(str(self.step2))  # выводим оставшееся время
        if self.step2 == 0:
            self.timer2.stop()  # останавливаем второй таймер
            self.main_label.setText('Тест скорости набора текста')
            self.generate_button.setEnabled(True)
            self.settings_button.setEnabled(True)
            self.time_choice_box.setEnabled(True)
            self.exit_button.setEnabled(True)
            # текст становится некликабельным, кнопки - наоборот
            self.text_input.clear()  # очистка текста
            self.string_label.hide()  # прячем текст-виджет
            self.step2 = self.last_step2  # взводим таймер
            score = str(self.sym_count / self.step2)  # вычисляыем счёт
            if len(score) > 5:
                score = score[:5]
            score = float(score)
            # ↑ обрезаем до 10 знаков после запятой
            arr = SWorker.get_statistic(self.LOGIN, self.PASSWORD)
            # ↑ добываем старую статистику
            best_score = arr[0]
            if score > best_score:
                best_score = score
            # ↑ подсчитываем лучший счёт
            # ↓ обновляем суммарное время
            total_time = arr[2] + self.step2
            # ↓ обновляем общий счетчик символов
            total_sym_count = arr[3] + self.sym_count
            # ↓ заново высчитываем средний результат по аккаунту
            medium_score = str((self.sym_count + total_sym_count)
                               / (total_time + self.step2))
            # ↓ обрезаем до 10 знаков после запятой
            if len(medium_score) > 5:
                medium_score = medium_score[:5]
            medium_score = float(medium_score)
            # ↓ обновляем статистику
            SWorker.change_statistic(self.LOGIN, self.PASSWORD,
                                     best_score, medium_score,
                                     total_time, total_sym_count)
            # ↓ создаем окно статистики
            self.show_statistic(score)

    def show_statistic(self, score):
        """Фунцкия создает окно статистики"""
        try:
            self.all_open_windows.remove(self.statistic_window)
            # пробуем удалить предыдущую копию этого окна
            self.statistic_window.destroy()
        except AttributeError:
            print('Окно статистики создано!')
        arr = SWorker.get_statistic(self.LOGIN, self.PASSWORD)
        # ↑ добываем статистику
        self.statistic_window = StatisticWindow(arr[0], score, arr[1], arr[2],
                                                self.sym_count, self.step2,
                                                arr[3])
        self.statistic_window.show()
        # ↑ создам окно статистики
        self.all_open_windows.append(self.statistic_window)

    def show_settings(self):
        """Фунцкия создает окно настроек"""
        try:
            self.all_open_windows.remove(self.settings_window)
            # пробуем удалить предыдущую копию этого окна
            self.settings_window.destroy()
        except AttributeError:
            print('Окно настроек создано!')
        self.settings_window = SettingsWindow(self.all_open_windows)
        self.settings_window.show()
        self.all_open_windows.append(self.settings_window)

    def show_hall_of_frame(self):
        """Фунцкия создает окно зала славы"""
        try:
            self.all_open_windows.remove(self.hof_window)
            # пробуем удалить предыдущую копию этого окна
            self.hof_window.destroy()
        except AttributeError:
            print('Окно зала славы создано!')
        except ValueError:
            print('Окно зала славы создано!')
        accounts = AccWorker.get_all()  # список списков паролей и аккаунтов :)
        best_dict = dict()  # словарь для логинов + лучших счетов
        medium_dict = dict()  # словарь для логинов + лучших средних счетов
        for account in accounts:
            login = account[0]
            s = SWorker.get_statistic(login, account[1])  # добываем статистику
            best_score = s[1]
            medium_score = s[0]
            best_dict[login] = best_score
            medium_dict[login] = medium_score
        best_dict = dict_sorting(best_dict, cutoff=10, isreversed=True)
        medium_dict = dict_sorting(medium_dict, cutoff=10, isreversed=True)
        # ↑ манипуляции на строках 346-357 призваны создать два словаря
        # из средних и лучших счётов в обратном алфавитном порядке
        self.hof_window = HallOfFrameWindow(best_dict, medium_dict)
        self.hof_window.show()
        self.all_open_windows.append(self.hof_window)

    def first_configuration(self):
        """Окно до входа в аккаунт"""
        AWorker.set('')  # обнуляем предыдущий вход
        self.main_label.move(330, 100)  # слегка опускаем главный текст-виджет
        self.help_label.setGeometry(735, 350, 400, 60)
        self.help_label.setText(' Здравствуйте!')
        # прячем ненужные виджеты
        self.generate_button.hide()
        self.text_input.hide()
        self.string_label.hide()
        self.time_choice_box.hide()
        self.exit_button.hide()
        self.computer_image.hide()
        # показываем нужные виджеты
        self.hof_button.show()
        self.login_input.show()
        self.password_input.show()
        self.enter_account_button.show()
        self.create_account_button.show()
        self.error_label.show()
        # убираем возможный сообщения об ошибке
        self.error_label.setText('')

    def second_configuration(self):
        """Окно после входа в аккаунт"""
        self.main_label.move(330, 50)  # слегка поднимаем главный текст-виджет
        self.help_label.setGeometry(330, 200, 1200, 60)
        self.help_label.setText(
            'Переписывайте части предложений как можно скорее!')
        # прячем ненужные виджеты
        self.login_input.hide()
        self.password_input.hide()
        self.enter_account_button.hide()
        self.create_account_button.hide()
        self.error_label.hide()
        self.hof_button.hide()
        # показываем нужные виджеты
        self.computer_image.show()
        self.exit_button.show()
        self.generate_button.show()
        self.text_input.show()
        self.string_label.show()
        self.time_choice_box.show()


class SettingsWindow(QWidget):
    """Класс для окна настроек"""

    def __init__(self, windows):
        """Создаём красоту"""
        super().__init__()
        self.windows = windows
        self.initUI()

    def initUI(self):
        """Рисуем GUI"""
        # заканчиваем с фоном
        self.move(300, 200)  # координаты от балды
        self.setFixedSize(450, 500)
        self.setWindowTitle('Настройки')
        # текст-виджет для выбора тем
        self.theme_label = QLabel(self)
        self.theme_label.setGeometry(-50, 15, 200, 40)
        self.theme_label.setAlignment(Qt.AlignCenter)
        self.theme_label.setFont(QtGui.QFont('comic sans ms', 20))
        self.theme_label.setText('Тема')
        # кнопка тёмной темы
        self.rb_dark = QRadioButton(self)
        self.rb_dark.setGeometry(120, 15, 140, 40)
        self.rb_dark.setText('Тёмная')
        self.rb_dark.setFont(QtGui.QFont('comic sans ms', 20))
        self.rb_dark.clicked.connect(lambda slate, t='d': self.setTheme(t))
        # кнопка светлой темы
        self.rb_light = QRadioButton(self)
        self.rb_light.setGeometry(290, 15, 140, 40)
        self.rb_light.setText('Светлая')
        self.rb_light.setFont(QtGui.QFont('comic sans ms', 20))
        self.rb_light.clicked.connect(lambda slate, t='l': self.setTheme(t))
        # добавляем красоты
        if TWorker.get() == 'l':  # светлая
            self.rb_light.setChecked(True)
            self.setStyleSheet(light_main_window_stylesheet)
        elif TWorker.get() == 'd':  # тёмная
            self.rb_dark.setChecked(True)
            self.setStyleSheet(dark_main_window_stylesheet)
        self.rb_dark.setStyleSheet(radio_button_stylesheet)
        self.rb_light.setStyleSheet(radio_button_stylesheet)

    def setTheme(self, theme):
        """Функция выбора темы, подключена к кнопкам"""
        if TWorker.get() != theme:
            TWorker.set(theme)
            # ↑ если выбранная тема не равна предыдущей,
            # меняем тему в файле на выбранную)))))
            if theme == 'l':  # светлая
                for window in self.windows:
                    print('Меняю тему', window, 'на', theme)
                    if (isinstance(window, StatisticWindow)
                            or isinstance(window, HallOfFrameWindow)):
                        for widget in window.all_widgets:
                            widget.setStyleSheet(
                                light_statistic_window_stylesheet)
                    # ↑ если окно статистики или зала славы,
                    # то меняем стиль не самого окна, а его текст-виджетов
                    else:
                        window.setStyleSheet(light_main_window_stylesheet)
                self.setStyleSheet(light_main_window_stylesheet)
            elif theme == 'd':  # тёмная
                for window in self.windows:
                    print('Меняю тему', window, 'на', theme)
                    if (isinstance(window, StatisticWindow)
                            or isinstance(window, HallOfFrameWindow)):
                        for widget in window.all_widgets:
                            widget.setStyleSheet(
                                dark_statistic_window_stylesheet)
                    # ↑ если окно статистики или зала славы,
                    # то меняем стиль не самого окна, а его текст-виджетов
                    else:
                        window.setStyleSheet(dark_main_window_stylesheet)
                self.setStyleSheet(dark_main_window_stylesheet)


class StatisticWindow(QWidget):
    """Класс для окна достижений и статистики"""

    def __init__(self, best_score, score, medium_score,
                 total_time, sym_count, time, total_sym_count):
        self.best_score = best_score  # рекордный результат
        self.score = score  # текущий результат
        self.medium_score = medium_score  # средний результат
        self.total_time = total_time  # всего времени потрачено
        self.sym_count = sym_count  # набрано символов
        self.time = time  # потрачено времени
        self.total_sym_count = total_sym_count  # всего набрано символов
        self.all_widgets = []
        """Создаём красоту"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Рисуем GUI"""
        # заканчиваем с фоном
        self.move(300, 200)  # координаты от балды
        self.setFixedSize(1240, 430)
        self.setWindowTitle('Статистика и результаты')
        self.setStyleSheet(statistic_window_stylesheet)
        # делаем 6 виджетов для статистики
        x = 10
        y = 10
        for i in range(2):  # будет 2 строки с виджетами
            for j in range(3):  # в каждой строке будет по 3 столбца
                label = QLabel(self)
                label.setGeometry(x, y, 400, 200)
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QtGui.QFont('comic sans ms', 30))
                self.all_widgets.append(label)
                x += 410
            x = 10
            y += 210
        for num, widget in enumerate(self.all_widgets):
            if num == 0:
                widget.setText('Лучший результат\n' + str(self.best_score)
                               + '\n симв/сек')
            elif num == 1:
                widget.setText('Текущий результат\n' + str(self.score)
                               + '\n симв/сек')
            elif num == 2:
                widget.setText('Средний результат\n' + str(self.medium_score)
                               + '\n симв/сек')
            elif num == 3:
                widget.setText('Суммарное время\n' + str(self.total_time)
                               + '\n секунд')
            elif num == 4:
                widget.setText('Набрано\n' + str(self.sym_count)
                               + ' символов за \n' + str(self.time) +
                               ' секунд')
            elif num == 5:
                widget.setText('Всего набрано \n' + str(self.total_sym_count)
                               + '\n символов')
            self.change_theme()

    def change_theme(self):
        # добавляем красоты
        if TWorker.get() == 'l':  # светлая
            for label in self.all_widgets:
                label.setStyleSheet(light_statistic_window_stylesheet)
        elif TWorker.get() == 'd':  # тёмная
            for label in self.all_widgets:
                label.setStyleSheet(dark_statistic_window_stylesheet)


class HallOfFrameWindow(QWidget):
    """Класс для окна зала славы"""

    def __init__(self, medium_dict, best_dict):
        """Создаём красоту"""
        super().__init__()
        self.best_dict = best_dict
        self.medium_dict = medium_dict
        self.all_widgets = []
        self.all_best_score_labels = []
        self.all_medium_score_labels = []
        self.initUI()

    def initUI(self):
        """Рисуем GUI"""
        # заканчиваем с фоном
        self.move(400, 200)  # координаты от балды
        self.setFixedSize(1050, 560)
        self.setWindowTitle('Зал славы')
        self.setStyleSheet(statistic_window_stylesheet)
        x = 155
        for i in range(2):
            # 2 текст-виджета для категории
            label = QLabel(self)
            label.setGeometry(x, 10, 210, 40)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QtGui.QFont('comic sans ms', 20))
            label.setStyleSheet(dark_main_window_stylesheet)
            self.all_widgets.append(label)
            x += 530
            if i == 0:
                label.setText('Лучший счёт')
            else:
                label.setText('Средний счёт')
        y = 60
        x = 10
        for i in range(10):
            # 10 текст-виджет для лучших результатов
            label = QLabel(self)
            label.setGeometry(x, y, 500, 40)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QtGui.QFont('comic sans ms', 20))
            label.setStyleSheet(dark_main_window_stylesheet)
            self.all_best_score_labels.append(label)
            self.all_widgets.append(label)
            y += 50
        y = 60
        x = 540
        for i in range(10):
            # 10 текст-виджет для средних результатов
            label = QLabel(self)
            label.setGeometry(x, y, 500, 40)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QtGui.QFont('comic sans ms', 20))
            label.setStyleSheet(dark_main_window_stylesheet)
            self.all_medium_score_labels.append(label)
            self.all_widgets.append(label)
            y += 50
        index = 0
        # ставим значения в текст-виджеты
        for name, score in self.best_dict.items():
            self.all_best_score_labels[index].setText(name + '  -  '
                                                      + str(score))
            index += 1
        index = 0
        for name, score in self.medium_dict.items():
            self.all_medium_score_labels[index].setText(name + '  -  '
                                                        + str(score))
            index += 1
        self.change_theme()

    def change_theme(self):
        # добавляем красоты
        if TWorker.get() == 'l':  # светлая
            for label in self.all_widgets:
                label.setStyleSheet(light_statistic_window_stylesheet)
        elif TWorker.get() == 'd':  # тёмная
            for label in self.all_widgets:
                label.setStyleSheet(dark_statistic_window_stylesheet)
