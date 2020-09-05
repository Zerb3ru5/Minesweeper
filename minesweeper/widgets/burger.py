from kivy.uix.button import Button


class BurgerButton(Button):
    def __init__(self, **kwargs):
        super(BurgerButton, self).__init__(**kwargs)
        self.background_normal = 'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/burger.png'

