import random
from .cells import SuicideCell, PoisonCell, SnakeCell, FoodCell
from .resourceClasses import TurnEnum, COLORS


class Field:
    def __init__(self,  width=20, height=20):
        self.width = width
        self.height = height
        self.suicide_pos = -1, -1
        self.poison_pos = -1, -1
        self.food_pos = -1, -1

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

    def update(self, game, directions):
        if self.get_chance(0.01):
            self.change_suicide_cell()
        if self.get_chance(0.001):
            self.change_poison_cell()
        if self.get_chance(0.001):
            self.change_food_cell()

        found = [False for _ in range(game.snake.len + 2)]

        for y in range(self.height):
            for x in range(self.width):
                cell = self._cells[y][x]
                if cell is not None:
                    self._cells[y][x] = cell.update(game, directions)
                    if type(cell) is SnakeCell and cell.time_to_live > 0:
                        if cell.time_to_live > game.snake.len:
                            raise ValueError("A snake cell with ttl = {0} at ({1}, {2})".format(str(cell.time_to_live),
                                                                                                str(y), str(x)))
                        found[cell.time_to_live - 1] = True
                        if cell.time_to_live == game.snake.len:
                            cell.color = COLORS.LIGHT_GREEN
                        else:
                            cell.color = COLORS.GREEN
        # for i in range(game.snake.len):
        #     if not found[i] and i < game.snake.len:
        #         raise ValueError("I haven't snake cell with ttl = {0}".format(str(i + 1)))

    def find_snake_end(self, snake_len):
        tail_pos = -1, -1
        pre_tail_pos = -1, -1

        for y in range(self.height):
            for x in range(self.width):
                cell = self._cells[y][x]
                if type(cell) is SnakeCell:
                    if tail_pos == (-1, -1) and cell.time_to_live == snake_len:
                        tail_pos = y, x
                    if pre_tail_pos == (-1, -1) and cell.time_to_live == snake_len - 1:
                        pre_tail_pos = y, x
                    # print("{0} to {1} at {2}".format(cell.time_to_live, snake_length - cell.time_to_live + 1, (y, x)))
        return tail_pos, pre_tail_pos

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
                    self._cells[y][x].direction = TurnEnum.get_reversed(self._cells[y][x].direction)

        if tail_pos == (-1, -1) or pre_tail_pos == (-1, -1):
            tail_pos, pre_tail_pos = self.find_snake_end(snake_length)
        direction_y, direction_x = tail_pos[0] - pre_tail_pos[0], tail_pos[1] - pre_tail_pos[1]
        print(direction_y, direction_x, tail_pos, pre_tail_pos)
        direction_y = max(min(direction_y, 1), -1)  # normalize
        direction_x = max(min(direction_x, 1), -1)

        return tail_pos, (direction_y, direction_x)
