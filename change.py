from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import letter_detect
import word_detect


class ChangeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Change.ui', self)
        self.setFixedSize(500, 150)
        self.window = None
        self.setWindowTitle('Идентификация шрифтов')
        self.pushButton.clicked.connect(self.letter_recognize)
        self.pushButton_2.clicked.connect(self.word_recognize)

    def letter_recognize(self):
        self.window = letter_detect.LetterDetectedWindow()
        self.window.show()
        self.close()

    def word_recognize(self):
        self.window = word_detect.WordDetectedWindow()
        self.window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChangeWindow()
    ex.show()
    sys.exit(app.exec_())
