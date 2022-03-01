"""
Today's accomplishments were yesterday's impossibilities
(Robert H. Schuller)
"""
import sys
from PyQt5.QtWidgets import QApplication
from frontend import MainWindow


def except_hook(cls, exception, traceback):
    """Делаем адекватный отчёт об ошибке"""
    sys.__excepthook__(cls, exception, traceback)


def main():
    # немножко магии
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showFullScreen()
    sys.excepthook = except_hook
    sys.exit(app.exec())


# поехали
if __name__ == '__main__':
    main()
