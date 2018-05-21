from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter

from snake.renderer import Renderer
from snake.resourceClasses import TurnEnum
from .game import Game
from .Settings import Settings


class Board(QFrame):
    UPDATE_INTERVAL = 100  # RUNNING IN THE 90'S
    statusUpdated = pyqtSignal(str)

    def __init__(self, settings, parent):
        super().__init__(parent)
        self.UPDATE_INTERVAL = settings.game_speed
        self.game = Game(settings)

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
        elif event.key() == Qt.Key_F4 and (event.modifiers() & Qt.AltModifier):
            print("key close")
            self.close()
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
        status += "\tSnake len: " + str(self.game.snake.len)
        self.statusUpdated.emit(status)

    def close(self):
        print("closed")
        self.parent().close()
        super().close()


class SnakeWindow(QMainWindow):
    game_settings = pyqtSignal(Settings)

    def __init__(self, settings):
        super().__init__()

        self.board = Board(settings, self)
        self.status_bar = self.statusBar()
        self.square_size = settings.square_size
        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.board)

        self.board.statusUpdated[str].connect(self.status_bar.showMessage)

        self.setWindowTitle('Snake')
        self.resize(self.board.game.field.width * self.square_size,
                    self.board.game.field.height * self.square_size + self.board.height())
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def reset(self, settings):
        self.board = Board(settings, self)
        self.status_bar = self.statusBar()
        self.square_size = settings.square_size
        self.init_ui()

    def close(self):
        print("Closed")
        super().close()
