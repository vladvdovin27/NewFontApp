from Recognize_model import RecognizeModels
from compare_images import compare_images
import os


class FontDetector:
    """
    Главный класс для нахождения нужных шрифтов
    """
    def __init__(self, target):
        self.target = target
        self.letter = ''
        self.labels = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯёабвгдежзийклмнопрстуфхцчшщъыьэюя"
        self.result = ''

    def __call__(self, filename):
        if self.target == 'letter':
            self.letter_detected(filename)
            if self.letter in self.labels and len(self.letter) == 1:
                self.find_font(filename)
                word_text = f'Буква на изображении {self.letter}' + '\n' + \
                            f'Если это неверная буква, то нажмите на кнопку ниже' + '\n' + \
                            f'Самые вероятные шрифты:'
                text = word_text + '\n' * 2 + self.result + '\n'
            else:
                text = 'Нейросеть не распознала букву, нажмите на кнопку ниже'
            return text
        elif self.target == 'word':
            word = RecognizeModels.detected_letters(filename)
            if all(list(map(lambda x: True if x in self.labels else False, list(word)))):
                self.find_font_word()
                word_text = f'Буква на изображении {word}' + '\n' + \
                            f'Если это неверное слово, то нажмите на кнопку ниже' + '\n' + \
                            f'Самые вероятные шрифты:'
                text = word_text + '\n' * 2 + self.result + '\n'
            else:
                text = 'Нейросеть не распознала слово, нажмите на кнопку ниже'
            return text
        else:
            return False

    def letter_detected(self, filename):
        self.letter = RecognizeModels.letter_read_tesseract(filename).strip()
        symbols = '.,;!? :'
        clear_string = ''
        for elm in self.letter:
            if elm not in symbols:
                clear_string += elm
        self.letter = clear_string

    def find_font(self, filename):
        letter_img_name = self.letter + '.png'
        font_path = 'DataFonts'

        font_metric = []
        for font in os.listdir(path=font_path):
            for let in os.listdir(path=font_path + '/' + font):
                if let == letter_img_name:
                    metric = compare_images(filename, font_path + '/' + font + '/' + let)
                    font_metric.append((font, metric))

        if font_metric:
            font_metric.sort(key=lambda x: x[1], reverse=True)
            self.result = '\t' + font_metric[0][0] + '\n\t' + font_metric[1][0] + '\n\t' + font_metric[2][0]
        else:
            self.result = 'Произошла ошибка, пожалуйста, попробуйте еще раз или\n обратитесь к разработчику'

    def find_font_word(self):
        dir_name = 'output'
        font_path = 'DataFonts'
        font_metric = []

        for font in os.listdir(path=font_path):
            metric = 0
            for letter in os.listdir(path=dir_name):
                for let in os.listdir(path=font_path + '/' + font):
                    if let == letter:
                        metric += compare_images(dir_name + '/' + letter, font_path + '/' + font + '/' + let)
            font_metric.append((font, metric))

        import shutil
        shutil.rmtree(dir_name)

        if font_metric:
            font_metric.sort(key=lambda x: x[1], reverse=True)
            self.result = '\t' + font_metric[0][0] + '\n\t' + font_metric[1][0] + '\n\t' + font_metric[2][0]
        else:
            self.result = 'Произошла ошибка, пожалуйста, попробуйте еще раз или\n обратитесь к разработчику'
