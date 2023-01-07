import pytesseract
import matplotlib.pyplot as plt
import cv2
from Decoder import Decoder
import torch
import json
from img2vec_pytorch import Img2Vec
from PIL import Image, ImageChops
from scipy.spatial.distance import cosine
import sqlite3
import numpy as np
from torchvision.transforms import ToPILImage
import os


class Backend:
    """
    Class for all methods of backend
    Main methods: find_font, add_font
    """
    @staticmethod
    def letter_read(path):
        """
        Letter detect from image
        :param path: Путь к изображения
        :return:str
        """
        # Image load
        image = plt.imread(path)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = img * 255
        img = img.astype('uint8')

        # Letter detect
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(img, config=config, lang="rus")

    @staticmethod
    def decode(vectors_list):
        """
        Decode vectors to image(64*64*3)
        :param vectors_list:
        :return:
        """
        # Init model and load parameters
        model = Decoder()
        model.load_state_dict(torch.load('decoder.pt'))
        model.eval()

        transformer = ToPILImage()

        # Set up
        settings = Backend.load_settings()
        device = 'cuda' if settings['CUDA'] else 'cpu'
        model.to(device)
        vectors_list = torch.stack(list(map(lambda x: torch.from_numpy(x).to(device).to(torch.float32), vectors_list)))
        print(vectors_list[0].dtype)
        print(type(vectors_list[0]))

        # Decode
        result = model(vectors_list)
        img_res = []

        for elm in result:
            elm = torch.transpose(elm, 1, 2)
            elm = torch.transpose(elm, 0, 1)
            img_res.append(transformer(elm))

        return img_res

    @staticmethod
    def encode(path_list):
        # Load 'CUDA' setting
        cuda = Backend.load_settings()['CUDA']
        # Init a 'image to vec' model
        img2vec = Img2Vec(cuda=cuda)

        img_list = [Image.open(path) for path in path_list]

        vectors = img2vec.get_vec(img_list)

        return vectors

    @staticmethod
    def load_settings():
        with open("Settings.json", "r") as read_file:
            settings = json.load(read_file)

        return settings

    @staticmethod
    def images_hash(image):
        """
        Return a hash of image
        :return: str
        """
        image = np.array(image)
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)
        img_hash = ""
        for x in range(8):
            for y in range(8):
                if threshold_image[x][y] == 255:
                    img_hash += "1"
                else:
                    img_hash += "0"

        return img_hash

    @staticmethod
    def compare_hashes(hash_1, hash_2):
        """
        Hash's compare
        :param hash_1: str
        :param hash_2: str
        :return: int
        """
        s = 0
        for i in range(16):
            if hash_1[i] == hash_2[i]:
                s += 1
        return s

    @staticmethod
    def process_image(image_1, image_2):
        """
        Handle a images
        :return: float
        """
        size = (28, 28)
        image_1.thumbnail(size)
        image_2.thumbnail(size)

        result = ImageChops.difference(image_1, image_2)

        return Backend.compare_process_image(result)

    @staticmethod
    def compare_process_image(image):
        """
        Handle a difference between two images
        :param image: Image
        :return: float
        """
        pixels = image.load()
        x, y = image.size
        s = 0

        for i in range(x):
            for j in range(y):
                if pixels[i, j] == (0, 0, 0):
                    s += 1

        return s / (x * y)

    @staticmethod
    def find_font(path):
        # Init a letters id
        letters_id = {'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ж': 7, 'З': 8, 'И': 9, 'Й': 10,
                      'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18, 'Т': 19,
                      'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27, 'Ы': 28,
                      'Ь': 29, 'Э': 30, 'Ю': 31, 'Я': 32}
        # Load a settings
        settings = Backend.load_settings()

        # Get a vector of image
        vector = Backend.encode([path])[0]

        # Get a letter on image
        letter = Backend.letter_read(path).upper()

        # Create a connect to database
        con = sqlite3.connect('Fonts.sqlite3')
        cursor = con.cursor()

        # Get a all letter from a db
        db_res = cursor.execute('SELECT font, vector FROM Main WHERE letter = ?', str(letters_id[letter[0]])).fetchall()
        res = []

        # Cosine distance
        for elm in db_res:
            array = np.array(list(map(float, elm[1].split(', '))))
            cos_dis = cosine(array, vector)

            new_list = [elm[0], array, cos_dis]
            res.append(new_list)

        res.sort(key=lambda x: x[2], reverse=True)

        res = res[:min(20, len(res))]
        img_list = None

        # Compare a image's hashes
        if settings['Hash']:
            if img_list is None:
                img_list = Backend.decode([elm[1] for elm in res])  # Get a images from a vectors

            # Get a hashes for all images to compare
            hashes = [Backend.images_hash(elm) for elm in img_list]

            # Get a main image's hash
            image_hash = Backend.images_hash(Image.open(path))
            for i in range(len(res)):
                res[i][2] += Backend.compare_hashes(hashes[i], image_hash)
        # Compare a different of images
        if settings['Diff']:
            if img_list is None:
                img_list = Backend.decode([elm[1] for elm in res])
            image = Image.open(path)

            for i in range(len(res)):
                res[i][2] += Backend.process_image(img_list[i], image)

        # Get a first of five best results
        best_res = res[:min(5, len(res))]
        best_res.sort(key=lambda x: x[2], reverse=True)
        fonts = []

        # Take a name of best fonts
        for elm in best_res:
            font = cursor.execute('SELECT Font FROM Font WHERE id = ?', str(elm[0])).fetchall()
            fonts.append(font[0][0])

        return fonts

    @staticmethod
    def add_font(path_to_dir):
        # Init a letters id
        letters_id = {'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ж': 7, 'З': 8, 'И': 9, 'Й': 10,
                      'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18, 'Т': 19,
                      'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27, 'Ы': 28,
                      'Ь': 29, 'Э': 30, 'Ю': 31, 'Я': 32}
        # Get a font's name from path to dir
        font_name = path_to_dir.split('/')[-1]

        # Load settings
        settings = Backend.load_settings()

        # device = 'cuda' if settings['CUDA'] else 'cpu'
        # Init a image to vector model
        img2vec = Img2Vec(cuda=settings['CUDA'])

        # Init a connection to db
        con = sqlite3.connect('Fonts.sqlite3')
        cursor = con.cursor()

        # Add a font's name into db
        cursor.execute('INSERT INTO Font(Font) VALUES(?)', font_name)

        # Get a id of font
        font_id = cursor.execute('SELECT id FROM Font WHERE Font = ?', font_name).fetchone()[0]

        for img in os.listdir(path_to_dir):
            # Letter read from current image
            letter = Backend.letter_read(os.path.join(path_to_dir, img))

            # Get a vector of current image
            vector = img2vec.get_vec(Image.open(os.path.join(path_to_dir, img))).tolist()

            # Preprocess the vector
            str_vector = ', '.join(list(map(str, vector)))

            cursor.execute("INSERT INTO Main(font, letter, vector) VALUES(?, ?, ?)", (str(font_id), letter, str_vector))
