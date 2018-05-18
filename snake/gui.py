from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter

from snake.renderer import Renderer
from snake.resourceClasses import TurnEnum
from .game import Game
from .Settings import Settings


# TODO: добавить ЦУП (настройки) (MCC)
class Board(QFrame):
    UPDATE_INTERVAL = 100  # RUNNING IN THE 90'S
    statusUpdated = pyqtSignal(str)

    def __init__(self, game, parent):
        super().__init__(parent)

        self.game = game

        self.timer = QBasicTimer()
        self.timer.start(self.UPDATE_INTERVAL, self)

        self.setFocusPolicy(Qt.StrongFocus)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.game.update()
            self.update()
            self.update_status()
        else:
            super().timerEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setViewport(self.contentsRect())

        renderer = Renderer(painter)
        renderer.render(self.game.field)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Space:
            self.game.pause()
            return

        if key == Qt.Key_R:
            self.game.restart()

        if self.game.is_paused:
            return

        if key == Qt.Key_Left or key == Qt.Key_A:
            self.game.turn(TurnEnum.LEFT)
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.game.turn(TurnEnum.RIGHT)
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.game.turn(TurnEnum.DOWN)
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.game.turn(TurnEnum.UP)
        else:
            super().keyPressEvent(event)

    def update_status(self):
        status = 'Score: {0}'.format(self.game.score)
        if self.game.is_won:
            status = 'YOU WON!!' + status
        elif self.game.is_dead:
            status = 'GAME OVER. ' + status
        elif self.game.is_paused:
            status = 'PAUSED'
        self.statusUpdated.emit(status)


class SnakeWindow(QMainWindow):
    game_settings = pyqtSignal(Settings)

    def __init__(self, game, mcc):
        super().__init__()

        self.board = Board(game, self)
        self.status_bar = self.statusBar()

        self.mcc = mcc

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.board)

        self.board.statusUpdated[str].connect(self.status_bar.showMessage)

        self.setWindowTitle('Snake')
        self.resize(self.board.game.field.width * 20, self.board.game.field.height * 20)
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def reset(self, settings, mcc):
        self.__init__(Game().restart(settings), mcc)

    def close(self):
        self.mcc.close()
        super().close()


class MCCBoard(QFrame):
    UPDATE_INTERVAL = 100  # RUNNING IN THE 90'S
    statusUpdated = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setViewport(self.contentsRect())


class MCCWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.board = MCCBoard(self)

        self.sizes = (0, 0)
        self.my_size = 200, 120

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.board)

        self.setWindowTitle('MCC')
        self.resize(*self.my_size)
        self.set_corner()
        self.setDisabled(False)

        self.button = QPushButton("Restart", self)
        self.button.setToolTip("This is pointless, but press me")
        self.button.move(40, 40)
        self.button.clicked.connect(self.on_click)
        self.show()

    def set(self, snake_window, restart):
        self.sizes = (snake_window.board.game.field.width, snake_window.board.game.field.height)
        self.init_ui()
        self.restart = restart
        self.show()

    def set_corner(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + (self.sizes[0]) * 20 / 2 + self.my_size[0] / 2 + 4,
                  (screen.height() - size.height()) / 2 - self.sizes[1] * 20 / 2 + self.my_size[1] / 2)
        # Уроки выравнивания окон от ОМО "Костылёк", только здесь и сейчас

    @pyqtSlot()
    def on_click(self):
        self.restart()
        print("Restarted")
