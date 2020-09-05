from kivy.uix.button import Button
from kivy.core.window import Window

from kivy.graphics import Line

from minesweeper.widgets.core.graphics import Mine, Flag


class Cell(Button):
    # icons
    mine_icon = None
    flag = None

    theme = None
    pos_x = 0
    pos_y = 0
    grid_size = 15
    mine = False
    revealed = False
    flagged = False
    neighbour_count = 0
    cells = []

    all = None
    weep = None

    def __init__(self, theme, all, weep, x, y, grid_size, **kwargs):
        super().__init__(**kwargs)

        # define some parameters
        self.theme = theme
        self.pos_x = x
        self.pos_y = y
        self.grid_size = grid_size

        self.all = all
        self.weep = weep

        # set the base background picture
        self.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}_normal.png'
        self.background_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}_normal.png'
        self.background_disabled_down = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}_normal.png'

    def __repr__(self):
        return '<Cell: %d, %s>' % (self.pos_x, self.pos_y)

    def count_neighbours(self, cells):
        # define the universal cell variable - IMPORTANT!!!
        self.cells = cells

        if self.mine:
            self.neighbour_count = -1
            return

        for x_offset in range(3):
            # change the values to -1, 0 and 1
            x_offset = x_offset - 1
            i = self.pos_x + x_offset

            if i < 0 or i >= self.grid_size:
                continue

            for y_offset in range(3):
                # change the values to -1, 0 and 1
                y_offset = y_offset - 1
                j = self.pos_y + y_offset

                if j < 0 or j >= self.grid_size:
                    continue

                neighbour = cells[i][j]
                if neighbour.mine:
                    self.neighbour_count += 1

        self.background_disabled_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell' \
                                          f'/{self.theme.current}.png'

    def make_mine(self):
        self.mine = True
        self.background_disabled_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}.png'
        # self.disabled = True

    def on_touch_down(self, touch):
        if touch.button == 'right' and self.collide_point(*touch.pos) and not self.revealed:
            # (un)flag the pressed button and check for victory
            self.toggle_flag()
            if self.victory():
                print('-- VICTORY --')
            return False
        elif touch.button == 'left' and self.collide_point(*touch.pos) and not self.revealed:
            # reveal the pressed button
            self.reveal()
            # check for victory
            if self.victory():
                print('-- VICTORY --')
            # if the pressed button is a mine, game over
            if self.mine:
                self.game_over()
            return False

    def reveal(self):
        self.revealed = True
        self.disabled = True

        if self.flagged:
            self.canvas.remove(self.flag)
            self.canvas.ask_update()

        if self.mine:
            print(self, self.pos, self.size)
            with self.canvas:
                self.mine_icon = Mine(self.theme, self.pos, self.size)
            self.bind(pos=self.redraw, size=self.redraw)
        elif not self.mine and self.neighbour_count != 0:

            # set the correct font, font size (70% of the button height) and font color
            self.font_size = f'{int(self.size[1] * 0.7)}sp'
            self.font_name = 'gothic'
            self.color = self.theme.get_secondary()

            # set the text
            self.text = str(self.neighbour_count)

        if self.neighbour_count == 0:
            self.flood()

    def toggle_flag(self):
        if self.flagged and not self.revealed:
            self.flagged = False
            self.canvas.remove(self.flag)
            self.canvas.ask_update()
            self.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}_normal.png'
        elif not self.flagged and not self.revealed:
            self.flagged = True
            self.flag = Flag(self.theme, self.pos, self.size)
            self.canvas.add(self.flag)
            self.bind(pos=self.redraw, size=self.redraw)
            self.background_normal = f'C:/Users/Nutzer/PycharmProjects/Minesweeper/assets/img/cell/{self.theme.current}.png'

    def flood(self):
        for x_offset in range(3):
            # change the values to -1, 0 and 1
            x_offset = x_offset - 1
            i = self.pos_x + x_offset

            if i < 0 or i >= self.grid_size:
                continue

            for y_offset in range(3):
                # change the values to -1, 0 and 1
                y_offset = y_offset - 1
                j = self.pos_y + y_offset

                if j < 0 or j >= self.grid_size:
                    continue

                neighbour = self.cells[i][j]
                if not neighbour.revealed:
                    neighbour.reveal()

    def victory(self):
        normal_not_selected_count = 0
        not_flagged_mines_count = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # count the normal fields that are not revealed, if 0, all fields unless the mines are selected -->
                # victory
                if not self.cells[i][j].revealed and not self.cells[i][j].mine:
                    normal_not_selected_count += 1

                # count the mine fields that are not flagged, if 0, all mines are flagged --> victory
                if self.cells[i][j].flagged is False and self.cells[i][j].mine:
                    not_flagged_mines_count += 1

        # check the results
        if normal_not_selected_count == 0 or not_flagged_mines_count == 0:
            return True
        else:
            return False

    def game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if not self.cells[i][j].revealed:
                    self.cells[i][j].reveal()

        print('-- GAME OVER --')
        self.all.stopwatch.stop()
        self.all.game_over([self.all.stopwatch.minutes, self.all.stopwatch.seconds])

    def redraw(self, *args):
        if self.mine and self.revealed:
            self.mine_icon.redraw(self.theme, self.pos, self.size)
        elif self.flagged and not self.revealed:
            self.flag.redraw(self.theme, self.pos, self.size)
