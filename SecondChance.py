from compare_images import compare_images
import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class WrongWindow(QMainWindow):
    def __init__(self, path_to_img):
        super().__init__()
        uic.loadUi('WindowWrongLetter.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.letter_path = path_to_img
        self.letter = ''

    def run(self):
        if self.lineEdit.text:
            self.letter = self.lineEdit.text()
            self.process()
        else:
            self.label_4.setText('Вы не ввели букву')

    def process(self):
        letter_img_name = self.letter + '.png'
        font_path = 'DataFonts'

        font_metric = []
        for font in os.listdir(path=font_path):
            for let in os.listdir(path=font_path + '/' + font):
                if let == letter_img_name:
                    metric = compare_images(self.letter_path, font_path + '/' + font + '/' + let)
                    font_metric.append((font, metric))

        font_metric.sort(key=lambda x: x[1], reverse=True)

        result = font_metric[0][0] + '\n' + font_metric[1][0] + '\n' + font_metric[2][0]

        self.label_4.setText(result)
