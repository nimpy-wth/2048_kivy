from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage, Color
from kivy.core.window import Window, Keyboard
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation
from kivy.vector import Vector
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import random

key_vectors = {Keyboard.keycodes['up']: (0, 1), 
            Keyboard.keycodes['right']: (1, 0),
            Keyboard.keycodes['down']: (0, -1),
            Keyboard.keycodes['left']: (-1, 0)}

colors = ['EEE4DA', 'EDE0C8', 'F2B179',
        'F59563', 'F67C5F', 'F65E3B', 'EDCF72',
        'EDCC61', 'EDC850', 'EDC53F', 'EDC22E']

tile_colors = {2**i: color for i, color in enumerate(colors, start=1)}

spacing = 15

def all_cells(flip_x=False, flip_y=False):
    for x in (reversed(range(5)) if flip_x else range(5)):
        for y in (reversed(range(5)) if flip_y else range(5)):
            yield (x, y)


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

    def update_colors(self):
        self.color = get_color_from_hex(tile_colors[self.number])
        if self.number > 4:
            self.number_color = get_color_from_hex('F9F6F2')

    def resize(self, pos, size):
        self.pos = pos
        self.size = size
        self.font_size = 0.5 * self.width


class Board(Widget):

    b = None
    moving = None

    def is_deadlocked(self):
        for x, y in all_cells():
            if self.b[x][y] is None:
                return False
            number = self.b[x][y].number
            if self.can_merge(x + 1, y, number) or self.can_merge(x, y + 1, number):
                return False
        return True

    def new_tile(self, *args):
        empty_cells = [(x, y) for x, y in all_cells() if self.b[x][y] is None]
        x, y = random.choice(empty_cells)
        tile = Tile(pos=self.cell_pos(x, y), size=self.cell_size)
        self.b[x][y] = tile
        self.add_widget(tile)
        self.moving = False

        if len(empty_cells) == 1 and self.is_deadlocked():
            print('Game Over')
        
    def reset(self):
        self.b = [[None for i in range(5)] 
                for j in range(5)]
        self.new_tile()
        self.new_tile()
    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.resize()

    def cell_pos(self, board_x, board_y):
        return (self.x + spacing + board_x * (self.cell_size[0] + spacing), 
                self.y + spacing + board_y * (self.cell_size[1] + spacing))

    def resize(self, *args):
        self.cell_size = (.20 * (self.width - 6 * spacing),) * 2
        self.canvas.before.clear()
        with self.canvas.before:
            BorderImage(pos=self.pos,size=self.size,
                        source='board.png')
            Color(*get_color_from_hex('ccc0b4'))
            for board_x, board_y in all_cells():
                BorderImage(pos=self.cell_pos(board_x, board_y), 
                            size=self.cell_size, 
                            source='cell.png')
                
        if not self.b :
            return

        for board_x, board_y in all_cells():
            tile = self.b[board_x][board_y]
            if tile:
                tile.resize(pos=self.cell_pos(board_x, board_y), 
                            size=self.cell_size)

    on_pos = resize
    on_size = resize

    def on_key_down(self, window, key, *args):
        if key in key_vectors:
            self.move(*key_vectors[key])
            
    def valid_cell(self, board_x, board_y):
        return (board_x >= 0 and board_y >= 0 
                and board_x <= 4 and board_y <= 4)

    def can_move(self, board_x, board_y):
        return (self.valid_cell(board_x, board_y) 
                and self.b[board_x][board_y] is None)
    
    def can_merge(self, board_x, board_y, number):
        return (self.valid_cell(board_x, board_y) 
                and self.b[board_x][board_y] is not None 
                and self.b[board_x][board_y].number == number)

    def move(self, dir_x, dir_y):
        if self.moving :
            return
        for board_x, board_y in all_cells(dir_x > 0, dir_y > 0):
            tile = self.b[board_x][board_y]
            if not tile:
                continue
            x, y = board_x, board_y

            while self.can_move(x + dir_x, y + dir_y):
                self.b[x][y] = None
                x += dir_x
                y += dir_y
                self.b[x][y] = tile

            if self.can_merge(x + dir_x, y + dir_y, tile.number):
                self.b[x][y] = None
                x += dir_x
                y += dir_y
                self.remove_widget(self.b[x][y])
                self.b[x][y] = tile
                tile.number *= 2
                tile.update_colors()
                if tile.number == 2048 :
                    print('You win the game.')

            if x == board_x and y == board_y:
                continue
            anim = Animation(pos=self.cell_pos(x, y), duration=0.20, 
                            transition='linear')
            if not self.moving:
                anim.on_complete = self.new_tile
                self.moving = True
            anim.start(tile)

    def on_touch_up(self, touch):
        v = Vector(touch.pos) - Vector(touch.opos)
        if v.length() < 20:
            return
        if abs(v.x) > abs(v.y):
            self.move(1 if v.x > 0 else -1, 0)
        else:
            self.move(0, 1 if v.y > 0 else -1)


class GameApp(App):

    def on_start(self):
        board = self.root.ids.board
        board.reset()
        Window.bind(on_key_down = board.on_key_down)

    def exit_button_click(self, instance):
        self.confirm_popup(instance, "Are you sure you want to exit?",
                            self.exit_confirm).open()

    def restart_button_click(self, instance):
        self.confirm_popup(instance, "Are you sure you want to restart?",
                            self.new_game).open()

    def confirm_popup(self, obj, message, callback):
        box_popup = BoxLayout(orientation = "horizontal")

        popup = Popup(
            title = "Confirmation",
            title_size = 40,
            title_color = get_color_from_hex('574C44'),
            content = box_popup,
            size_hint = (0.5, 0.4),
            auto_dismiss = True,
            background_color = get_color_from_hex('EADFD6'),
            background = '',
            )

        box_popup.add_widget(Label(
            text = message,
            font_size = 30,
            color = get_color_from_hex('574C44'),
            size_hint_y = None,
            height = 40,
            pos_hint = {"center_x": 0.5,"center_y": 0.5},
        ))

        box_popup.add_widget(Button(
            text = "Yes",
            on_release = lambda *args: self.confirm_callback(popup, callback),
            size_hint = (0.45, 0.2),
            background_normal = '',
            background_color = get_color_from_hex('54B87A')
        ))

        box_popup.add_widget(Button(
            text = "No",
            on_press = lambda *args: popup.dismiss(),
            size_hint = (0.45, 0.2),
            background_normal = '',
            background_color = get_color_from_hex('BF3636')
        ))

        return popup

    def confirm_callback(self, instance, callback):
        instance.dismiss()
        callback()

    def exit_confirm(self):
        App.get_running_app().stop()

    def new_game(self, *args):
        board = self.root.ids.board
        b_children = board.children[:]
        for wid in b_children:
            board.remove_widget(wid)

        board.b = [[None for i in range(5)] for j in range(5)]
        board.new_tile()
        board.new_tile()

        exit_button = Button(text = 'Exit', pos = (40, 20), size = (150,80),
                            on_press = self.exit_button_click,
                            background_color = get_color_from_hex('AEA189'),
                            background_normal = '')
        
        restart_button = Button(text='Restart', pos = (40, 120),size = (150,90),
                                on_press = self.restart_button_click,
                                background_color = get_color_from_hex('AEA189'),
                                background_normal = '')

        board.add_widget(exit_button)
        board.add_widget(restart_button)

        self.game_won = False

    def build(self):
        return self.root


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    GameApp().run()

