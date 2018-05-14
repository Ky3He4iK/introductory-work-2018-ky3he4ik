import queue

from .field import Field
from .cells import SnakeCell, DeathWallCell
from .resourceClasses import TurnEnum


class SnakeState:
    TURNS = {
        TurnEnum.UP:    (-1, 0),
        TurnEnum.DOWN:  (1, 0),
        TurnEnum.LEFT:  (0, -1),
        TurnEnum.RIGHT: (0, 1),
    }

    def __init__(self, head_position, start_length, direction):
        self.head = head_position
        self.len = start_length
        self.direction = direction
        self.directions = [direction for _ in range(self.len)]

    def turn(self, direction):
        if direction not in self.TURNS.keys():
            raise ValueError('{0} is not a valid side' % direction)
        self.direction = direction

    @staticmethod
    def get_turn(turn):
        for t in SnakeState.TURNS:
            if turn == SnakeState.TURNS[t]:
                return t

    def is_reverse(self, direction):
        return self.len > 1 and self.TURNS[self.direction][0] == -self.TURNS[direction][0] and \
               self.TURNS[self.direction][1] == -self.TURNS[direction][1]

    def get_next_position(self):
        dy, dx = self.TURNS[self.direction]
        # print(dy, dx)
        if self.len == len(self.directions):
            self.directions = self.directions[1:] + [self.direction]
        elif self.len > len(self.directions):
            self.directions = [self.directions[0] for _ in range(self.len - len(self.directions))] + \
                              self.directions[1:] + [self.direction]
        else:
            self.directions = self.directions[len(self.directions) - self.len + 1:] + [self.direction]
        return self.head[0] + dy, self.head[1] + dx


class Game:
    def __init__(self, width=20, height=20):
        self.field = Field(width, height)
        self.snake = SnakeState((1, 2), 2, TurnEnum.RIGHT)

        self.is_paused = True
        self.is_dead = False
        self.score = 0

        self.init_level()

    def init_level(self):
        self.field.set_cell(1, 1, SnakeCell(time_to_live=1, direction=TurnEnum.RIGHT))
        self.field.set_cell(1, 2, SnakeCell(time_to_live=2, direction=TurnEnum.RIGHT))

        for x in range(self.field.width):
            self.field.set_cell(0, x, DeathWallCell())
            self.field.set_cell(self.field.width - 1, x, DeathWallCell())

        for y in range(self.field.height):
            self.field.set_cell(y, 0, DeathWallCell())
            self.field.set_cell(y, self.field.height - 1, DeathWallCell())

        self.spawn_food()
        self.spawn_poison_food()
        self.spawn_suicide_food()
        self.spawn_food()

    def spawn_food(self):
        self.field.change_food_cell()

    def spawn_poison_food(self):
        self.field.change_poison_cell()

    def spawn_suicide_food(self):
        self.field.change_suicide_cell()

    def pause(self):
        self.is_paused = not self.is_paused

    def turn(self, side):
        if self.snake.is_reverse(side):
            self.reverse_snake(side)
        else:
            self.snake.turn(side)

    def update(self):
        if self.is_paused or self.is_dead:
            return

        if not self.try_move_head():
            self.is_dead = True
            return

        cell = self.field.get_cell(*self.snake.head)
        if cell is not None:
            cell.on_bump(self)

        # self.field.set_cell(*self.snake.head, )
        SnakeCell(time_to_live=self.snake.len, direction=self.snake.direction)
        # Костыль. Зато обновление длины змейки происходит на клетке с едой

        if self.is_dead:
            return

        self.field.update(game=self, directions=self.snake.directions)

        self.field.set_cell(*self.snake.head, SnakeCell(time_to_live=self.snake.len, direction=self.snake.direction))

    def try_move_head(self):
        new_y, new_x = self.snake.get_next_position()

        if self.field.contains_cell(new_y, new_x):
            self.snake.head = new_y, new_x
            return True
        return False

    def restart(self):
        self.__init__(self.field.width, self.field.height)

    def get_direction(self, dy, dx):
        pass

    def reverse_snake(self, direction):
        res = self.field.reverse_snake(self.snake.len)
        self.snake.turn(SnakeState.get_turn(res[1]))
        self.snake.head = res[0]
        # print(direction)
        print("Reversed. current direction is {0}. Head at {1}".format(str(direction), str(self.snake.head)))
