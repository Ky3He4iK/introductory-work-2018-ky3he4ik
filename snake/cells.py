from .resourceClasses import COLORS


class Cell:
    color = 'black'

    def update(self, game):
        return self

    def on_bump(self, game):
        pass


class SnakeCell(Cell):
    color = COLORS.GREEN

    def __init__(self, time_to_live):
        self.time_to_live = time_to_live

    def update(self, game):
        if self.time_to_live == 0:
            game.is_dead = True
            return
        if self.time_to_live == 1:
            return None
        return SnakeCell(self.time_to_live - 1)

    def on_bump(self, game):
        if self.time_to_live > 1:
            game.is_dead = True


class FoodCell(Cell):
    color = COLORS.YELLOW

    def __init__(self):
        self.is_eaten = False

    def on_bump(self, game):
        self.is_eaten = True
        game.snake.len += 1
        game.score += 1
        game.field.change_food_cell()

    def update(self, game):
        return None if self.is_eaten else self


class PoisonCell(Cell):
    color = COLORS.TURQUOISE

    def __init__(self):
        self.is_eaten = False

    def on_bump(self, game):
        # pass
        self.is_eaten = True
        game.snake.len -= 1
        game.score -= 2
        game.spawn_poison_food()

    def update(self, game):
        return None if self.is_eaten else self


class SuicideCell(Cell):
    color = COLORS.RED

    def on_bump(self, game):
        # pass
        game.is_dead = True

    def update(self, game):
        return self


class Wall(Cell):
    def __init__(self, game, y, x):
        pass


class DeathWallCell(Wall):
    """Snake will die on bump"""
    color = COLORS.GREY

    def on_bump(self, game):
        game.is_dead = True


class RubberWallCell(Wall):
    """This wall reverse snake if bump"""
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        raise SyntaxError("Not implemented")


class PortalWallCell(Wall):
    """Snake's head will be moved to opposite side"""
    color = COLORS.PURPLE

    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        if x == 0:
            self.to = (y, game.field.width - 2)
        elif y == 0:
            self.to = (game.field.height - 2, x)
        elif x == game.field.width - 1:
            self.to = (y, 1)
        elif y == game.field.height - 1:
            self.to = (1, x)
        else:
            self.to = (y, x)

    def on_bump(self, game):
        game.snake.head = self.to


class InvertedPortalWallCell(PortalWallCell):
    """Like simple portal sell but x or y will be inverted"""
    def __init__(self, game, y, x):
        super().__init__(game, y, x)
        if x == 0:
            self.to = (game.field.height - y - 1, game.field.width - 2)
        elif y == 0:
            self.to = (game.field.height - 2, game.field.width - x - 1)
        elif x == game.field.width - 1:
            self.to = (game.field.height - y - 1, 1)
        elif y == game.field.height - 1:
            self.to = (1, game.field.width - x - 1)
        else:
            self.to = (y, x)


class WallCells:
    Death = DeathWallCell
    Reverse = RubberWallCell

    class Portals:
        Simple = PortalWallCell
        Inverted = InvertedPortalWallCell
