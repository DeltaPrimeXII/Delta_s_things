#Delta's Chess

import pyglet
from pieces import *





def render_game():

    render_board(8)
    render_pieces()





def render_board(n):
    color = True
    for y in range(n):
        for x in range(n):
            a = pyglet.shapes.Rectangle(x=x*64, y=y*64, width=64, height=64)
            a.draw()
            color = not color
def render_pieces():
    pass