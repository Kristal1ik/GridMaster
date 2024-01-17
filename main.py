import pygame
from PyQt5 import QtWidgets
from pygame.locals import QUIT, USEREVENT, MOUSEBUTTONDOWN
from pygame.event import Event, post

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QImage, QPainter, QPixmap, QColor


class Constants:
    w = 1600
    h = 900
    peach = (255, 228, 196)
    white = (0, 0, 0)


class Game():
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((Constants.w, Constants.h), pygame.HIDDEN)

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        self.screen.fill(Constants.white)
        pygame.display.update()


class GameWidget(QWidget):
    def __init__(self, game=None, parent=None):
        super().__init__()
        # self.initUI()
        grid = QGridLayout(self)
        grid.setContentsMargins(1, 1, 1, 1)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 1)
        self.game = Game()

        button_open_local = QtWidgets.QPushButton(self)
        button_open_local.setText("Открыть локально")
        button_open_local.setGeometry(5, 5, 200, 40)

        button_save_local = QtWidgets.QPushButton(self)
        button_save_local.setText("Сохранить локально")
        button_save_local.setGeometry(210, 5, 200, 40)

        button_open_db = QtWidgets.QPushButton(self)
        button_open_db.setText("Открыть из бд")
        button_open_db.setGeometry(420, 5, 200, 40)

        button_save_db = QtWidgets.QPushButton(self)
        button_save_db.setText("Сохранить бд")
        button_save_db.setGeometry(630, 5, 200, 40)

        button_start = QtWidgets.QPushButton(self)
        button_start.setText("Старт")
        button_start.setGeometry(Constants.w - 220, 5, 100, 40)

        button_stop = QtWidgets.QPushButton(self)
        button_stop.setText("Стоп")
        button_stop.setGeometry(Constants.w - 110, 5, 100, 40)

        button_open_local.clicked.connect(self.button_open_local_click)
        button_save_local.clicked.connect(self.button_save_local_click)
        button_open_db.clicked.connect(self.button_open_db_click)
        button_save_db.clicked.connect(self.button_save_db_click)
        button_start.clicked.connect(self.button_start_click)
        button_stop.clicked.connect(self.button_stop_click)


        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(40)

        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setGeometry(0, 50, Constants.w // 2 + 150, Constants.h - 50)

        self.rect()

    def button_open_local_click(self):
        print("button_open_local")

    def button_save_local_click(self):
        print("button_save_local")

    def button_open_db_click(self):
        print("button_open_db")

    def button_save_db_click(self):
        print("button_save_db")

    def button_start_click(self):
        print("button_start")

    def button_stop_click(self):
        print("button_stop")

    # def initUI(self):
    #     hbox = QHBoxLayout(self)
    #     pixmap = QPixmap("play.png")
    #     lbl = QLabel(self)
    #     lbl.setPixmap(pixmap)
    #     hbox.addWidget(lbl)
    #     self.setLayout(hbox)
    #     self.move(100, 200)
    #     print("dd")
    #     self.show()

    def pygame_loop(self):
        self.game.loop()
        self.update(Constants.w // 2 + 150, Constants.h // 2 - 150, Constants.w, Constants.h)

    def paintEvent(self, e):
        if self.game:
            buf = self.game.screen.get_buffer()
            img = QImage(buf, Constants.w, Constants.h, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(Constants.w // 2 + 150, Constants.h // 2 - 150, img)

            painter = QPainter(self)
            painter.setPen(QColor(255, 228, 196))
            painter.setBrush(QColor(255, 228, 196))
            painter.drawRect(0, 0, Constants.w, 50)

    def closeEvent(self, e):
        QWidget.closeEvent(self, e)
        post(Event(QUIT))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = GameWidget()
    w.resize(Constants.w, Constants.h)
    w.show()
    sys.exit(app.exec_())
