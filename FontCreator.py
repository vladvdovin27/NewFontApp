from Recognize_model import RecognizeModels
import os
from PIL import Image
import cv2


class FontCreator:
    """
    Класс для добавления новых шрифтов в базу
    """
    def __init__(self, lang_labels):
        self.result = ''
        self.lang_labels = lang_labels
        self.letters = []
        self.directory_name = 'DataFonts'

    def __call__(self, path, font_name, labels):
        """
        Создание нового шрифта на изображении(в принципе использовать можно)
        :param path: путь к изображению
        :param font_name: название шрифта
        :param labels: все символы, которые есть на изображении
        :return:
        """

        self.letters = []
        boxes = RecognizeModels.detected_letters(path, target='font')
        boxes = boxes.splitlines()

        img = cv2.imread(path)
        height, width, _ = img.shape

        if font_name in os.listdir(path=self.directory_name):
            self.result = 'Шрифт с данным названием существует, проверьте свои данные'
        elif len(boxes) != len(labels):
            self.result = 'Нейросеть не смогла определить все буквы, которые вы вписали\nСпособы решения проблемы:\n' \
                          '1. Перепроверьте символы, которые вы вписали\n' \
                          '2. Проверьте ваше входное изображение, попробуйте сделать его еще раз\n' \
                          'В случае, если ничего из этого не помогло, сообщите о баге'
        else:
            os.mkdir(os.path.join(self.directory_name, font_name))
            try:
                for i in range(len(labels)):
                    b = boxes[i].split()
                    print(b)
                    if b[0] in self.lang_labels:
                        if b[0] not in self.letters:
                            print(b[0])
                            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

                            image = Image.open(path)
                            new_img = image.crop((x, height - h, w, height - y))
                            new_img.convert('RGBA')

                            new_img.save(os.path.join(self.directory_name, font_name, b[0] + '.png'))

                            self.letters.append(b[0])

                self.result = 'Шрифт успешно добавлен в вашу базу шрифтов'
            except Exception as e:
                print(e)
                self.result = 'Произошла непредвиденная ошибка'

        return self.result
