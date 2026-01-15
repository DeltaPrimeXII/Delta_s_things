#Physics_object
import pyglet
from utilities import *
from engine import Engine
#==================================================
#==================================================

class Ball:

    def __init__(self, x, y, r, engine:"Engine"):
        self._x = x
        self._y = y
        self._r = r
        self.engine = engine
        self.object = pyglet.shapes.Circle(x=self.x, y=self.y, radius=self.r)
        self.velocity = Vector2(0, 0)

    #------------------------------

    def render(self) -> None:
        """Render the shape on screen"""
        self.object.draw()
    
    def gravity(self) -> None:
        """Add gravity to the vertical velocity"""
        self.velocity.y += -Engine.gravity

    def apply_physics(self) -> None:
        """Handle all the physic"""
        self.gravity()
        for i in range(len(self.engine.statics)):
            x = self.x + self.velocity.x + self.engine.statics[i].x
            y = self.y + self.velocity.y + self.engine.statics[i].y
            if dot(self.engine.statics[i].normal, Vector2(x, y)) <= self.r:
                self.velocity = symmetry(self.velocity, self.engine.statics[i].normal)
        self.move()
    
    def move(self) -> None:
        """Update coords with the velocity"""
        self.x += self.velocity.x
        self.y += self.velocity.y

    #------------------------------
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self.object.x = value
    #----------
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self.object.y = value
    #----------
    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, value):
        self._r = value
        self.object.radius = value
    #----------

#==================================================

class WorldBoundary:
    def __init__(self, x:float, y:float, normal:"Vector2"):
        self.x = x
        self.y = y
        self.normal = normal