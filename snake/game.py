from .field import Field
from .cells import SnakeCell, FoodCell, DeathWallCell, PoisonCell


class TurnEnum:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


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

    def turn(self, direction):
        if direction not in self.TURNS.keys():
            raise ValueError('{0} is not a valid side' % direction)
        self.direction = direction

    def get_next_position(self):
        dy, dx = self.TURNS[self.direction]
        return self.head[0] + dy, self.head[1] + dx


class Game:
    def __init__(self, width=20, height=20):
        self.field = Field(width, height)
        self.snake = SnakeState((1, 2), 2, 'right')

        self.is_paused = True
        self.is_dead = False
        self.score = 0

        self.init_level()

    def init_level(self):
        self.field.set_cell(1, 1, SnakeCell(time_to_live=1))
        self.field.set_cell(1, 2, SnakeCell(time_to_live=2))

        for x in range(self.field.width):
            self.field.set_cell(0, x, DeathWallCell())
            self.field.set_cell(self.field.width - 1, x, DeathWallCell())

        for y in range(self.field.height):
            self.field.set_cell(y, 0, DeathWallCell())
            self.field.set_cell(y, self.field.height - 1, DeathWallCell())

        self.spawn_food()
        self.spawn_poison_food()
        self.spawn_suicide_food()

    def spawn_food(self):
        y, x = self.field.get_random_empty_cell()
        self.field.set_cell(y, x, FoodCell())

    def spawn_poison_food(self):
        y, x = self.field.get_random_empty_cell()
        self.field.set_cell(y, x, PoisonCell())

    def spawn_suicide_food(self):
        self.field.change_suicide_cell()

    def pause(self):
        self.is_paused = not self.is_paused

    def turn(self, side):
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

        self.field.set_cell(*self.snake.head, SnakeCell(time_to_live=self.snake.len))
        # Костыль. Зато обновление длины змейки происходит в тот же тик, а не следующий
        # TODO: придумать замену этому костылю

        if self.is_dead:
            return

        self.field.update(game=self)

        self.field.set_cell(*self.snake.head, SnakeCell(time_to_live=self.snake.len))

    def try_move_head(self):
        new_y, new_x = self.snake.get_next_position()

        if self.field.contains_cell(new_y, new_x):
            self.snake.head = new_y, new_x
            return True
        return False

    def restart(self):
        self.__init__(self.field.width, self.field.height)
