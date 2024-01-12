import pygame
from pygame.locals import QUIT, USEREVENT, MOUSEBUTTONDOWN
from pygame.event import Event, post
from random import randint

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSpinBox, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter, QPixmap


def get_color():
    return [randint(1, 10) * 25 for _ in range(3)]


class Game():
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((800, 800), pygame.HIDDEN)
        self.r = 1
        self.v = 1
        self.pos = 10, 10
        self.color = get_color()
        self.back_color = get_color()

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                self.pos = event.pos
                self.color = get_color()
                self.back_color = get_color()
            if event.type == USEREVENT:
                self.v = event.dict.get('v', self.v)
        self.screen.fill(self.back_color)
        pygame.draw.circle(self.screen, self.color, self.pos, self.r)
        pygame.display.update()
        self.r += self.v
        if not 1 < self.r < 200: self.v = -self.v


class GameWidget(QWidget):
    def __init__(self, game=None, parent=None):
        super().__init__()
        box = QSpinBox()
        box.setRange(-10, 10)
        box.setValue(1)
        box.valueChanged.connect(self.on_box)
        grid = QGridLayout(self)
        grid.setContentsMargins(1, 1, 1, 1)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 1)
        grid.addWidget(box, 0, 1, 1, 1)
        self.game = Game()
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(40)

    def pygame_loop(self):
        self.game.loop()
        self.update(100, 100, 800, 800)

    def on_box(self, val):
        post(Event(USEREVENT, {'v': val}))

    def paintEvent(self, e):
        if self.game:
            buf = self.game.screen.get_buffer()
            img = QImage(buf, 800, 800, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(100, 100, img)

    def mousePressEvent(self, e):
        x, y = e.pos().x(), e.pos().y()
        post(Event(MOUSEBUTTONDOWN, {'pos': (x, y)}))

    def closeEvent(self, e):
        QWidget.closeEvent(self, e)
        post(Event(QUIT))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = GameWidget()
    w.resize(900, 900)
    w.show()
    sys.exit(app.exec_())