#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from snake.gui import SnakeWindow
from snake.cells import WallCells
from snake.Settings import Settings

if __name__ == '__main__':
    app = QApplication([])

    settings = Settings(width=25, height=25, wall=WallCells.Portals.Random, game_speed=30, square_size=15,
                        moving_cells=True, moving_factor=0.01)
    settings.print()
    snake = SnakeWindow(settings)
    sys.exit(app.exec_())
