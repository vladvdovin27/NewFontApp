from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import start
import json


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/SettingWindow.ui', self)
        self.setFixedSize(528, 506)
        self.to_save = {
            'Да': True,
            'Нет': False
        }
        self.to_parse = {
            True: 1,
            False: 0
        }
        self.parse()
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.go2main)
        self.window = None

    def save(self):
        new_settings = {}

        new_settings['Hash'] = self.to_save[self.comboBox.currentText()]
        new_settings['Diff'] = self.to_save[self.comboBox_2.currentText()]
        new_settings['CUDA'] = self.to_save[self.comboBox_3.currentText()]

        with open('Settings.json', 'w') as fp:
            json.dump(new_settings, fp)

    def go2main(self):
        self.window = start.Window()
        self.window.show()
        self.close()

    def parse(self):
        with open("Settings.json", "r") as read_file:
            settings = json.load(read_file)

        print(settings)
        print(settings['Hash'])
        print(self.to_parse[settings['Hash']])
        self.comboBox.setCurrentIndex(self.to_parse[settings['Hash']])
        self.comboBox_2.setCurrentIndex(self.to_parse[settings['Diff']])
        self.comboBox_3.setCurrentIndex(self.to_parse[settings['CUDA']])
