from .field import Field
from .cells import SnakeCell, DeathWallCell
from .resourceClasses import TurnEnum
from .Settings import Settings


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
        self.real_direction = self.direction

    def turn(self, direction):
        if direction not in self.TURNS.keys():
            raise ValueError('{0} is not a valid side'.format(str(direction)))
        self.direction = direction

    @staticmethod
    def get_turn(turn):
        for t in SnakeState.TURNS:
            if turn == SnakeState.TURNS[t]:
                return t
        print("Unknown direction: {0}".format(str(turn)))

    def is_reverse(self, direction):
        return self.len > 1 and self.TURNS[self.real_direction][0] == -self.TURNS[direction][0] and \
               self.TURNS[self.real_direction][1] == -self.TURNS[direction][1]

    def get_next_head(self):
        return self.head[0] + self.TURNS[self.direction][0], self.head[1] + self.TURNS[self.direction][1]

    def get_next_position(self):
        dy, dx = self.TURNS[self.direction]
        return self.head[0] + dy, self.head[1] + dx


class Game:
    def __init__(self, settings):
        self.wall = settings.wall
        self.field = Field(settings)
        self.snake = SnakeState((1, 2), 2, TurnEnum.RIGHT)

        self.is_paused = True
        self.is_dead = False
        self.score = 0
        self.is_won = False

        self.init_level()

    def init_level(self):
        self.field.set_cell(1, 1, SnakeCell(time_to_live=1))
        self.field.set_cell(1, 2, SnakeCell(time_to_live=2))
        # self.field.get_cell(1, 2).color = COLORS.LIGHT_GREEN

        for x in range(self.field.width):
            self.field.set_cell(0, x, self.wall(self, 0, x))
            self.field.set_cell(self.field.height - 1, x, self.wall(self, self.field.height - 1, x))

        for y in range(self.field.height):
            self.field.set_cell(y, 0, self.wall(self, y, 0))
            self.field.set_cell(y, self.field.width - 1, self.wall(self, y, self.field.width - 1))

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
            pass
        else:
            self.snake.turn(side)

    def update(self):
        if self.is_paused or self.is_dead:
            return

        self.snake.real_direction = self.snake.direction

        cell_next = self.field.get_cell(*self.snake.get_next_head())
        if type(cell_next) is DeathWallCell:
            cell_next.on_bump(self)
            return

        if not self.try_move_head():
            self.is_dead = True
            return

        cell = self.field.get_cell(*self.snake.head)
        if cell is not None:
            cell.on_bump(self)

        self.field.set_cell(*self.snake.head, SnakeCell(time_to_live=self.snake.len))
        # Костыль. Зато обновление длины змейки происходит на клетке с едой, а не на следующей

        if self.is_dead:
            if self.snake.len >= self.field.get_field_square() - 1:
                self.is_won = True
            return

        self.field.update(game=self)

        self.field.set_cell(*self.snake.head, SnakeCell(time_to_live=self.snake.len))

    def try_move_head(self):
        new_y, new_x = self.snake.get_next_position()
        if self.field.contains_cell(new_y, new_x):
            self.snake.head = new_y, new_x
            return True
        return False

    def restart(self, settings=None):
        if settings is None:
            settings = Settings(width=self.field.width, height=self.field.height, wall=self.wall)
        self.__init__(settings)

    def get_direction(self, dy, dx):
        pass
