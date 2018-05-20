from .cells import WallCells


class Settings:
    def __init__(self, width=20, height=20, wall=WallCells.Death, game_speed=100, square_size=20, moving_cells=False,
                 moving_factor=0.001):
        self.width = width
        self.height = height
        self.wall = wall
        self.game_speed = game_speed
        self.square_size = square_size
        self.moving_sells = moving_cells
        self.moving_factor = moving_factor
