from kivy.clock import Clock
from kivy.uix.label import Label


class GameClock(Label):

    minutes = 0
    seconds = 0

    def __init__(self, theme, **kwargs):
        super(GameClock, self).__init__(**kwargs)

        self.text = self.time_to_string(self.minutes, self.seconds)
        self.font_size = '50sp'
        self.font_name = 'gothic'
        self.color = theme.get_secondary_accent()
        self.halign = 'right'
        self.valign = 'bottom'

        self.bind(size=self.setter('text_size'))

    def time_to_string(self, minutes, seconds):
        min_str = str(minutes)
        if len(min_str) == 1:
            min_str = '0' + min_str

        sec_str = str(seconds)
        if len(sec_str) == 1:
            sec_str = '0' + sec_str

        return min_str + ':' + sec_str

    def increment_time(self, interval):
        if self.seconds == 59 and self.minutes < 59:
            self.minutes += 1
            self.seconds = 0
        elif self.minutes == 59 and self.seconds == 59:
            self.minutes = 0
            self.seconds = 0
        else:
            self.seconds += 1

        self.text = self.time_to_string(self.minutes, self.seconds)

    def start(self):
        Clock.schedule_interval(self.increment_time, 1)

    def stop(self):
        Clock.unschedule(self.increment_time)

    def reset(self):
        self.minutes = 0
        self.seconds = 0

        self.text = self.time_to_string(self.minutes, self.seconds)
