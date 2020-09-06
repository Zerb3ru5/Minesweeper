from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

from kivy.graphics import Line
from kivy.graphics import Color

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.core.window import Window

from minesweeper.widgets.leaderboard import NameAdder, NameAdderButton


class VictoryScreen(Screen):

    minutes = int()
    seconds = int()
    order = ''

    leaderboard_button_visible = True

    def __init__(self, theme, **kwargs):
        super(VictoryScreen, self).__init__(**kwargs)

        self.theme = theme
        self.name_adder = NameAdder(theme=theme)

        self.root = AnchorLayout(anchor_x='center', anchor_y='center')

        # make a green line on the ground (to have some style on the winners page ;))
        with self.root.canvas:
            self.color = Color(0, 255, 0, 1)
            self.line = Line(points=[50, 50, Window.width - 50, 50])
        self.root.bind(pos=self.redraw, size=self.redraw)

        self.anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.box = BoxLayout(orientation='vertical', size_hint=[1, None], size=[10, 210])
        self.box.bind(minimum_size=self.box.setter('size'))

        self.paused_label = Label(
            text='Victory',
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
        self.box.add_widget(self.paused_label)

        self.info = Label(
            text='dummy',
            font_size='25sp',
            font_name='gothic',
            color=theme.get_secondary(),
            halign='center',
            valign='bottom',
            padding_y=15,
            size_hint=[1, None],
            size=[150, 40]
        )
        self.info.bind(size=self.info.setter('text_size'))
        self.box.add_widget(self.info)

        # the button to go to the menu screen
        quit_layout = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=[1, None], size=[15, 65])
        self.quit_button = Button(
            text='Back to menu',
            size_hint=[None, None],
            size=[150, 50],
            font_name='gothic',
            font_size='16sp',
            color=[0.9, 0.9, 0.9, 1],
            padding_y=50,
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png',
            on_release=lambda n: self.change_to_menu()
        )
        quit_layout.add_widget(self.quit_button)
        self.box.add_widget(quit_layout)

        # the add button for the leaderboard
        self.to_leaderboard_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=[1, None], size=[15, 70])
        self.to_leaderboard_button = NameAdderButton(theme, self.box)

        # add the bindings of the submit button (translate the data to the leaderboard)
        self.to_leaderboard_button.name_adder.submit.on_release = lambda: self.add_to_leaderboard(
            name=self.to_leaderboard_button.name_adder.input.text,
            minutes=self.minutes,
            seconds=self.seconds,
            order=self.order
        )

        self.to_leaderboard_layout.add_widget(self.to_leaderboard_button)
        self.box.add_widget(self.to_leaderboard_layout)

        self.anchor.add_widget(self.box)
        self.root.add_widget(self.anchor)

        self.add_widget(self.root)

    def add_leaderboard_button(self):
        if not self.leaderboard_button_visible:
            self.to_leaderboard_layout.add_widget(self.to_leaderboard_button)
            self.leaderboard_button_visible = True

    def remove_leaderboard_button(self):
        if self.leaderboard_button_visible:
            self.to_leaderboard_layout.remove_widget(self.to_leaderboard_button)

            # remove also the the name adder field
            self.to_leaderboard_button.reset_button()

            self.leaderboard_button_visible = False

    def add_to_leaderboard(self, name, minutes, seconds, order):
        if not name == '':
            print('Leaderboard entry: ', name, minutes, seconds, order)
            self.manager.get_screen('leaderboard_screen').entries.append([name, minutes, seconds, order])
            self.manager.get_screen('leaderboard_screen').update_list()
            self.change_to_leaderboard()

    def change_to_menu(self):
        # reset the leaderboard button
        self.to_leaderboard_button.reset_button()

        self.manager.get_screen('game_screen').reset_game()
        self.manager.current = 'menu_screen'

    def change_to_leaderboard(self):
        # reset the leaderboard button
        self.to_leaderboard_button.reset_button()

        self.manager.get_screen('game_screen').reset_game()
        self.manager.current = 'leaderboard_screen'

    def redraw(self, *args):
        self.line.points = [50, 50, Window.width - 50, 50]

    def apply_theme(self, theme):
        self.paused_label.color = theme.get_secondary()
        self.info.color = theme.get_secondary_accent()
        self.to_leaderboard_button.name_adder.apply_theme(theme)

        # recolor the button
        self.quit_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.quit_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'
        self.to_leaderboard_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'
        self.to_leaderboard_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
