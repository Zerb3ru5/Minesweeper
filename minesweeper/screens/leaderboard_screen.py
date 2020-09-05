from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.core.window import Window

from minesweeper.widgets.leaderboard import Entry, Leaderboard, NameAdder

from minesweeper.widgets.settings import SettingsGroup, SettingName, SettingLabel


class LeaderboardScreen(Screen):
    def __init__(self, theme, **kwargs):
        super(LeaderboardScreen, self).__init__(**kwargs)

        # a list of all entries (if access needed e.g. for theme change)
        self.entries = Leaderboard(theme=theme)
        print('entries = ', self.entries)

        # the main container
        self.root = BoxLayout(orientation='vertical')

        # the top bar with the back button
        bar = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[150, 50], padding=[20, -20])
        self.back_button = Button(
            size_hint=[None, None],
            size=[50, 50],
            on_release=lambda n: self.change_to_menu(),
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_pressed_{theme.current}.png'
        )
        bar.add_widget(self.back_button)
        self.root.add_widget(bar)

        # to display a nice heading
        self.heading = Label(
            text='Leaderboard',
            font_size='50sp',
            font_name='gothic',
            color=theme.get_secondary(),
            halign='center',
            valign='bottom',
            padding_y=20,
            size_hint=[1, None],
            size=[150, 150]
        )
        self.heading.bind(size=self.heading.setter('text_size'))
        self.root.add_widget(self.heading)

        # center the scrollview
        test = AnchorLayout(anchor_x='center')

        # to make the panel scrollable
        settings = ScrollView(
            size_hint=[None, 1],
            size=[450, 50],
            bar_color=[0, 0, 0, 0],
            bar_inactive_color=[0, 0, 0, 0]
        )

        # to place the entries beneath each other
        self.entry_list = GridLayout(cols=1, size_hint_y=None)
        self.entry_list.bind(minimum_height=self.entry_list.setter('height'))

        # add the entries from the file subsequently
        for entry in self.entries:
            print(entry)
            self.entry_list.add_widget(entry)

        settings.add_widget(self.entry_list)
        test.add_widget(settings)
        self.root.add_widget(test)
        self.add_widget(self.root)

    def update_list(self):
        self.entry_list.clear_widgets()
        for entry in self.entries:
            # print(entry)
            self.entry_list.add_widget(entry)

    def change_to_menu(self):
        self.manager.current = 'menu_screen'

    # UNIVERSAL: to update the theme when switched
    def apply_theme(self, theme):
        self.heading.color = theme.get_secondary()
        for entry in self.entries:
            entry.apply_theme(theme)

        # recolor buttons
        self.back_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_normal_{theme.current}.png'
        self.back_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_pressed_{theme.current}.png'