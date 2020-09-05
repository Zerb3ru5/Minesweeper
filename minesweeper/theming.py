from kivy.graphics import Color


class Theme:
    themes = {
        'light': [
            [214 / 255, 214 / 255, 214 / 255, 1],  # primary color
            [214 / 255, 214 / 255, 214 / 255, 0.5],  # accent color of primary color
            [0.1, 0.1, 0.1, 1],  # secondary color
            [0.1, 0.1, 0.1, 0.5]  # accent color of the secondary color
        ],
        'dark': [
            [18 / 255, 18 / 255, 18 / 255, 1],
            [18 / 255, 18 / 255, 18 / 255, 0.8],
            [0.9, 0.9, 0.9, 1],
            [0.9, 0.9, 0.9, 0.5]
        ]
    }

    def __init__(self, current):
        self.current = current

    def get_primary(self):
        return self.themes[self.current][0]

    def get_primary_accent(self):
        return self.themes[self.current][1]

    def get_secondary(self):
        return self.themes[self.current][2]

    def get_secondary_accent(self):
        return self.themes[self.current][3]

    def make_color(self, color):
        return Color(color[0], color[1], color[2], color[3])
