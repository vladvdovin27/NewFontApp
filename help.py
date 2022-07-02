from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import start


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/HelpWindow.ui', self)
        self.window = None
        self.setFixedSize(482, 343)
        self.setWindowTitle('Помощь')
        self.pushButton.clicked.connect(self.go2main)

    def go2main(self):
        """
        Функция возвращения обратно
        :return:
        """
        self.window = start.Window()
        self.window.show()
        self.close()
