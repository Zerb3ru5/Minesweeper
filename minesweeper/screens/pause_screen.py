from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout


class PauseScreen(Screen):
    def __init__(self, theme, **kwargs):
        super(PauseScreen, self).__init__(**kwargs)

        # to center the aligned items
        self.root = AnchorLayout(anchor_x='center', anchor_y='center')

        # to align the buttons and the label on the pause screen
        box = BoxLayout(orientation='vertical', spacing=35, size_hint=[1, None])
        box.bind(minimum_size=box.setter('size'))

        # the "paused" label
        self.paused_label = Label(
            text='Game paused',
            font_size='50sp',
            font_name='gothic',
            color=theme.get_secondary(),
            halign='center',
            valign='bottom',
            padding_y=10,
            size_hint=[1, None],
            size=[150, 60]
        )
        self.paused_label.bind(size=self.paused_label.setter('text_size'))
        box.add_widget(self.paused_label)

        # initialize the layout that keeps the continue button centered
        continue_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=[1, None], size=[150, 50])

        # the button to continue the game
        self.continue_button = Button(
            text='Continue',
            size_hint=[None, None],
            size=[150, 50],
            font_name='gothic',
            font_size='16sp',
            color=[0.9, 0.9, 0.9, 1],
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png',
            on_release=lambda n: self.change_to_game()
        )
        continue_layout.add_widget(self.continue_button)
        box.add_widget(continue_layout)

        # initialize the button that keeps the quit button centered
        quit_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=[1, None], size=[150, 50])

        # the button to quit the game and return to the menu
        self.quit_button = Button(
            text='Quit game',
            size_hint=[None, None],
            size=[150, 50],
            font_name='gothic',
            font_size='16sp',
            color=[0.9, 0.9, 0.9, 1],
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png',
            on_release=lambda n: self.change_to_menu()
        )
        quit_layout.add_widget(self.quit_button)
        box.add_widget(quit_layout)

        self.root.add_widget(box)
        self.add_widget(self.root)

    def change_to_game(self):
        self.manager.current = 'game_screen'
        self.manager.get_screen('game_screen').stopwatch.start()

    def change_to_menu(self):
        self.manager.get_screen('game_screen').reset_game()
        self.manager.current = 'menu_screen'

    def apply_theme(self, theme):
        self.paused_label.color = theme.get_secondary()

        # recolor the buttons
        self.continue_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.continue_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'
        self.quit_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.quit_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'
