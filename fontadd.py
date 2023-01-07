import Back as Back
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import start
from Backend import Backend


class FontAddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/FontAddWindow.ui', self)
        self.window = None
        self.path = ''
        self.result = ''
        self.setFixedSize(880, 739)
        self.setWindowTitle('Добавление шрифта')
        self.pushButton.clicked.connect(self.go2main)
        self.pushButton_2.clicked.connect(self.choose_image)
        self.pushButton_3.clicked.connect(self.run)

    def go2main(self):
        """
        Функция возврата на главный экран
        :return:
        """
        self.window = start.Window()
        self.window.show()
        self.close()

    def choose_image(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def run(self):
        self.result = 'Шрифт добавлен в базу'

        try:
            Backend.add_font(self.path)
        except Exception:
            self.result = 'Произошла ошибка при добавлении шрифта, попробуйте снова'

        self.label_3.setText(self.result)
