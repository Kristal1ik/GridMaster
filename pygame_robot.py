import pygame
from PyQt5 import QtWidgets
from pygame.locals import QUIT, USEREVENT, MOUSEBUTTONDOWN
from pygame.event import Event, post

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QImage, QPainter, QPixmap, QColor


class Constants:
    w = 1600
    h = 900
    peach = (255, 228, 196)


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # хак
        self.screen = pygame.Surface((Constants.w, Constants.h), pygame.HIDDEN)

        self.width = 21
        self.height = 21
        self.board = [[0] * 21 for _ in range(21)]
        self.way = 0
        self.way1 = 0
        self.run = False
        self.flag = False
        self.x = 300
        self.y = 300
        self.k = 0
        self.coords = []
        self.left = 6
        self.top = 6
        self.cell_size = 28
        self.coords1 = [[0, 6], [7, 6], [7, 2], [10, 2], [10, -1], [-6, -1], [-6, 3], [-4, 3], [-4, 1], [-5, 1], [-5, 0],
                   [0, 0]]
        self.coords2 = []

        for i in self.coords1:
            x = i[0]
            y = i[1]
            self.coords2.append([x * 28 + 300, -y * 28 + 300])

    def r_l_f_b(self, h):
        self.x = round(self.x, 2)
        self.y = round(self.y, 2)
        print(self.x, self.y)

        if h[0] != self.x:
            try:
                a = (h[0] - self.x) / abs((h[0] - self.x))
            except:
                a = 1
            self.x += 0.1 * 5 * a
            pygame.draw.circle(self.screen, pygame.Color(0, 0, 0),
                               (self.x, self.y),
                               (self.cell_size // 2 - 2), 20)

        if h[1] != self.y:
            try:
                a1 = (h[1] - self.y) / abs((h[1] - self.y))
            except:
                a1 = 1
            self.y += 0.1 * 5 * a1
            pygame.draw.circle(self.screen, pygame.Color(0, 0, 0),
                               (self.x, self.y),
                               (self.cell_size // 2 - 2), 20)

    def render(self, coords=[], run=False):
        if self.coords == []:
            self.coords = coords
        if not self.run:
            self.run = run

        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(self.screen, pygame.Color(255, 255, 255),
                                 (self.left + j * self.cell_size,
                                  self.top + i * self.cell_size,
                                  self.cell_size,
                                  self.cell_size), 1)

        pygame.draw.circle(self.screen, pygame.Color(0, 0, 0),
                           (self.x, self.y),
                           (self.cell_size // 2 - 2), 20)

        if self.run:
            print(self.coords)
            try:
                if self.coords[0] != [self.x, self.y]:
                    self.r_l_f_b(self.coords[0])
                else:
                    del self.coords[0]
            except Exception as e:
                print(e)

            if len(self.coords) == 0:
                self.run = False

    def loop(self):
        # print(9)
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.render(self.coords2, True)

        self.screen.fill((0, 150, 0))
        self.render()
        clock.tick(120)
        pygame.display.flip()


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
        button_start.setGeometry(Constants.w - 220 - 50, 5, 100, 40)

        button_stop = QtWidgets.QPushButton(self)
        button_stop.setText("Стоп")
        button_stop.setGeometry(Constants.w - 110 - 50, 5, 100, 40)

        button_open_local.clicked.connect(self.button_open_local_click)
        button_save_local.clicked.connect(self.button_save_local_click)
        button_open_db.clicked.connect(self.button_open_db_click)
        button_save_db.clicked.connect(self.button_save_db_click)
        button_start.clicked.connect(self.button_start_click)
        button_stop.clicked.connect(self.button_stop_click)

        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(20)

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
        self.start()


    def button_stop_click(self):
        print("button_stop")
        self.stop()


    def pygame_loop(self):
        # print("fdgfdg")
        # self.game.loop()
        # self.update(Constants.w // 2 + 150, Constants.h // 2 - 150, Constants.w, Constants.h)
        self.game.loop()
        self.update()

    def paintEvent(self, e):
        buf = self.game.screen.get_buffer()
        img = QImage(buf, Constants.w, Constants.h, QImage.Format_RGB32)
        p = QPainter(self)
        p.drawImage(Constants.w // 2 + 150, Constants.h // 2 - 150, img)

        painter = QPainter(self)
        painter.setPen(QColor(255, 228, 196))
        painter.setBrush(QColor(255, 228, 196))
        painter.drawRect(0, 0, Constants.w, 50)

    def start(self):
        self.game = Game()
        self.game.render(self.game.coords2, True)

    def stop(self):
        self.game = Game()
        self.game.render(self.game.coords2, False)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = GameWidget()
    w.resize(Constants.w - 50, Constants.h)
    w.show()
    sys.exit(app.exec_())
