#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from snake.game import Game
from snake.gui import SnakeWindow, MCCWindow
from snake.cells import PortalWallCell
from snake.Settings import Settings

if __name__ == '__main__':
    app = QApplication([])

    mcc = MCCWindow()
    snake = SnakeWindow(Game(Settings(width=30, height=20, wall=PortalWallCell)), mcc)
    mcc.set(snake, snake.board.game.restart)
    sys.exit(app.exec_())
