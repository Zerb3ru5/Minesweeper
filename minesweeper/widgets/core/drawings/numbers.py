from kivy.graphics import InstructionGroup

from kivy.graphics import Color


class One(InstructionGroup):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)

        self.add(theme.make_color(theme.get_secondary_accent()))
