from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout


class MenuScreen(Screen):
    def __init__(self, theme, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.root = BoxLayout(orientation='vertical')

        # the settings button
        self.bar = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[150, 50], padding=[20, -20])
        self.settings_button = Button(
            size_hint=[None, None],
            size=[50, 50],
            on_release=lambda n: self.change_to_settings(),
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/settings_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/settings_button_pressed_{theme.current}.png'
        )
        self.bar.add_widget(self.settings_button)

        # the leaderboard button
        leaderboard_anchor = AnchorLayout(anchor_y='bottom', anchor_x='right', size_hint=[1, None])
        self.leaderboard_button = Button(
            size_hint=[None, None],
            size=[50, 50],
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/leaderboard_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/leaderboard_button_pressed_{theme.current}.png',
            on_release=lambda n: self.change_to_leaderboard()
        )
        leaderboard_anchor.add_widget(self.leaderboard_button)
        self.bar.add_widget(leaderboard_anchor)
        self.root.add_widget(self.bar)

        # add the logo
        self.logo = Label(
            text='Minesweeper',
            font_size='86sp',
            font_name='gothic',
            color=theme.get_secondary(),
            halign='center',
            valign='bottom')
        self.logo.bind(size=self.logo.setter('text_size'))
        self.logo.padding_y = 35
        self.root.add_widget(self.logo)

        # add the button to the game screen
        button_layout = AnchorLayout(anchor_y='top', anchor_x='center')
        self.game_button = Button(
            text='New game',
            size_hint=[None, None],
            size=[350, 100],
            font_name='gothic',
            font_size='26sp',
            color=[0.9, 0.9, 0.9, 1],
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/game_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/game_button_pressed_{theme.current}.png',
            on_release=lambda n: self.change_to_game())
        button_layout.add_widget(self.game_button)
        self.root.add_widget(button_layout)

        self.add_widget(self.root)

    def change_to_game(self):
        # self.manager.get_screen('game_screen').reset_game()
        self.manager.current = 'game_screen'
        self.manager.get_screen('game_screen').stopwatch.start()

    def change_to_settings(self):
        self.manager.current = 'settings_screen'

    def change_to_leaderboard(self):
        self.manager.current = 'leaderboard_screen'

    def apply_theme(self, theme):
        self.logo.color = theme.get_secondary()

        # recolor the buttons
        self.game_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/game_button_normal_{theme.current}.png'
        self.game_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/game_button_pressed_{theme.current}.png'

        self.leaderboard_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/leaderboard_button_normal_{theme.current}.png'
        self.leaderboard_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/leaderboard_button_pressed_{theme.current}.png'

        self.settings_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/settings_button_normal_{theme.current}.png'
        self.settings_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/settings_button_pressed_{theme.current}.png'
