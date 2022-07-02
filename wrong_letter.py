from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import start
import os
from compare_images import compare_images


class WrongLetterWindow(QMainWindow):
    def __init__(self, filename):
        super().__init__()
        uic.loadUi('ui/WrongLetter.ui', self)
        self.setFixedSize(479, 528)
        self.filename = filename
        self.window = None
        self.result = ''
        self.setWindowTitle('Идентификация шрифтов')
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_5.clicked.connect(self.go2main)

    def go2main(self):
        self.window = start.Window()
        self.window.show()
        self.close()

    def run(self):
        if self.lineEdit.text() != '':
            letter_img_name = self.lineEdit.text() + '.png'
            font_path = 'DataFonts'

            font_metric = []
            for font in os.listdir(path=font_path):
                for let in os.listdir(path=font_path + '/' + font):
                    if let == letter_img_name:
                        metric = compare_images(self.filename, font_path + '/' + font + '/' + let)
                        font_metric.append((font, metric))

            if font_metric:
                font_metric.sort(key=lambda x: x[1], reverse=True)
                self.result = '\t' + font_metric[0][0] + '\n\t' + font_metric[1][0] + '\n\t' + font_metric[2][0]
            else:
                self.result = 'Произошла ошибка, пожалуйста, попробуйте еще раз или\n обратитесь к разработчику'

            word_text = f'Самые вероятные шрифты:'
            text = word_text + '\n' * 2 + self.result + '\n'
            self.label_3.setText(text)
