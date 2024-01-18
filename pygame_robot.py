import pygame
import pymysql
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFrame, QTextEdit, QFileDialog, \
    QMessageBox, QMainWindow, QTableWidget, QDialog
from PyQt5.QtCore import QTimer, QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QImage, QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from src.parser import parser

class Constants:
    w = 1600
    h = 900
    peach = (255, 228, 196)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(669, 385)
        self.deleteFilmButton = QPushButton(Form)
        self.deleteFilmButton.setObjectName(u"deleteFilmButton")
        self.deleteFilmButton.setGeometry(QRect(10, 330, 651, 51))
        self.filmsTable = QTableWidget(Form)
        self.filmsTable.setObjectName(u"filmsTable")
        self.filmsTable.setGeometry(QRect(10, 0, 651, 321))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.deleteFilmButton.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0444\u0430\u0439\u043b", None))
    # retranslateUi

class DB(QDialog, Ui_Form):  # Вот тут основное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.up_f()
        self.deleteFilmButton.clicked.connect(self.df)
        self.dialogs = []
        # self.exitAction.triggered.connect(self.exit)

    def up_f(self):
        result = []
        connection = pymysql.connect(
            host='185.221.213.34',
            port=3306,
            user='predprof',
            password='Xz28]~w&V$weNQ%',
            database='interpret',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM `data`"
            cursor.execute(select_all_rows)
            res = cursor.fetchall()
        connection.close()
        cursor.close()

        for i in res:
            res = list(i.values())
            result.append(res[:-1])
        print(result)

        self.filmsTable.setRowCount(len(result))
        self.filmsTable.setColumnCount(len(result[0]))
        self.filmsTable.setHorizontalHeaderLabels(
            ['Название файла', 'Дата сохранения'])

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.filmsTable.setItem(i, j, QTableWidgetItem(str(val)))

    def df(self):
        rows = list(set([i.row() for i in self.filmsTable.selectedItems()]))
        ids = [self.filmsTable.item(i, 0).text() for i in rows]
        if not ids:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите что-нибудь!")
            msg.setWindowTitle("Уведомление")
            msg.exec_()
            return

        else:
            connection = pymysql.connect(
                host='185.221.213.34',
                port=3306,
                user='predprof',
                password='Xz28]~w&V$weNQ%',
                database='interpret',
                cursorclass=pymysql.cursors.DictCursor
            )
            print(int(''.join(ids)))

            with connection.cursor() as cursor:
                insert_query = f'''DELETE FROM `data` WHERE id = "{int(''.join(ids))}";'''
                cursor.execute(insert_query)
                connection.commit()
                print('удалена')

            connection.close()
            cursor.close()
            self.up_f()

    def exit(self):
        self.close()

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
        self.coords1 = parser('temp.txt')
        self.coords2 = []

        for i in self.coords1:
            print(i)
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


class GameWidget(QMainWindow):
    def __init__(self, game=None, parent=None):
        super().__init__()
        # self.initUI()
        grid = QGridLayout(self)
        grid.setContentsMargins(1, 1, 1, 1)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 1)
        self.game = Game()

        self.button_open_local = QtWidgets.QPushButton(self)
        self.button_open_local.setText("Открыть локально")
        self.button_open_local.setGeometry(5, 5, 200, 40)

        self.button_save_local = QtWidgets.QPushButton(self)
        self.button_save_local.setText("Сохранить локально")
        self.button_save_local.setGeometry(210, 5, 200, 40)

        self.button_open_db = QtWidgets.QPushButton(self)
        self.button_open_db.setText("Открыть из бд")
        self.button_open_db.setGeometry(420, 5, 200, 40)

        self.button_save_db = QtWidgets.QPushButton(self)
        self.button_save_db.setText("Сохранить бд")
        self.button_save_db.setGeometry(630, 5, 200, 40)

        self.button_start = QtWidgets.QPushButton(self)
        self.button_start.setText("Старт")
        self.button_start.setGeometry(Constants.w - 220 - 50, 5, 100, 40)

        self.button_stop = QtWidgets.QPushButton(self)
        self.button_stop.setText("Стоп")
        self.button_stop.setGeometry(Constants.w - 110 - 50, 5, 100, 40)

        self.button_open_local.clicked.connect(self.button_open_local_click)
        self.button_save_local.clicked.connect(self.button_save_local_click)
        self.button_open_db.clicked.connect(self.button_open_db_click)
        self.button_save_db.clicked.connect(self.button_save_db_click)
        self.button_start.clicked.connect(self.button_start_click)
        self.button_stop.clicked.connect(self.button_stop_click)

        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(20)

        self.textEdit1 = QTextEdit(self)
        self.textEdit1.setGeometry(0, 50, Constants.w // 2 + 150, Constants.h - 50)

        self.rect()

    def button_open_local_click(self):
        print("button_open_local")
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать файл",
                                                         ".",
                                                         "Text Files(*.txt)")
        print(filename)

        with open(filename, encoding='utf8') as f:
            self.textEdit1.setPlainText(''.join(f.readlines()))

    def button_save_local_click(self):
        print("button_save_local")
        filename, ok = QFileDialog.getSaveFileName(self,
                                                   "Сохранить файл",
                                                   ".",
                                                   "Text Files(*.txt)")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Файл <br><b>{}</b> <br> успешно сохранён!".format(filename.split('/')[-1]))
        msg.setWindowTitle("Уведомление")
        msg.exec_()

        print(filename)

    def button_open_db_click(self):
        print("button_open_db")
        self.window2 = DB()
        self.window2.show()

    def button_save_db_click(self):
        print("button_save_db")

        connection = pymysql.connect(
            host='185.221.213.34',
            port=3306,
            user='predprof',
            password='Xz28]~w&V$weNQ%',
            database='interpret',
            cursorclass=pymysql.cursors.DictCursor
        )
        a = self.textEdit1.toPlainText().strip()

        with connection.cursor() as cursor:
            insert_query = f'''INSERT INTO `data`(`file`, `time`, `txt`) VALUES ({'[value-1]'},{'[value-2]'},{'[value-3]'});'''
            cursor.execute(insert_query)
            connection.commit()
            print('добавлено')

        connection.close()
        cursor.close()

    def button_start_click(self):
        print("button_start")
        a = self.textEdit1.toPlainText().strip()
        print(a)
        with open('temp.txt', 'wt', encoding='utf8') as f:
            print(self.textEdit1.toPlainText().strip(), file=f)

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

    app = QApplication(sys.argv[1:])
    w = GameWidget()
    w.resize(Constants.w - 50, Constants.h)
    w.show()
    sys.exit(app.exec_())