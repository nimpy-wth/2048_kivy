from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage
from kivy.core.window import Window
from kivy.utils import get_color_from_hex


class Board(Widget):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

    def board_background(self):
        with self.canvas.before:
            BorderImage(pos=self.pos, 
                        size=self.size, 
                        source='boardbg.png')


class GameApp(App):
    def on_start(self):
        board = self.root.ids.board
        board.board_background()


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    GameApp().run()

