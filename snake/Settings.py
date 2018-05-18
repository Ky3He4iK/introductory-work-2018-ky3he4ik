from .cells import DeathWallCell


class Settings:
    def __init__(self, width=20, height=20, wall=DeathWallCell):
        self.width = width
        self.height = height
        self.wall = wall
