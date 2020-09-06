from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from random import randint

from minesweeper.widgets.core.cell import Cell


class Minesweeper(GridLayout):

    theme = None
    grid_size = 0
    mines_percent = 0
    game_state = 'None'

    def __init__(self, all, theme, grid_size=15, mines_percent=0.15, **kwargs):
        super(Minesweeper, self).__init__(
            cols=grid_size,
            spacing=[1, 1],
            **kwargs)

        self.all = all
        self.theme = theme
        self.grid_size = grid_size
        self.mines_percent = mines_percent

        # define a background for the grid --> dark lines between the tiles
        with self.canvas:
            self.color = theme.make_color(theme.get_secondary())
            self.grid_background = Rectangle(pos=self.pos, size=(self.width, self.height))
        self.bind(pos=self.redraw, size=self.redraw)

        self.cells = []
        mine_spot_options = []

        # set all self.cells and put them all in a list
        for i in range(grid_size):
            cell_row = []
            for j in range(grid_size):
                cell = Cell(theme, self.all, self, i, j, grid_size)

                mine_spot_options.append((i, j))

                cell_row.append(cell)
                self.add_widget(cell)
            self.cells.append(cell_row)

        count = 0
        # choose the mine spots and make the mines
        for spot in range(int(grid_size * grid_size * mines_percent)):
            spot = mine_spot_options.pop(randint(0, len(mine_spot_options)) - 1)
            self.cells[spot[0]][spot[1]].make_mine()
            count += 1
        print(count)

        for i in range(grid_size):
            for j in range(grid_size):
                self.cells[i][j].count_neighbours(self.cells)

    def redraw(self, *args):
        if self.game_state == 'won':
            self.color.rgba = [0, 255, 0, 1]
        elif self.game_state == 'lost':
            self.color.rgba = [255, 0, 0, 1]
        else:
            self.color.rgba = self.theme.get_secondary()
        self.grid_background.pos = self.pos
        self.grid_background.size = (self.width, self.height)

    def reset_game(self, grid_size=None, mines_percent=None):
        # remove all the existing widgets to prevent interference with the new ones
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.remove_widget(self.cells[i][j])

        # take the same grid size and mines percent as before, if no other instructions given
        if grid_size is None:
            grid_size = self.grid_size
        if mines_percent is None:
            mines_percent = self.mines_percent

        # clear the canvas
        self.canvas.clear()

        # "create" the game again
        self.__init__(self.all, self.theme, grid_size, mines_percent)

    def game_over(self):
        print('show game over screen')
