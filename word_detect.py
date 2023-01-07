from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import start
import letter_detect


class WordDetectedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/WordDetectedWidow.ui', self)
        self.setFixedSize(650, 651)
        self.window = None
        self.filename = ''
        self.setWindowTitle('Идентификация шрифтов')
        self.pushButton.clicked.connect(self.choose_image)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.hide()
        self.pushButton_3.clicked.connect(self.wrong_word)
        self.pushButton_5.clicked.connect(self.go2main)

    def go2main(self):
        self.window = start.Window()
        self.window.show()
        self.close()

    def choose_image(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def run(self):
        if self.filename != '':
            result_text = self.detector(self.filename)
        else:
            result_text = 'Выберите изображения перед определением шрифта'
        self.label_3.setText(result_text)
        self.pushButton_3.show()

    def wrong_word(self):
        self.window = letter_detect.LetterDetectedWindow()
        self.window.show()
        self.close()
