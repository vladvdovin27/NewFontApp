from compare_images import compare_images
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic
from ImageHandler import ImageHandler
from SecondChance import WrongWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Window.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.letter_path = ''
        self.letter = ''
        self.imgHandler = None
        self.pushButton_2.clicked.connect(self.wrongLetter)
        self.pushButton_2.hide()

    def run(self):
        self.letter_path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.imgHandler = ImageHandler(self.letter_path)
        self.letter = self.imgHandler.set_letter()
        self.process()

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

        letter_text = f'Буква на изображении {self.letter}' + '\n' + \
                      f'Если это неверная буква, то нажмите на кнопку ниже' + '\n'
        result = font_metric[0][0] + '\n' + font_metric[1][0] + '\n' + font_metric[2][0] + '\n' * 2 + letter_text

        self.pushButton_2.show()
        self.label_4.setText(result)

    def wrongLetter(self):
        self.new_window = WrongWindow(self.letter_path)
        self.new_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
