class TurnEnum:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    @staticmethod
    def get_reversed(direction):
        if direction == TurnEnum.RIGHT:
            return TurnEnum.LEFT
        elif direction == TurnEnum.LEFT:
            return TurnEnum.RIGHT
        elif direction == TurnEnum.UP:
            return TurnEnum.DOWN
        elif direction == TurnEnum.DOWN:
            return TurnEnum.UP


class COLORS:
    GREY = 0x666666
    RED = 0xCC6666
    GREEN = 0x66CC66
    BLUE = 0x6666CC
    BROWN = 0xCCCC66
    PURPLE = 0xCC66CC
    TURQUOISE = 0x66CCCC
    YELLOW = 0xDAAA00
    LIGHT_GREEN = 0x5CFF5C
    WHITE = 0xFFFFFF
