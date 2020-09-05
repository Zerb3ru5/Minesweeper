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

import math
import json

from minesweeper.widgets.settings import SettingsGroup, SettingName, SettingLabel


class SettingsScreen(Screen):
    def __init__(self, theme, data, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # the main container
        self.root = BoxLayout(orientation='vertical')

        # the top bar with the back button
        bar = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[150, 50], padding=[20, -20])
        self.back_button = Button(
            size_hint=[None, None],
            size=[50, 50],
            on_release=lambda n: self.change_to_menu(theme),
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_pressed_{theme.current}.png'
        )
        bar.add_widget(self.back_button)
        self.root.add_widget(bar)

        # to display a nice heading
        self.heading = Label(
            text='Settings',
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

        # to make the settings panel scrollable
        settings = ScrollView(
            size_hint=[1, 1]
        )
        # to place the settings groups beneath each other
        settings_gridlayout = GridLayout(cols=1, size_hint_y=None)
        settings_gridlayout.bind(minimum_height=settings_gridlayout.setter('height'))

        # setup the group for the general game settings
        self.game_group = SettingsGroup(name='Game settings', theme=theme, size_y=180)

        # the grid size settings
        grid_size_setting = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[50, 50], padding=[20, 0])
        self.grid_size_setting_name = SettingName(name='Grid size', theme=theme, size_hint=[0.33, None], size=[150, 50])
        self.grid_size_setting_value = SettingLabel(text='15', theme=theme, size_hint=[0.1, None], size=[30, 50],
                                                    halign='right')
        self.grid_size_setting_slider = Slider(
            min=3,
            max=20,
            step=1,
            on_touch_up=lambda instance, touch: self.grid_size_setting_change(self.grid_size_setting_slider,
                                                                              self.grid_size_setting_value, instance,
                                                                              touch),
            on_touch_move=lambda instance, touch: self.grid_size_setting_update_value_label(
                self.grid_size_setting_slider,
                self.grid_size_setting_value,
                instance, touch),
            value=data['grid_size'])
        grid_size_setting.add_widget(self.grid_size_setting_name)
        grid_size_setting.add_widget(self.grid_size_setting_slider)
        grid_size_setting.add_widget(self.grid_size_setting_value)
        self.game_group.root.add_widget(grid_size_setting)

        # the mines percentage settings
        mines_percentage_setting = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[50, 50],
                                             padding=[20, 0])
        self.mines_percentage_setting_name = SettingName(name='Mines percentage', theme=theme, size_hint=[0.8, None],
                                                         size=[150, 50])
        self.mines_percentage_setting_value = SettingLabel(text='15%', theme=theme, size_hint=[0.2, None],
                                                           size=[30, 50], halign='right')
        self.mines_percentage_setting_slider = Slider(
            min=1,
            max=50,
            step=1,
            on_touch_up=lambda instance, touch: self.mines_percentage_setting_change(
                self.mines_percentage_setting_slider,
                self.mines_percentage_setting_value,
                instance, touch),
            on_touch_move=lambda instance, touch: self.mines_percentage_setting_update_value_label(
                self.mines_percentage_setting_slider,
                self.mines_percentage_setting_value, instance, touch),
            value=data['mines_percentage'])
        mines_percentage_setting.add_widget(self.mines_percentage_setting_name)
        mines_percentage_setting.add_widget(self.mines_percentage_setting_slider)
        mines_percentage_setting.add_widget(self.mines_percentage_setting_value)
        self.game_group.root.add_widget(mines_percentage_setting)

        # self.game_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.game_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.game_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.game_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.game_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        settings_gridlayout.add_widget(self.game_group)

        # setup the group for the leaderboard settings
        self.leaderboard_group = SettingsGroup(name='Leaderboard', theme=theme, size_y=130)

        # the button to clear the leaderboard
        leaderboard_clear_setting = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=[1, None],
                                                 size=[50, 60], padding=[20, 5])

        self.leaderboard_clear_setting_button = Button(text='Clear leaderboard', font_name='gothic', font_size='16sp',
                                                       size_hint=[None, None], size=[250, 50],
                                                       on_release=self.clear_leaderboard, color=theme.get_secondary(),
                                                       background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png',
                                                       background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png', )

        leaderboard_clear_setting.add_widget(self.leaderboard_clear_setting_button)
        self.leaderboard_group.root.add_widget(leaderboard_clear_setting)

        # some placeholders
        # self.leaderboard_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.leaderboard_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.leaderboard_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.leaderboard_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.leaderboard_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        settings_gridlayout.add_widget(self.leaderboard_group)

        # setup the group for the dark mode settings
        self.dark_mode_group = SettingsGroup(name='Appearance', theme=theme, size_y=120)

        # the switch for the dark mode
        dark_mode_settings = BoxLayout(orientation='horizontal', size_hint=[1, None], size=[50, 50], padding=[20, 5])

        # get the state of the switch, according to the settings file
        if data['theme'] == 'light':
            dark_mode_state = False
        else:
            dark_mode_state = True

        self.dark_mode_settings_name = SettingName(name='Dark mode', theme=theme, size_hint=[1, None], size=[50, 50])
        self.dark_mode_setting_switch = Switch(active=dark_mode_state, size_hint=[0.3, None], size=[50, 50])
        self.dark_mode_setting_switch.bind(
            active=lambda instance, value: self.dark_mode_settings_change(theme, instance, value))

        dark_mode_settings.add_widget(self.dark_mode_settings_name)
        dark_mode_settings.add_widget(self.dark_mode_setting_switch)
        self.dark_mode_group.root.add_widget(dark_mode_settings)

        # some placeholders
        # self.dark_mode_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.dark_mode_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.dark_mode_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.dark_mode_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        # self.dark_mode_group.root.add_widget(Button(size_hint=[None, None], size=[450, 50]))
        settings_gridlayout.add_widget(self.dark_mode_group)

        settings.add_widget(settings_gridlayout)
        self.root.add_widget(settings)
        self.add_widget(self.root)

        # apply the given settings
        # self.apply_settings(data)
        

    def change_to_menu(self, theme):
        self.save_settings(theme)
        self.manager.current = 'menu_screen'

    # GRID SIZE SETTINGS
    # grid size settings, fired when the mouse leaves the slider
    def grid_size_setting_change(self, slider, label, instance, touch):
        if instance.collide_point(*touch.pos):
            print('current grid size', slider.value)
            self.manager.get_screen('game_screen').weeper.reset_game(grid_size=slider.value)
            label.text = str(slider.value)

            #  calculate the least possible value for the mines percentage slider (so that there is always 1 mine in the
            #  field)
            least_mine_percentage = math.ceil(
                (1 * 100) / (self.grid_size_setting_slider.value * self.grid_size_setting_slider.value))

            # apply the value to the slider
            self.mines_percentage_setting_slider.min = least_mine_percentage
            self.mines_percentage_setting_slider.step = least_mine_percentage

            # set the value to the value nearest to 15%
            self.mines_percentage_setting_slider.value = ((50 - (50 % least_mine_percentage)) * 0.3) - (
                    (50 - (50 % least_mine_percentage)) * 0.3) % least_mine_percentage

            # apply the new value to the minesweeper game and change the value displayed on the side
            self.manager.get_screen('game_screen').weeper.reset_game(
                mines_percent=self.mines_percentage_setting_slider.value / 100)
            self.mines_percentage_setting_value.text = str(self.mines_percentage_setting_slider.value) + '%'

    # fired when the slider is moved
    def grid_size_setting_update_value_label(self, slider, label, instance, touch):
        if instance.collide_point(*touch.pos):
            label.text = str(slider.value)

    # MINES PERCENTAGE SETTINGS
    # fired when the slider is moved
    def mines_percentage_setting_change(self, slider, label, instance, touch):
        if instance.collide_point(*touch.pos):
            print('current mines percent', slider.value / 100)
            self.manager.get_screen('game_screen').weeper.reset_game(mines_percent=slider.value / 100)
            label.text = str(slider.value) + '%'

    # fired when the mouse leaves the slider
    def mines_percentage_setting_update_value_label(self, slider, label, instance, touch):
        print(instance)
        if instance.collide_point(*touch.pos):
            label.text = str(slider.value) + '%'

    # CLEAR LEADERBOARD SETTINGS
    # fires when the button is released, deletes the whole leaderboard
    def clear_leaderboard(self, *args):
        self.manager.get_screen('leaderboard_screen').entries.clear_all()
        self.manager.get_screen('leaderboard_screen').update_list()

    # DARK MODE SETTINGS
    # fired when the switch is activated
    def dark_mode_settings_change(self, theme, instance, value):
        print(value)
        if value:
            theme.current = 'dark'
        else:
            theme.current = 'light'

        Window.clearcolor = theme.get_primary()
        self.apply_theme(theme)

    # UNIVERSAL: to update the theme when switched
    def apply_theme(self, theme):
        self.heading.color = theme.get_secondary()

        self.game_group.apply_theme(theme)
        self.grid_size_setting_name.color = theme.get_secondary()
        self.grid_size_setting_value.color = theme.get_secondary()
        self.grid_size_setting_slider.color = theme.get_secondary()

        self.mines_percentage_setting_name.color = theme.get_secondary()
        self.mines_percentage_setting_value.color = theme.get_secondary()
        self.mines_percentage_setting_slider.color = theme.get_secondary()

        self.leaderboard_group.apply_theme(theme)
        self.leaderboard_clear_setting_button.color = theme.get_secondary()

        # recolor button
        self.leaderboard_clear_setting_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.leaderboard_clear_setting_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'

        self.back_button.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_normal_{theme.current}.png'
        self.back_button.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/return_button_pressed_{theme.current}.png'

        self.dark_mode_group.apply_theme(theme)
        self.dark_mode_settings_name.color = theme.get_secondary()

        self.manager.get_screen('menu_screen').apply_theme(theme)
        self.manager.get_screen('game_screen').apply_theme(theme)
        self.manager.get_screen('pause_screen').apply_theme(theme)
        self.manager.get_screen('game_over_screen').apply_theme(theme)
        self.manager.get_screen('leaderboard_screen').apply_theme(theme)

    # save the current settings
    def save_settings(self, theme):
        data = {}
        data['grid_size'] = self.grid_size_setting_slider.value
        data['mines_percentage'] = self.mines_percentage_setting_slider.value
        data['theme'] = theme.current

        with open('saves\settings.json', 'w') as settings_file:
            json.dump(data, settings_file)
