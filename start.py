import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import change
import help
import fontadd


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/StartWindow.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.add_font)
        self.pushButton_3.clicked.connect(self.help)
        self.setFixedSize(715, 603)
        self.window = None
        self.setWindowTitle('Идентификация шрифтов')

    def run(self):
        """
        Загрузка окна для выбора режима работы приложения
        :return:
        """
        self.window = change.ChangeWindow()
        self.window.show()
        self.close()

    def help(self):
        """
        Загрузка окна для помощь пользователю
        :return:
        """
        self.window = help.HelpWindow()
        self.window.show()
        self.close()

    def add_font(self):
        """
        Загрузка окна для добавления нового шрифта в базу
        :return:
        """
        self.window = fontadd.FontAddWindow()
        self.window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
