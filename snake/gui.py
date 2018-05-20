from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QPushButton, QCheckBox, QRadioButton, QVBoxLayout, \
    QGridLayout, QGroupBox
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter

from snake.renderer import Renderer
from snake.resourceClasses import TurnEnum
from .game import Game
from .Settings import Settings
from .cells import WallCells


# TODO: добавить ЦУП (настройки) (MCC)
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

    def __init__(self, settings, mcc):
        super().__init__()

        self.board = Board(settings, self)
        self.status_bar = self.statusBar()
        self.square_size = settings.square_size

        self.mcc = mcc

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.board)

        self.board.statusUpdated[str].connect(self.status_bar.showMessage)

        self.setWindowTitle('Snake')
        self.resize(self.board.game.field.width * self.square_size, self.board.game.field.height * self.square_size)
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
        self.mcc.close()
        print("Closed")
        super().close()


class MCCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()

        self.sizes = (self.settings.width, self.settings.height)
        self.my_size = 200, 420
        self.factor = self.settings.square_size


        # self.init_ui()

    def init_ui(self):
        def set_walls():
            def on_toggle_death(toggle):
                if toggle:
                    self.settings.wall = WallCells.Death
            def on_toggle_portal(toggle):
                if toggle:
                    self.settings.wall = WallCells.Portals.Simple
            def on_toggle_portal_inverted(toggle):
                if toggle:
                    self.settings.wall = WallCells.Portals.Inverted
            def on_toggle_reverse(toggle):
                if toggle:
                    self.settings.wall = WallCells.Reverse
            variants = [[WallCells.Death, "Death wall"], [WallCells.Portals.Simple, "Portal wall"],
                        [WallCells.Portals.Inverted, "Inverted portal wall"], [WallCells.Reverse, "Rubber wall"]]

            buttons = []
            for w in variants:
                radio = QRadioButton(w[1])
                radio.setToolTip(w[0].__doc__)
                if radio is self.settings.wall:
                    radio.toggle()

                radio.toggled.connect(on_toggle_death if w is WallCells.Death else on_toggle_portal
                    if w is WallCells.Portals.Simple else on_toggle_portal_inverted if w is WallCells.Portals.Inverted
                    else on_toggle_reverse if w is WallCells.Reverse else on_toggle_death)
                buttons.append(radio)
            return buttons

        self.setWindowTitle('MCC')
        self.resize(*self.my_size)
        self.set_corner()
        self.setDisabled(False)

        button = QPushButton("Restart", self)
        button.setToolTip("Restart the game")
        button.move(40, 40)
        button.clicked.connect(self.on_click)

        v_box = QVBoxLayout()

        for radio in set_walls():
            v_box.addWidget(radio)

        group_box = QGroupBox("Settings")
        group_box.setLayout(v_box)
        grid = QGridLayout()
        grid.addWidget(group_box)
        self.setLayout(grid)
        self.show()

    def set(self, settings, restart):
        self.settings = settings
        self.sizes = (settings.width, settings.height)
        self.factor = settings.square_size
        self.init_ui()
        self.restart = restart

        cb = QCheckBox('Move food/poison/death cells', self)
        cb.toggle()
        cb.stateChanged.connect(self.moving_toggle)

        self.show()

    def moving_toggle(self, state):
        self.settings.moving_sells = state == Qt.Checked

    def set_corner(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + self.sizes[0] * self.factor / 2 + self.my_size[0] / 2 + 4,
                  (screen.height() - size.height()) / 2 - self.sizes[1] * self.factor / 2 + self.my_size[1] / 2)
        # Уроки выравнивания окон от ОМО "Костылёк", только здесь и сейчас

    @pyqtSlot()
    def on_click(self):
        self.restart(self.settings)
        print("Restarted")
