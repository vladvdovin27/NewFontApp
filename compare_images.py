from PIL import Image, ImageChops
import cv2
import matplotlib.pyplot as plt


def images_hash(path):
    """
    Хеширование изображения
    :param path: str
    :return: str
    """
    image = plt.imread(path)
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


def compare_hashes(hash_1, hash_2):
    """
    Сравнение хешов изображения
    :param hash_1: str
    :param hash_2: str
    :return: int
    """
    s = 0
    for i in range(16):
        if hash_1[i] == hash_2[i]:
            s += 1
    return s


def process_image(image_1, image_2):
    """
    Обработка и сравнение изображений
    :param image_1: Image
    :param image_2: Image
    :return: float
    """
    size = (28, 28)
    image_1.thumbnail(size)
    image_2.thumbnail(size)

    result = ImageChops.difference(image_1, image_2)

    return compare_process_image(result)


def compare_process_image(image):
    """
    Сравнение изображений по их разнице
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


def compare_images(path_1, path_2):
    """
    Функция сравнения изображений несколькими алгоритмами
    И возвращение метрики
    Минимальное значение: 0
    Максимальное значение: 17
    :param path_1: str
    :param path_2: str
    :return: int
    """
    image_1 = Image.open(path_1)
    image_2 = Image.open(path_2)

    hash_1, hash_2 = images_hash(path_1), images_hash(path_2)
    hash_result = compare_hashes(hash_1, hash_2)

    diff_result = process_image(image_1, image_2)

    metrics = hash_result + diff_result
    return metrics
