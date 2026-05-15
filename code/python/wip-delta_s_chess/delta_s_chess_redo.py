#Delta's Chess

import pyglet
import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent))
# from _libraries import keyboard as kb
from render import *
from game import Board

#==================================================

#Nearest-neighbor sampling by default
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

#==================================================

class Window:

    def __init__(self):
        self.window = pyglet.window.Window(width=640, height=640, caption="Delta's Chess", resizable=True)
        pyglet.gl.glClearColor(0.1, 0.1, 0.2, 1)


        @self.window.event
        def on_resize(width, height):
            pass

        #Each frame
        @self.window.event
        def on_draw():
            self.window.clear()
            game.render(player)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.SPACE:
                pass

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            game.clicked(x, y, player)


    def run(self):
        pyglet.app.run(1/60)

#==================================================
game = Board()
player = 1

window = Window()
window.run()
