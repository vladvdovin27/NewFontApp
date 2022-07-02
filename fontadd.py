from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import start
from FontCreator import FontCreator


class FontAddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/FontAddWindow.ui', self)
        self.window = None
        self.path = ''
        self.result = ''
        self.rus_label = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯёабвгдежзийклмнопрстуфхцчшщъыьэюя"
        self.setFixedSize(880, 739)
        self.setWindowTitle('Добавление шрифта')
        self.pushButton.clicked.connect(self.go2main)
        self.pushButton_2.clicked.connect(self.choose_image)
        self.pushButton_3.clicked.connect(self.run)
        self.creator = FontCreator(self.rus_label)

    def go2main(self):
        """
        Функция возвращения обратно
        :return:
        """
        self.window = start.Window()
        self.window.show()
        self.close()

    def choose_image(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def run(self):
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
            self.result = self.creator(self.path, self.lineEdit_2.text(), self.lineEdit.text())
        else:
            self.result = 'Введите данные'

        self.label_3.setText(self.result)
