from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage, Color
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty, NumericProperty

colors = ['EEE4DA', 'EDE0C8', 'F2B179',
        'F59563', 'F67C5F', 'F65E3B', 'EDCF72',
        'EDCC61', 'EDC850', 'EDC53F', 'EDC22E']

tile_colors = {2**i: color for i, color in enumerate(colors, start=1)}

spacing = 15

def all_cells():
    for x in range(4):
        for y in range (4):
            yield (x,y)

class Tile(Widget):
    font_size = NumericProperty(24)
    number = NumericProperty(2)
    color = ListProperty(get_color_from_hex(tile_colors[2]))
    number_color = ListProperty(get_color_from_hex('776E65'))

    def __init__(self, number = 2,**kwargs):
        super(Tile,self).__init__(**kwargs)
        self.font_size = 0.5 * self.width
        self.number = number
        self.update_colors()



class Board(Widget):
    b = None

    def reset(self):
        self.b = [[None for i in range(4)] 
                for j in range(4)]
    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.resize()

    def cell_pos(self, board_x, board_y):
        return (self.x + spacing + board_x * (self.cell_size[0] + spacing), 
                self.y + spacing + board_y * (self.cell_size[1] + spacing))

    def resize(self, *args):
        self.cell_size = (.25 * (self.width - 5 * spacing),) * 2
        self.canvas.before.clear()
        with self.canvas.before:
            BorderImage(pos=self.pos,
                        size=self.size,
                        source='boardbg.png')
            
            Color(*get_color_from_hex('ccc0b4'))
            for board_x, board_y in all_cells():
                BorderImage(pos=self.cell_pos(board_x, board_y), 
                            size=self.cell_size, 
                            source='cell.png')
                
    
    on_pos = resize
    on_size = resize


class GameApp(App):
    def on_start(self):
        board = self.root.ids.board
        # board.resize()
        board.reset()


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    GameApp().run()

