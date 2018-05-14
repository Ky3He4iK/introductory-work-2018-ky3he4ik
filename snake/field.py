import random
from .cells import SuicideCell, PoisonCell, SnakeCell


class Field:
    def __init__(self,  width=20, height=20):
        self.width = width
        self.height = height
        self.suicide_pos = -1, -1
        self.poison_pos = -1, -1

        self._cells = [[None for _ in range(width)] for _ in range(height)]

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

    def change_suicide_cell(self):
        if self.suicide_pos != (-1, -1):
            self.set_cell(*self.suicide_pos, None)
        self.suicide_pos = self.get_random_empty_cell()
        self.set_cell(*self.suicide_pos, SuicideCell())

    def change_poison_cell(self):
        if self.poison_pos != (-1, -1):
            self.set_cell(*self.poison_pos, None)
        self.poison_pos = self.get_random_empty_cell()
        self.set_cell(*self.poison_pos, PoisonCell())

    def set_cell(self, y, x, cell):
        if not self.contains_cell(y, x):
            raise ValueError('Cell ({0}, {1}) is outside of field'.format(y, x))
        self._cells[y][x] = cell

    def get_cell(self, y, x):
        if not self.contains_cell(y, x):
            raise ValueError('Cell ({0}, {1}) is outside of field'.format(y, x))
        return self._cells[y][x]

    def update(self, game):
        if self.get_chance(0.01):
            self.change_suicide_cell()
        if self.get_chance(0.01):
            self.change_poison_cell()

        for y in range(self.height):
            for x in range(self.width):
                cell = self._cells[y][x]
                if cell is not None:
                    self._cells[y][x] = cell.update(game)

    def reverse_snake(self, snake_length):
        tail_pos = -1, -1
        pre_tail_pos = -1, -1

        for y in range(self.height):
            for x in range(self.width):
                cell = self._cells[y][x]
                if type(cell) is SnakeCell:
                    if tail_pos == (-1, -1) and cell.time_to_live == 1:
                        tail_pos = y, x
                    if pre_tail_pos == (-1, -1) and cell.time_to_live == 2:
                        pre_tail_pos = y, x
                    print("{0} to {1} at {2}".format(cell.time_to_live, snake_length - cell.time_to_live + 1, (y, x)))
                    self._cells[y][x].time_to_live = snake_length - cell.time_to_live + 1

        direction = tail_pos[0] - pre_tail_pos[0], tail_pos[1] - pre_tail_pos[1]
        return tail_pos, direction
