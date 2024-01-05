from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage, Color
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

spacing = 15

def all_cells():
    for x in range(4):
        for y in range (4):
            yield (x,y)

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

