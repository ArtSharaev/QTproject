# -----------------------------------------------------------------------------
"""Нейтральные стили"""

# стиль для сообщений об ошибке
error_stylesheet = """
QWidget {
   color: #B22222;
}
"""

# базовый стиль для кнопок
buttons_stylesheet = """
QPushButton {
   background-color: #2F4F4F;
   color: #FFFFFF;
   border-radius: 10px;
   border-style: outset;
   border-width: 2px;
}
QPushButton:pressed {
    background-color: #FFFFFF;
    color: #2F4F4F;
}
"""

# стиль красных кнопок
danger_buttons_stylesheet = """
QPushButton {
   background-color: #B22222;
   color: #FFFFFF;
   border-radius: 10px;
   border-style: outset;
   border-width: 2px;
}
QPushButton:pressed {
    background-color: #FFFFFF;
    color: #B22222;
}
"""

# стиль для радио-кнопок
radio_button_stylesheet = """
QRadioButton {
   background-color: #2F4F4F;
   color: #FFFFFF;
   border-radius: 10px;
   border-style: outset;
   border-width: 2px;
}
QRadioButton::indicator {
    width: 20px;
    height: 20px;
}
"""

# стиль для вывода предложений
string_label_stylesheet = """
QLabel {
   color: #B8860B;
}
"""

# стиль выпадающего списка для выбора времени
combobox_stylesheet = """
QComboBox {
    border-width: 2px;
    border-style: outset;
    background: #2F4F4F;
    color: #FFFFFF
}

"""

# фон окна статистики
statistic_window_stylesheet = """
QWidget {
   background-color: #2F4F4F;
}
"""

# ----------------------------------------------------------------------------
"""Тёмные стили"""

# базовый стиль для всех виджетов
dark_main_window_stylesheet = """
QWidget {
   background-color: #212121;
   color: #FFFFFF;
}
"""

# стиль для текст-виджетов окна статистики
dark_statistic_window_stylesheet = """
QLabel {
   background-color: #212121;
   color: #FFFFFF;
   border-width: 2px;
   border-style: outset;
   border-radius: 20px;
}
"""
# ----------------------------------------------------------------------------
"""Светлые стили"""

# базовый стиль для всех виджетов
light_main_window_stylesheet = """
QWidget {
   background-color: #FFFFFF;
   color: #212121;
}
"""

# стиль для текст-виджетов окна статистики
light_statistic_window_stylesheet = """
QLabel {
   background-color: #FFFFFF;
   color: #212121;
   border-width: 2px;
   border-style: outset;
   border-radius: 20px;
}
"""
# ----------------------------------------------------------------------------
