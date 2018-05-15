from .renderer import COLORS
from .resourceClasses import TurnEnum


class Cell:
    color = 'black'

    def update(self, game, directions):
        return self

    def on_bump(self, game):
        pass


class SnakeCell(Cell):
    color = COLORS.GREEN

    def __init__(self, time_to_live, direction):
        self.time_to_live = time_to_live
        self.direction = direction

    def update(self, game, directions):
        if self.time_to_live == 0:
            game.is_dead = True
            return
        if self.time_to_live == 1:
            return None
        directions[self.time_to_live - 1] = self.direction
        return SnakeCell(self.time_to_live - 1, directions[self.time_to_live - 1])

    def on_bump(self, game):
        game.is_dead = True


class FoodCell(Cell):
    color = COLORS.YELLOW

    def __init__(self):
        self.is_eaten = False

    def on_bump(self, game):
        self.is_eaten = True
        game.snake.len += 1
        game.score += 1
        game.spawn_food()

    def update(self, game, directions):
        return None if self.is_eaten else self


class PoisonCell(Cell):
    color = COLORS.TURQUOISE

    def __init__(self):
        self.is_eaten = False

    def on_bump(self, game):
        self.is_eaten = True
        game.snake.len -= 1
        game.score -= 2
        game.spawn_poison_food()

    def update(self, game, directions):
        return None if self.is_eaten else self


class SuicideCell(Cell):
    color = COLORS.RED

    def on_bump(self, game):
        game.is_dead = True

    def update(self, game, directions):
        return self


class DeathWallCell(Cell):
    color = COLORS.GREY

    def on_bump(self, game):
        game.is_dead = True


class ReverseWallCell(Cell):
    color = COLORS.BROWN

    def on_bump(self, game):
        game.reverse_snake(TurnEnum.get_reversed(game.snake.direction))
