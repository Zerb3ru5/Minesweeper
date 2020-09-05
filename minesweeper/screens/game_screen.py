from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from minesweeper.widgets.core.minesweeper import Minesweeper
from minesweeper.widgets.burger import BurgerButton
from minesweeper.widgets.clock import GameClock


class GameScreen(Screen):
    def __init__(self, theme, grid_size, mines_percentage, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.root = BoxLayout(orientation='vertical')

        # the bar that contains the burger button and the stopwatch
        self.bar = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[500, 50], padding=[20, -20])

        # the burger button
        self.burger = Button(
            size=[50, 50],
            size_hint=[None, None],
            on_release=lambda n: self.change_to_settings(),
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/pause_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/pause_button_pressed_{theme.current}.png'
        )
        self.bar.add_widget(self.burger)

        # the stopwatch
        self.stopwatch = GameClock(theme=theme)
        self.bar.add_widget(self.stopwatch)

        # the layout that centers the game
        self.game = AnchorLayout(anchor_x='center', anchor_y='center')

        # the game
        self.weeper = Minesweeper(all=self, theme=theme, grid_size=grid_size, mines_percent=mines_percentage/100, size_hint=[None, 0.9])
        self.weeper.bind(height=self.weeper.setter('width'))
        self.game.add_widget(self.weeper)

        self.root.add_widget(self.bar)
        self.root.add_widget(self.game)
        self.add_widget(self.root)

    def change_to_settings(self):
        self.stopwatch.stop()
        self.manager.current = 'pause_screen'

    def redraw(self, *args):
        self.rect.pos = self.stopwatch.pos
        self.rect.size = (self.stopwatch.width, self.stopwatch.height)

    def reset_game(self):
        self.weeper.reset_game()
        self.stopwatch.reset()

    def apply_theme(self, theme):
        self.stopwatch.color = theme.get_secondary_accent()
        self.weeper.reset_game()

        # recolor buttons
        self.burger.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/pause_button_normal_{theme.current}.png'
        self.burger.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/pause_button_pressed_{theme.current}.png'

    def game_over(self, time):
        self.manager.get_screen('game_over_screen').info.text = self.stopwatch.time_to_string(time[0], time[1]) + ' min'
        self.manager.get_screen('game_over_screen').minutes = time[0]
        self.manager.get_screen('game_over_screen').seconds = time[1]
        self.manager.get_screen('game_over_screen').order = 'lost'

        # look if the entry would fit into the leaderboard and show the leaderboard button accordingly
        if self.manager.get_screen('leaderboard_screen').entries.fits_in_leaderboard(time):
            self.manager.get_screen('game_over_screen').add_leaderboard_button()
        else:
            self.manager.get_screen('game_over_screen').remove_leaderboard_button()

        self.manager.current = 'game_over_screen'
