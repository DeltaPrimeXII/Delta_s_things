#Engine

import pyglet
from physics_object import *
from random import randint
from math import sqrt

class Engine:

    gravity = 1

    def __init__(self):
        self.objects = []
        self.statics = []
        self.window = pyglet.window.Window(width=1280, height=720, caption="Delta's Engine", resizable=True)
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1)


        @self.window.event
        def on_resize(width, height):
            self.statics[1].y = -height
            self.statics[2].x = -width

        @self.window.event
        def on_draw():
            self.window.clear()
            self.physics_loop()
            for e in self.objects:
                e.render()

        @self.window.event
        def on_key_press(symbol, modifiers):
            print(f"symbol: {symbol}, modifiers: {modifiers}")
            self.objects.append(Ball(randint(100, 500), randint(100, 500), 15, self, Vector2(10, 40)))
            self.objects.append(Ball(randint(300, 800), randint(100, 500), 15, self, Vector2(20, 0)))
            self.objects.append(Link(self.objects[len(self.objects)-2], self.objects[len(self.objects)-1], 200))


    def run(self):
        pyglet.app.run(1/60)
    
    def physics_loop(self):
        for e in self.objects:
            e.apply_physics()



if __name__ == "__main__":
    engine = Engine()
    engine.statics.append(WorldBoundary(0, 0, Vector2(0, 1), Vector2(0.1, 0.3)))#Bottom
    engine.statics.append(WorldBoundary(0, -engine.window.height, Vector2(0, -1)))#Top
    engine.statics.append(WorldBoundary(-engine.window.width, 0, Vector2(-1, 0)))#Right
    engine.statics.append(WorldBoundary(0, 0, Vector2(1, 0)))#Left
    engine.run()

    print("engine ended")