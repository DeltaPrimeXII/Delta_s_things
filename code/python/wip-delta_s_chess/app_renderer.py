

from app import *

#==================================================

#Nearest-neighbor sampling by default
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST
width, height = 800, 800

#==================================================

class Window:

    def __init__(self, app:"App"):
        self.window = pyglet.window.Window(width=width, height=height, caption="Delta's Chess", resizable=True)
        self.window.set_minimum_size(320, 320)
        pyglet.gl.glClearColor(0.1, 0.1, 0.2, 1)
        self.app = app


        @self.window.event
        def on_resize(width, height):
            self.app.update_size(width, height)

        #Each frame
        @self.window.event
        def on_draw():
            self.window.clear()
            self.app.main()


        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.SPACE:
                pass

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.app.clicked(x, y, button, modifiers)

    def run(self):
        pyglet.app.run(1/60)

#==================================================
appli = App(width, height)
window = Window(appli)
window.run()
