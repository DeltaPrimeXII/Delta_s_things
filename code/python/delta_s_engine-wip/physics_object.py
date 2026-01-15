#Physics_object
import pyglet
from utilities import *
from engine import Engine
#==================================================
#==================================================

class Ball:

    def __init__(self, x, y, r, engine:"Engine", vec=Vector2(0, 0)):
        self._x = x
        self._y = y
        self._r = r
        self.engine = engine
        self.object = pyglet.shapes.Circle(x=self.x, y=self.y, radius=self.r)
        self.velocity = vec

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
                self.velocity = symmetry(self.velocity, self.engine.statics[i].normal) * (Vector2(1, 1) - self.engine.statics[i].absorbtion)
        for e in self.engine.objects:
            if type(e) is Link:
                e.apply_physics()
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
    def __init__(self, x:float, y:float, normal:"Vector2", absorbtion=Vector2(0, 0)):
        self.x = x
        self.y = y
        self.normal = normal
        self.absorbtion = absorbtion

#==================================================

class Link:
    def __init__(self, ball_1, ball_2, length, rigid=True):
        self.ball_1 = ball_1
        self.ball_2 = ball_2
        self.length = length
        self.rigid = rigid
        self.object = pyglet.shapes.Line(self.ball_1.x, self.ball_1.y, self.ball_2.x, self.ball_2.y, 5)

    def render(self) -> None:
        """Render the shape on screen"""
        self.object.draw()

    def apply_physics(self) -> None:
        """Handle all the physic"""
        balls_vector = Vector2(self.ball_1.x - self.ball_2.x, self.ball_1.y - self.ball_2.y)# 1 --> 2
        current_length = balls_vector.length()
        if current_length > self.length:
            self.ball_1.velocity -= normalized(balls_vector) * (current_length - self.length) * (1/60) / 2
            self.ball_2.velocity += normalized(balls_vector) * (current_length - self.length) * (1/60) / 2
            
        elif self.rigid and current_length < self.length:
            self.ball_1.velocity += normalized(balls_vector) * (self.length - current_length) * (1/60) / 2
            self.ball_2.velocity -= normalized(balls_vector) * (self.length - current_length) * (1/60) / 2

        self.object.x = self.ball_1.x
        self.object.y = self.ball_1.y
        self.object.x2 = self.ball_2.x
        self.object.y2 = self.ball_2.y