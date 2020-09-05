from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Rectangle, Line, Color


class SettingsGroup(AnchorLayout):

    theme = None

    def __init__(self, theme, name='<SettingsGroup>', size_y=450, **kwargs):
        super(SettingsGroup, self).__init__(
            anchor_x='center',
            size_hint=[1, None],
            size=[350, size_y],
            **kwargs)

        self.theme = theme

        self.root = BoxLayout(
            orientation='vertical',
            size_hint=[None, None],
            size=[450, size_y],
            spacing=5
        )
        # self.root.bind(minimum_size=self.root.setter('size'))

        self.label = Label(
            text=name,
            font_size='16sp',
            font_name='gothic',
            color=theme.get_secondary_accent(),
            halign='left',
            valign='center'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.root.add_widget(self.label)

        # with self.label.canvas:
        with self.label.canvas:
            self.color = theme.make_color(theme.get_secondary_accent())
            # self.background = Rectangle(pos=self.label.pos, size=(self.label.width, self.label.height))
            self.separator = Line(points=[self.label.pos[0], self.label.pos[1], self.label.width, self.label.pos[1]],
                                  width=1)
        self.label.bind(pos=self.redraw, size=self.redraw)

        self.add_widget(self.root)

    def add_setting(self, name, interaction_object):
        print(interaction_object.size)
        settings = BoxLayout(orientation='horizontal', size_hint=[1, None], size=interaction_object.size, padding=[20, 5])
        naming_label = Label(
            text=name,
            font_size='16sp',
            font_name='gothic',
            color=self.theme.get_secondary(),
            halign='left',
            valign='center'
        )
        naming_label.bind(size=naming_label.setter('text_size'))
        settings.add_widget(naming_label)
        settings.add_widget(interaction_object)
        self.root.add_widget(settings)

    def redraw(self, *args):
        self.color.rgba = self.theme.get_secondary_accent()
        self.separator.points = [self.label.pos[0], self.label.pos[1], self.label.pos[0] + self.label.width, self.label.pos[1]]

    def apply_theme(self, theme):
        self.theme = theme
        self.label.color = theme.get_secondary_accent()

        self.color.rgba = theme.get_secondary_accent()
        self.separator.points = [self.label.pos[0], self.label.pos[1], self.label.pos[0] + self.label.width,
                                 self.label.pos[1]]


class SettingName(Label):
    def __init__(self, theme, name, **kwargs):
        super(SettingName, self).__init__(**kwargs)

        self.text = name
        self.font_size = '16sp'
        self.font_name = 'gothic'
        self.color = theme.get_secondary()
        self.halign = 'left'
        self.valign = 'center'
        self.bind(size=self.setter('text_size'))
        # self.bind(texture_size=self.setter('size'))


class SettingLabel(Label):
    def __init__(self, theme, **kwargs):
        super(SettingLabel, self).__init__(**kwargs)

        self.font_size = '16sp'
        self.font_name = 'gothic'
        self.color = theme.get_secondary()
        self.halign = 'right'
        self.valign = 'center'
        # self.padding_y = 2
        self.bind(size=self.setter('text_size'))
        # self.bind(texture_size=self.setter('size'))
