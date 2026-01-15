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
        self.window = pyglet.window.Window(width=800, height=600)
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1)

        @self.window.event
        def on_draw():
            self.window.clear()
            self.physics_loop()
            for e in self.objects:
                e.render()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.objects.append(Ball(randint(100, 500), randint(100, 500), randint(25, 50), self))


    def run(self):
        pyglet.app.run(1/60)
    
    def physics_loop(self):
        for e in self.objects:
            e.apply_physics()



if __name__ == "__main__":
    engine = Engine()
    engine.statics.append(WorldBoundary(0, 0, Vector2(sqrt(2)/2, sqrt(2)/2)))#Bottom
    engine.statics.append(WorldBoundary(0, -engine.window.height, Vector2(0, -1)))#Top
    engine.statics.append(WorldBoundary(-engine.window.width, 0, Vector2(-1, 0)))#Right
    engine.statics.append(WorldBoundary(0, 0, Vector2(1, 0)))#Left
    engine.run()

    print("engine ended")