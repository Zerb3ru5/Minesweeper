from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput

from kivy.graphics import Ellipse, Color, Line

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

import sqlite3


class Entry(BoxLayout):
    def __init__(self, theme, number, name, minutes, seconds, order, **kwargs):
        super(Entry, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint = [1, None]
        self.size = [150, 50]

        self.number = number
        self.name = name
        self.minutes = minutes
        self.seconds = seconds
        self.order = order

        # format the minutes and seconds values to a proper string displaying the time
        self.time = self.time_to_string(self.minutes, self.seconds)

        # the number to put the items into a specific sequence
        self.number_label = Label(
            text=str(self.number),
            font_size='20sp',
            font_name='gothic',
            color=theme.get_secondary_accent(),
            size_hint=[None, None],
            size=[50, 50]
        )
        self.number_label.bind(size=self.number_label.setter('text_size'))
        self.add_widget(self.number_label)

        # the label with the name of the player
        self.name_label = Label(
            text=self.name,
            font_name='gothic',
            font_size='25sp',
            halign='left',
            valign='center',
            color=theme.get_secondary(),
            size_hint=[1, None],
            size=[250, 50]
        )
        self.name_label.bind(size=self.name_label.setter('text_size'))
        self.add_widget(self.name_label)

        # the label with the time
        self.time_label = Label(
            text=self.time,
            font_size='20sp',
            font_name='gothic',
            valign='center',
            halign='right',
            color=theme.get_secondary(),
            size_hint=[None, None],
            size=[80, 50]
        )
        self.time_label.bind(size=self.time_label.setter('text_size'))
        self.add_widget(self.time_label)

        # the widget that can indicate to which one of the orders it belongs
        self.order_widget = Widget(
            size_hint=[None, None],
            size=[50, 50]
        )
        with self.order_widget.canvas:
            if self.order == 'lost':
                self.color = Color(255, 0, 0, 1)
            elif self.order == 'won':
                self.color = Color(0, 255, 0, 1)

            self.order_indicator = Ellipse(
                pos=[self.order_widget.pos[0] + 15, self.order_widget.pos[1] + 15],
                size=[20, 20]
            )
        self.order_widget.bind(pos=self.redraw, size=self.redraw)
        self.add_widget(self.order_widget)

        # the separator line
        with self.canvas:
            self.sep_color = theme.make_color(theme.get_secondary_accent())
            self.separator = Line(
                points=[self.pos[0] + 10, self.pos[1] + 10, self.pos[0] + self.width - 10, self.pos[1] + 10])

    def __repr__(self):
        return f'<Entry>'

    def redraw(self, *args):
        self.order_indicator.pos = [self.order_widget.pos[0] + 15, self.order_widget.pos[1] + 15]
        self.order_indicator.size = [20, 20]

        self.separator.points = [self.pos[0] + 42, self.pos[1] + 1, self.pos[0] + self.width - 10, self.pos[1] + 1]

    def time_to_string(self, minutes, seconds):
        min_str = str(minutes)
        if len(min_str) == 1:
            min_str = '0' + min_str

        sec_str = str(seconds)
        if len(sec_str) == 1:
            sec_str = '0' + sec_str

        return min_str + ':' + sec_str + ' min'

    def apply_theme(self, theme):
        self.number_label.color = theme.get_secondary_accent()
        self.name_label.color = theme.get_secondary()
        self.time_label.color = theme.get_secondary()
        self.sep_color.rgba = theme.get_secondary_accent()


# the class that bundles and manages all the entries (both the numerical and visual representations)
class Leaderboard(list):
    def __init__(self, theme):

        self.theme = theme

        # connect to the database
        self.conn = sqlite3.connect('C:/Users/Nutzer/PycharmProjects/Minesweeper/saves/leaderboard.db')
        self.c = self.conn.cursor()

        # to create the ground database if it does not exist
        self.c.execute(
            '''CREATE TABLE  IF NOT EXISTS entries (number INTEGER PRIMARY KEY, name TEXT, minutes INTEGER, 
            seconds INTEGER, ordering TEXT)''')
        self.conn.commit()

        # get all the sets in the database
        self.c.execute('SELECT * FROM entries')
        sets = self.c.fetchall()

        # create the visual representations for the entries in the leaderboard
        for entry_set in sets:
            super(Leaderboard, self).append(self.make_entry(
                number=entry_set[0],
                name=entry_set[1],
                minutes=entry_set[2],
                seconds=entry_set[3],
                order=entry_set[4]
            ))

    # create an entry, given a specific set
    def make_entry(self, number, name, minutes, seconds, order):
        entry = Entry(
            theme=self.theme,
            number=number,
            name=name,
            minutes=minutes,
            seconds=seconds,
            order=order
        )
        return entry

    # create a set, given an entry
    def make_set(self, entry):
        return list(entry.number, entry.name, entry.minutes, entry.seconds, entry.order)

    # the normal append function
    def append(self, entry):
        print('to add', entry)

        # make a set from the entry entity
        if type(entry) == list():
            print('reformat')
            entry_set = self.make_set(entry)
        else:
            entry_set = entry

        # fulfill the entry set
        entry_set.insert(0, len(self) + 1)
        print(entry_set)

        # add it to the database
        self.c.execute('''INSERT INTO entries (number, name, minutes, seconds, ordering) VALUES (?, ?, ?, ?, ?)''',
                       (entry_set[0], entry_set[1], entry_set[2], entry_set[3], entry_set[4]))
        self.conn.commit()

        # add it to the database
        # self.c.execute('''INSERT INTO entries (number, name, minutes, seconds, ordering) VALUES (?, ?, ?, ?, ?)''',
        #                (33, 'Ultra Funny Guy', 4, 20, 'won'))
        # self.conn.commit()

        # add it to the leaderboard
        super(Leaderboard, self).append(entry)

        # sort the whole list
        self.sort()

    def sort(self):
        self.c.execute('''SELECT * FROM entries''')
        data_sets = self.c.fetchall()

        # print('The data sets in the sort function', data_sets)

        # seperate the entries that were won from the ones that were lost
        won = []
        lost = []
        for data_set in data_sets:
            if data_set[4] == 'won':
                won.append(list(data_set))
            else:
                lost.append(list(data_set))

        # print('The games won: ', won, 'and the games lost', lost)

        # sort the two lists separately
        def sortFunc(element):
            return self.in_seconds(element)

        won.sort(key=sortFunc)
        lost.sort(key=sortFunc, reverse=True)

        # print('The sorted lists', won, lost)

        # delete all contents from the database
        self.c.execute('''DELETE FROM entries''')
        self.conn.commit()

        # rewrite the entries in the database
        index = 0
        for entry_list in [won, lost]:
            for entry_set in entry_list:
                index += 1
                if index < 11:
                    entry_set[0] = index
                    self.c.execute(
                        '''INSERT INTO entries (number, name, minutes, seconds, ordering) VALUES (?, ?, ?, ?, ?)''',
                        (entry_set[0], entry_set[1], entry_set[2], entry_set[3], entry_set[4]))
                    self.conn.commit()

        # delete all the visual representations
        super(Leaderboard, self).clear()

        # reload the visual representations of the entries
        sets = won + lost
        sets = sets[:10]
        for entry_set in sets:
            super(Leaderboard, self).append(self.make_entry(
                number=entry_set[0],
                name=entry_set[1],
                minutes=entry_set[2],
                seconds=entry_set[3],
                order=entry_set[4]
            ))

    def in_seconds(self, data_set):
        minutes = data_set[2]
        seconds = data_set[3]

        return minutes * 60 + seconds

    def fits_in_leaderboard(self, time):
        # checks if an entry would fit into the leaderboard
        # if the leaderboard is not empty
        if len(self) > 0:
            print(self[len(self) - 1])
            longest_time_in_leaderboard = [self[len(self) - 1].minutes, self[len(self) - 1].seconds]
            if (time[0] * 60 + time[1]) >= (
                    longest_time_in_leaderboard[0] * 60 + longest_time_in_leaderboard[1]) and len(self) >= 10:
                return False
            else:
                return True
        else:
            return True

    def clear_all(self):
        # deletes the table in the .db file
        self.c.execute('''DELETE FROM entries''')
        self.conn.commit()

        # clear the internal list
        super(Leaderboard, self).clear()


class NameAdder(AnchorLayout):
    def __init__(self, theme, **kwargs):
        super(NameAdder, self).__init__(**kwargs)

        self.theme = theme

        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.size_hint = [1, None]
        self.size = [350, 60]

        self.boxlayout = BoxLayout(orientation='horizontal', size_hint=[None, None], size=[400, 60])

        # the description for the text input
        self.desc_label = Label(
            text='Player name:',
            font_name='gothic',
            font_size='18sp',
            color=self.theme.get_secondary_accent(),
            size_hint=[None, None],
            size=[110, 60]
        )
        self.boxlayout.add_widget(self.desc_label)

        # the text input for the name
        input_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=[None, None], size=[215, 60])
        self.input = TextInput(
            multiline=False,
            size_hint=[None, None],
            size=[180, 35],
            font_name='gothic',
            font_size='18sp',
            background_color=theme.get_primary_accent(),
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{theme.current}.png',
            background_active=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{theme.current}.png',
            cursor_color=theme.get_secondary(),
            foreground_color=theme.get_secondary()
        )
        self.input.input_filter = lambda text, from_undo: text[:15 - len(self.input.text)]
        input_layout.add_widget(self.input)
        self.boxlayout.add_widget(input_layout)

        # the submit button
        submit_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.submit = Button(
            text='Submit',
            size_hint=[1, None],
            size=[50, 40],
            font_name='gothic',
            font_size='16sp',
            color=[0.9, 0.9, 0.9, 1],
            background_normal=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png',
            background_down=f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'
        )
        submit_layout.add_widget(self.submit)
        self.boxlayout.add_widget(submit_layout)

        self.add_widget(self.boxlayout)

    def apply_theme(self, theme):
        self.desc_label.color = theme.get_secondary()
        self.input.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{theme.current}.png'
        self.input.background_active = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{theme.current}.png'
        self.input.background_color = theme.get_primary_accent()
        self.input.foreground_color = theme.get_secondary()
        self.input.cursor_color = theme.get_secondary()

        # recolor the button
        self.submit.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.submit.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'


class NameAdderButton(ToggleButton):
    name_adder_visible = False

    def __init__(self, theme, box, **kwargs):
        super(NameAdderButton, self).__init__(**kwargs)

        self.theme = theme
        self.name_adder = NameAdder(theme)

        self.box = box
        self.text = 'Add to leaderboard'
        self.size_hint = [None, None]
        self.size = [190, 50]
        self.font_name = 'gothic'
        self.font_size = '16sp'
        self.color = [0.9, 0.9, 0.9, 1]
        self.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_normal_{theme.current}.png'
        self.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/buttons/button_pressed_{theme.current}.png'

    def on_state(self, widget, value):
        if value == 'down':
            self.box.add_widget(self.name_adder)
            self.name_adder_visible = True
        else:
            self.box.remove_widget(self.name_adder)
            self.name_adder_visible = False

    def add_name_adder(self):
        if not self.name_adder_visible:
            self.box.add_widget(self.name_adder)
            self.name_adder_visible = True

    def reset_button(self):
        if self.name_adder_visible:
            self.box.remove_widget(self.name_adder)
            self.name_adder_visible = False
        self.name_adder.input.text = ''
        self.state = 'normal'
