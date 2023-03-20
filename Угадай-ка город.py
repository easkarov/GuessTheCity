import sys
import requests
from io import BytesIO
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from maps_api import get_parameters
from PIL import Image
from random import shuffle


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cities = ["Владимир", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Севастополь",
                       "Кострома", "Самара", "Муром", "Архангельск"]
        self.initUI()

    def initUI(self):
        super().__init__()
        uic.loadUi('design.ui', self)  # Загружаем дизайн
        shuffle(self.cities)
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": None,
            "format": "json"}
        self.pixmap = QPixmap()
        self.current_city = 0
        self.image = QLabel(self)
        self.image.move(150, 50)
        self.image.resize(600, 500)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.show_city)
        self.run()

    def run(self):
        self.label_2.hide()
        city = self.cities[self.current_city]
        # print(city)
        self.geocoder_params["geocode"] = city
        response = requests.get(self.geocoder_api_server, params=self.geocoder_params)
        img = Image.open(BytesIO(get_parameters(response).content)).convert('RGB').save(
            f'images/{city}.jpeg')
        self.pixmap = QPixmap(f"images/{city}.jpeg")
        self.image.setPixmap(self.pixmap)
        self.image.show()
        self.current_city += 1
        if self.current_city == len(self.cities):
            self.current_city = 0

    def show_city(self):
        self.label_2.setText(self.cities[self.current_city - 1])
        self.label_2.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
