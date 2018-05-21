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

    def print(self):
        print("Current settings:")
        print("Field: {0}x{1} cells".format(str(self.width), str(self.height)))
        print("Cell size: {0} px".format(str(self.square_size)))
        print("Game speed: {0} ticks per second".format(str(1000 / self.game_speed)))
        print("Wall type: {0}".format(self.wall.__class__.__name__))
        if self.moving_sells:
            print("Food and poison cells will be moved with chance {0}%\nDeath cell - {1}%".
                  format(str(self.moving_factor * 10), str(self.moving_factor * 100)))
        else:
            print("Food, poison and death cells wouldn't be moved")
