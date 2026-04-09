#Delta's Chess

import pyglet
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from _libraries import keyboard as kb
from render import *

#==================================================

#Nearest-neighbor sampling by default
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

#==================================================

class Game_Window:

    def __init__(self):
        self.window = pyglet.window.Window(width=1280, height=720, caption="Delta's Chess", resizable=True)
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1)
        # self.sprite = pyglet.sprite.Sprite(img=pyglet.image.load('assets/drawings/space_8.png'), x=0, y=0)
        # self.sprite.scale = 10

        @self.window.event
        def on_resize(width, height):
            pass

        #Each frame
        @self.window.event
        def on_draw():
            self.window.clear()
            # self.sprite.draw()
            render_board(8)

        @self.window.event
        def on_key_press(symbol, modifiers):
            pass


    def run(self):
        pyglet.app.run(1/60)

#==================================================

game_window = Game_Window()
game_window.run()