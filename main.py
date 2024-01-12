import pygame
from pygame.locals import QUIT, USEREVENT, MOUSEBUTTONDOWN
from pygame.event import Event, post

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter, QPixmap


class Constants:
    w = 1600
    h = 900
    peach = (255, 228, 196)


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
        grid = QGridLayout(self)
        grid.setContentsMargins(1, 1, 1, 1)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 1)
        self.game = Game()
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(40)

    def pygame_loop(self):
        self.game.loop()
        self.update(Constants.w // 2 + 150, Constants.h // 2 - 150, Constants.w, Constants.h)

    def paintEvent(self, e):
        if self.game:
            buf = self.game.screen.get_buffer()
            img = QImage(buf, Constants.w, Constants.h, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(Constants.w // 2 + 150, Constants.h // 2 - 150, img)

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
    w.resize(Constants.w, Constants.h)
    w.show()
    sys.exit(app.exec_())
