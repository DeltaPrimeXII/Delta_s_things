#Delta's Color Picker

import pygame, sys
from pygame.locals import *
from tkinter import Tk
import time

import to_import.color_conversion as col

#====================================================================================================
#---------------Some Varibles----------------------

pygame.init()

WIDTH = 738
HEIGHT = 512

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Delta's Color Picker")

font = pygame.font.Font(pygame.font.get_default_font(), 36)

background = (18, 18, 20)
button = (29, 29, 30)
button_2 = (39, 39, 43)
outline = (34, 34, 36)
outline_2 = (44, 44, 47)
text_color = (250, 250, 250)

window.fill(background)
pygame.display.flip()

#====================================================================================================
#---------------Classes----------------------------

class Ui_controller:
    """class for storing all ui elements"""
    def __init__(self, section="main"):
        match section:

            case "main":
                self.ui = {
                    "buttons": [
                        Button("Color Mode: RGB", (5, 5), color_mode),
                        Button("Copy Color: #000000", (5 + get_button_size("Copy Palette").x + 5, lambda: HEIGHT - get_button_size("Copy Color").y - 5), copy_color),
                        Button("Copy Palette", (5, lambda: HEIGHT - get_button_size("Copy Palette").y - 5), copy_palette),
                        ],
                    "sliders": [
                        Slider("R", (90, 100), 255),
                        Slider("G", (90, 175), 255),
                        Slider("B", (90, 250), 255),
                        ],
                    }
                
            case "color_mode":
                self.ui = {
                    "buttons": [
                        Button("RGB", (10, HEIGHT//2-36//2)),
                        Button("HSL", (110, HEIGHT//2-36//2)),
                        Button("HSV", (210, HEIGHT//2-36//2)),
                        Button("OKLAB", (310, HEIGHT//2-36//2)),
                        ],
                    }

    def __repr__(self):
        result = ""
        for k in self.ui:
            for e in self.ui[k]:
                result += str(e.text) + " - "
        return result
    
    def display(self) -> None:
        for k in self.ui:
            for e in self.ui[k]:
                e.display()
    
    def check_clicks(self, mouse_co) -> None:
        for e in self.ui["buttons"]:
            # if hasattr(e, "is_clicked"):
            if e.is_clicked(mouse_co):
                e.use_button()
    
    def check_slides(self, mouse_co:tuple, scroll_value:int) -> None:
        for e in self.ui["sliders"]:
            # if hasattr(e, "is_slided"):
            if e.is_slided(mouse_co):
                e.change_value(scroll_value)
    
#--------------------------------------------------

class Coord:
    """class for better coordinates"""
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property #Update the x value when possible
    def x(self):
        return self._x() if callable(self._x) else self._x

    @property #Update the y value when possible
    def y(self):
        return self._y() if callable(self._y) else self._y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

#--------------------------------------------------

class Button:
    """class for clickable buttons"""
    def __init__(self, text:str="Text", coord:tuple=(0, 0), func=None):
        self.text = text
        self.rendered_text = font.render(f"{self.text}", True, text_color)
        self.text_size = Coord(self.rendered_text.get_size()[0], self.rendered_text.get_size()[1])
        self.coord = Coord(coord[0], coord[1])
        self.func = func
    
    def __repr__(self) -> str:
        return f"Button object -> (text:{self.text}, coordinates:{self.coord})"

    def display(self) -> None:
        pygame.draw.rect(window, button_2, (self.coord.x, self.coord.y, self.text_size.x+10, self.text_size.y+10))
        pygame.draw.rect(window, button, (self.coord.x+3, self.coord.y+3, self.text_size.x+10-6, self.text_size.y+10-6))
        window.blit(self.rendered_text, dest=(self.coord.x+5, self.coord.y+5))


    def is_clicked(self, mouse_co) -> bool:
        if self.coord.x <= mouse_co[0] <= (self.coord.x + self.text_size.x) and self.coord.y <= mouse_co[1] <= (self.coord.y + self.text_size.y):
            return True
        return False
    
    def use_button(self):
        self.func()
    
    def update_text(self, text):
        self.text = text
        self.rendered_text = font.render(f"{self.text}", True, text_color)
        self.text_size = Coord(self.rendered_text.get_size()[0], self.rendered_text.get_size()[1])

#--------------------------------------------------

class Slider:
    """class for sliders"""
    def __init__(self, text:str="Text", coord:tuple=(0, 0), limit:int=255, value:int=0):
        self.text = text
        self.rendered_text = font.render(f"{self.text}", True, text_color)
        self.text_size = Coord(self.rendered_text.get_size()[0], self.rendered_text.get_size()[1])
        self.coord = Coord(coord[0], coord[1])
        self.limit = limit
        self.value = value
    
    def __repr__(self) -> str:
        return f"Slider object -> (text:{self.text}, coordinates:{self.coord}, range:0-{self.limit}, value:{self.value})"

    def display(self) -> None:
        pygame.draw.rect(window, button_2, (self.coord.x, self.coord.y, 400+10, self.text_size.y+10))
        pygame.draw.rect(window, button, (self.coord.x+3, self.coord.y+3, 400+10-6, self.text_size.y+10-6))
        window.blit(self.rendered_text, dest=(self.coord.x+5, self.coord.y+5))
        window.blit(font.render(f": {self.value}", True, text_color), dest=(self.coord.x+5+30, self.coord.y+5))

    def is_slided(self, mouse_co) -> bool:
        if self.coord.x <= mouse_co[0] <= (self.coord.x + 400+10) and self.coord.y <= mouse_co[1] <= (self.coord.y + self.text_size.y):
            return True
        return False
    
    def change_value(self, scroll_value):
        self.value += scroll_value
        if self.value < 0:
            self.value = 0
        elif self.value > self.limit:
            self.value = self.limit
        # print(self.value)

#====================================================================================================
#---------------Buttons' Functions-----------------

def copy_color():
    global hex_color
    print("copied color: ", hex_color)
    r = Tk()
    r.withdraw()
    # r.clipboard_clear()
    r.clipboard_append(hex_color)
    r.update() # now it stays on the clipboard after the window is closed
    r.destroy()

#--------------------------------------------------

def copy_palette():
    print("palette copied to clipboard")

#--------------------------------------------------

def color_mode():
    global var_color_mode
    mode_ui = Ui_controller("color_mode")
    while True :

        mouse_co = pygame.mouse.get_pos()

        #================================#
        for event in pygame.event.get(): #
            security(event)              #
            window_resize(event)         #
        #================================# 

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for k in mode_ui.ui:
                    for e in mode_ui.ui[k]:
                        if e.is_clicked(mouse_co):
                            var_color_mode = e.text
                            return

        # Rendering the game -------------------------
        window.fill(background)
        mode_ui.display()
        pygame.display.flip()# Render on the screen

#====================================================================================================
#---------------Other Functions--------------------

def security(event):
    if event.type == pygame.QUIT:
        pygame.display.quit()
        sys.exit()

#--------------------------------------------------

def window_resize(event):
    global WIDTH, HEIGHT, window
    if event.type == VIDEORESIZE:
        WIDTH, HEIGHT = event.w, event.h
        window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # for e in ui.ui["buttons"]:
    #     e.__init__(e.text, e.)
    # for e in ui.ui["sliders"]:
    #     e.__init__(e.text)

#--------------------------------------------------

def get_button_size(text:str) -> "Coord":
    size = font.render(text, True, (0,0,0)).get_size()
    return Coord(size[0]+10, size[1]+10)

#--------------------------------------------------

def show_slider_color(sliders:list, color_mode:str="rgb"):
    start = [Coord(sliders[i].coord.x, sliders[i].coord.y) for i in range(3)]
    if color_mode == "HSL":
        pass
    elif color_mode == "HSV":
        pass
    elif color_mode == "OKLAB":
        pass
    else:
        for i in range(0, 255+1):
            pygame.draw.rect(window, (i, sliders[1].value, sliders[2].value), (start[0].x+i+140, start[0].y+12, 1, 20))
        for i in range(0, 255+1):
            pygame.draw.rect(window, (sliders[0].value, i, sliders[2].value), (start[1].x+i+140, start[1].y+12, 1, 20))
        for i in range(0, 255+1):
            pygame.draw.rect(window, (sliders[0].value, sliders[1].value, i), (start[2].x+i+140, start[2].y+12, 1, 20))
        for e in range(3):
            pygame.draw.rect(window, (255, 255, 255), (start[e].x+sliders[e].value+140, start[e].y+15+12, 1, 10))

#====================================================================================================
#---------------Main Loop--------------------------

var_color_mode = "RGB"
hex_color = "000000"
picker_ui = Ui_controller("main")
buttons = picker_ui.ui["buttons"]
sliders = picker_ui.ui["sliders"]

while True :

    mouse_co = pygame.mouse.get_pos()
    all_event = pygame.event.get()

    #================================#
    for event in all_event:          #
        security(event)              #
        window_resize(event)         #
    #================================# 

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            picker_ui.check_clicks(mouse_co)
            buttons[0].update_text(f"Color Mode: {var_color_mode}")

        
        if event.type == MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            scroll_value = event.y
            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                scroll_value *= 10
            picker_ui.check_slides(mouse_co, scroll_value)
            hex_color = '%02x%02x%02x' % (sliders[0].value, sliders[1].value, sliders[2].value)
            buttons[1].update_text(f"Copy Color: #{hex_color}")

    # Rendering the game -------------------------

    if all_event: #update the screen if something happens

        window.fill(background)

        picker_ui.display()
        show_slider_color(sliders, var_color_mode)
    
        pygame.draw.rect(window, (sliders[0].value, sliders[1].value, sliders[2].value), (10, 75, 50, HEIGHT - 150))#current color
        

        pygame.display.flip()# Render on the screen