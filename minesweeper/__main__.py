from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition

from minesweeper.screens.menu_screen import MenuScreen
from minesweeper.screens.game_screen import GameScreen
from minesweeper.screens.pause_screen import PauseScreen
from minesweeper.screens.settings_screen import SettingsScreen
from minesweeper.screens.game_over_screen import GameOverScreen
from minesweeper.screens.victory_screen import VictoryScreen
from minesweeper.screens.leaderboard_screen import LeaderboardScreen

from minesweeper.theming import Theme

import json


class Main(FloatLayout):
    def  __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

        # load in the settings from the settings.json file
        with open('saves\settings.json', 'r') as settings_file:
            settings_data = json.load(settings_file)

        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')

        self.content = ScreenManager()
        self.content.transition = NoTransition()

        theme = Theme(settings_data['theme'])

        # set the background color
        Window.clearcolor = theme.get_primary()

        self.content.add_widget(MenuScreen(name='menu_screen', theme=theme))
        self.content.add_widget(GameScreen(name='game_screen', theme=theme, grid_size=settings_data['grid_size'], 
                                           mines_percentage=settings_data['mines_percentage']))
        self.content.add_widget(PauseScreen(name='pause_screen', theme=theme))
        self.content.add_widget(GameOverScreen(name='game_over_screen', theme=theme))
        self.content.add_widget(VictoryScreen(name='victory_screen', theme=theme))
        self.content.add_widget(LeaderboardScreen(name='leaderboard_screen', theme=theme))
        self.content.add_widget(SettingsScreen(name='settings_screen', theme=theme, data=settings_data))

        self.screens.add_widget(self.content)
        self.add_widget(self.screens)


class MinesweeperApp(App):
    def build(self):
        self.icon = 'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/logo/icon.png'
        return Main()


if __name__ == '__main__':
    Config.set('graphics', 'resizable', 1)
    Config.set('graphics', 'width', '730')
    Config.set('graphics', 'height', '810')
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.write()
    MinesweeperApp().run()