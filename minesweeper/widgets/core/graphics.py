from kivy.graphics import InstructionGroup

from kivy.graphics import Color
from kivy.graphics import Line, Rectangle


class Mine(InstructionGroup):
    def __init__(self, theme, pos, size, **kwargs):
        super(Mine, self).__init__(**kwargs)

        self.color = theme.make_color(theme.get_secondary())
        print(self.color)

        self.x1 = Line(points=[pos[0] + 10, pos[1] + 10, pos[0] + size[0] - 10,
                               pos[1] + size[1] - 10])

        self.x2 = Line(points=[pos[0] + size[0] - 10, pos[1] + 10, pos[0] + 10,
                               pos[1] + size[1] - 10])

        self.add(self.color)
        self.add(self.x1)
        self.add(self.x2)

    def redraw(self, theme, pos, size):
        self.color.rgba = theme.get_secondary()
        self.x1.points = [pos[0] + 10, pos[1] + 10, pos[0] + size[0] - 10, pos[1] + size[1] - 10]
        self.x2.points = [pos[0] + size[0] - 10, pos[1] + 10, pos[0] + 10, pos[1] + size[1] - 10]


class Flag(InstructionGroup):
    def __init__(self, theme, pos, size, **kwargs):
        super(Flag, self).__init__(**kwargs)

        self.color = theme.make_color(theme.get_secondary())

        self.stick = Line(
            points=[pos[0] + size[0] - (size[0] / 5 * 2), pos[1] + (size[1] / 10), pos[0] + size[0] - (size[0] / 5 * 2),
                    pos[1] + size[1] - (size[1] / 6)], width=size[0] / 100)

        self.flag = Rectangle(pos=[pos[0] + size[0] / 4, pos[1] + size[1] / 2.3], size=[size[0] / 4 * 2, size[1] / 3])

        self.add(self.color)
        self.add(self.stick)
        self.add(self.flag)

    def redraw(self, theme, pos, size):
        self.color.rgba = theme.get_secondary()
        self.stick.points = [pos[0] + size[0] - (size[0] / 5 * 2), pos[1] + (size[1] / 10),
                             pos[0] + size[0] - (size[0] / 5 * 2),
                             pos[1] + size[1] - (size[1] / 6)]
        self.stick.width = size[0] / 100
        self.flag.pos = [pos[0] + size[0] / 4, pos[1] + size[1] / 2.3]
        self.flag.size = [size[0] / 4 * 2, size[1] / 3]
