import random
from .cells import SuicideCell, PoisonCell, FoodCell, DeathWallCell


class Field:
    def __init__(self,  width=20, height=20, WallType=DeathWallCell):
        self.width = width
        self.height = height
        self.suicide_pos = -1, -1
        self.poison_pos = -1, -1
        self.food_pos = -1, -1
        self._cells = [[None for _ in range(width)] for _ in range(height)]
        self.default_cell = WallType

    def contains_cell(self, y, x):
        return (0 <= y < self.height) and (0 <= x < self.width)

    def is_empty(self, y, x):
        if not self.contains_cell(y, x):
            raise ValueError('Cell ({0}, {1}) is outside of field'.format(y, x))
        return self._cells[y][x] is None

    def get_random_empty_cell(self):
        while True:
            y, x = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            if self.is_empty(y, x):
                return y, x

    @staticmethod
    def get_chance(threshold):
        return random.random() < threshold

    def change_cell(self, old_pos, new_cell):
        if old_pos != (-1, -1):
            self.set_cell(*old_pos, None)
        new_pos = self.get_random_empty_cell()
        self.set_cell(*new_pos, new_cell)
        return new_pos

    def change_suicide_cell(self):
        self.suicide_pos = self.change_cell(self.suicide_pos, SuicideCell())

    def change_poison_cell(self):
        self.poison_pos = self.change_cell(self.poison_pos, PoisonCell())

    def change_food_cell(self):
        self.food_pos = self.change_cell(self.food_pos, FoodCell())

    def set_cell(self, y, x, cell):
        if not self.contains_cell(y, x):
            raise ValueError('Cell ({0}, {1}) is outside of field'.format(y, x))
        self._cells[y][x] = cell

    def get_cell(self, y, x):
        if not self.contains_cell(y, x):
            raise ValueError('Cell ({0}, {1}) is outside of field'.format(y, x))
        return self._cells[y][x]

    def update(self, game):
        if self.get_chance(0.001):
            self.change_suicide_cell()
        if self.get_chance(0.0001):
            self.change_poison_cell()
        if self.get_chance(0.0001):
            self.change_food_cell()

        for y in range(self.height):
            for x in range(self.width):
                cell = self._cells[y][x]
                if cell is not None:
                    self._cells[y][x] = cell.update(game)

    def get_field_square(self):
        return len(self._cells) * len(self._cells[0])