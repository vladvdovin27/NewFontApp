from Exceptions import *
import os
from Recognize_model import RecognizeModels


class ImageHandler:
    """
    Класс для обработки изображения:
        1. Определение расположения текста(букв)
        2. Определение буквы на изображении
    """
    def __init__(self, path):
        """
        :param path: Путь изображению
        """
        self.letter = ''
        self.path = path
        if not os.path.exists(path):
            raise WrongPathContent('Неправильный путь к файлу')
        if not self.path.split('/')[-1].split('.')[-1] == 'png':
            raise WrongContent('Неправильное содержимое файла(неправильное расширение файла)')
        self.labels = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯёабвгдежзийклмнопрстуфхцчшщъыьэюя"

    def set_letter(self):
        self.letter = RecognizeModels.letter_read_tesseract(self.path).strip()
        symbols = '.,;!? :'
        clear_string = ''
        for elm in self.letter:
            if elm not in symbols:
                clear_string += elm
        self.letter = clear_string
        if len(self.letter) != 1 or self.letter not in self.labels:
            self.letter = RecognizeModels.letter_read_model('model.h5', self.path)
        return self.letter
