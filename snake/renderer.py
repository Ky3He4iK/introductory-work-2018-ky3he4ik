from PyQt5.QtGui import QColor


class Renderer:
    def __init__(self, painter):
        self.painter = painter

    def render(self, field):
        square_size = self.get_square_size(field)

        for i in range(field.height):
            for j in range(field.width):
                cell = field.get_cell(i, j)
                if cell is not None:
                    self.draw_square(j * square_size[0], i * square_size[1], square_size, cell.color)

    def get_square_size(self, field):
        rect = self.painter.window()
        return rect.width() // field.width, rect.height() // field.height

    def draw_square(self, x, y, size, color):
        width, height = size
        color = QColor(color)

        painter = self.painter
        painter.fillRect(x + 1, y + 1, width - 2,
                         height - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + height - 1, x, y)
        painter.drawLine(x, y, x + width - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + height - 1,
                         x + width - 1, y + height - 1)
        painter.drawLine(x + width - 1,
                         y + height - 1, x + width - 1, y + 1)
