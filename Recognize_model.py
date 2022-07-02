from tensorflow import keras
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt


class RecognizeModels:
    @staticmethod
    def letter_read_model(path_to_model, path_to_image):
        """
        Считывает букву с изображения
        :param path_to_model: Путь к предобученной модели
        :param path_to_image: Путь к файлу для чтения
        :return:
        """
        image = keras.preprocessing.image
        model = keras.models.load_model(path_to_model)

        img = image.load_img(path_to_image, target_size=(278, 278))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = model.predict(images, batch_size=1)
        result = int(np.argmax(classes))
        letters = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        return letters[result]

    @staticmethod
    def letter_read_tesseract(path):
        """
        Считывает букву с изображения
        :param path: Путь к изображения
        :return:str
        """
        image = plt.imread(path)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = img * 255
        img = img.astype('uint8')

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(img, config=config, lang="rus")
