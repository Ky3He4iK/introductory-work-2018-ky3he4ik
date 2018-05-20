#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from snake.gui import SnakeWindow, MCCWindow
from snake.cells import WallCells
from snake.Settings import Settings

if __name__ == '__main__':
    app = QApplication([])

    settings = Settings(width=30, height=20, wall=WallCells.Portals.Inverted, game_speed=50, square_size=15,
                        moving_cells=True, )

    mcc = MCCWindow()
    snake = SnakeWindow(settings, mcc)
    mcc.set(settings, snake.reset)
    sys.exit(app.exec_())
