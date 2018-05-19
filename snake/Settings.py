from .cells import DeathWallCell


class Settings:
    def __init__(self, width=20, height=20, wall=DeathWallCell, game_speed=100, square_size=20):
        self.width = width
        self.height = height
        self.wall = wall
        self.game_speed = game_speed
        self.square_size = square_size
