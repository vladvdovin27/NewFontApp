from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import start
from Backend import Backend


class LetterDetectedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/LetterDetectedWindow.ui', self)
        self.setFixedSize(650, 651)
        self.window = None
        self.setWindowTitle('Идентификация шрифтов')
        self.pushButton.clicked.connect(self.choose_image)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.hide()
        self.pushButton_5.clicked.connect(self.go2main)
        self.letter_path = ''

    def choose_image(self):
        self.letter_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def go2main(self):
        self.window = start.Window()
        self.window.show()
        self.close()

    def run(self):
        if self.letter_path != '':
            result_text = Backend.find_font(self.letter_path)
        else:
            result_text = 'Выберите изображения перед определением шрифта'
        self.label_3.setText(result_text)
        self.pushButton_3.show()
