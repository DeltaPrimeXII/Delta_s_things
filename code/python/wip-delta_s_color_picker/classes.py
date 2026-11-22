import pyglet
from enum import Enum
import color_functions as col
from settings import settings

#TODO: replace all the x, y parameters with self.mouse

#-------------------------

black = (0, 0, 0)
white = (255, 255, 255)
t = settings["outline_thickness"]
# color = {k: v for k, v in settings["color"].items()}

class TAB(Enum):
    MENU = "menu"
    PICKER = "picker"
    SETTINGS = "settings"

class mode(Enum):
    RGB = "rgb"
    HSV = "hsv"
    OKLCH = "oklch"

col_func = {
    mode.RGB: col.rgb_to_rgb,
    mode.HSV: col.hsv_to_rgb,
    mode.OKLCH: col.oklch_to_rgb,
}

col_func_reverse = {
    mode.RGB: col.rgb_to_rgb,
    mode.HSV: col.rgb_to_hsv,
    mode.OKLCH: col.rgb_to_oklch,
}

#===================================================

class Mouse:
    __slots__ = ("_x", "_y") # Make sure no other attributes can be added
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    def update(self, x:int, y:int) -> None:
        self._x = x
        self._y = y

#===================================================

class Tab:
    def __init__(self, app, name, scrollable=False):
        self.app = app
        self.name = name
        self.scrollable = scrollable
        self.mouse:Mouse = app.mouse
        self.ui = {}
        self.batch = pyglet.graphics.Batch()
        # For drawing order
        self.groups = [pyglet.graphics.Group(0),
                       pyglet.graphics.Group(1),
                       pyglet.graphics.Group(2),
                       pyglet.graphics.Group(3),]
        self.dragged_color:DisplayColor = None
        self.focused_text_box:TextBox = None
        self.offset = 0

    def __repr__(self) -> str:
        return f"Tab[{self.name}]"

    def __iter__(self):
        for ui in self.ui.values():
            yield ui

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False
    #-------------------------
    def element_at(self, x, y, element_type=None):
        for el in get_all_instance_of(self, element_type):
            if el.is_hovered(x, y):
                return el
        return None

    def tab_scroll(self, scroll):#TODO: check if it is possible to offset everything on screen
        self.offset = clamp(0, self.offset + scroll, 999)
    #-------------------------
    def on_resize(self, width, height) -> None:
        for ui in self.ui.values():
            ui.update_coords()
    #-------------------------
    def on_key_press(self, symbol, modifiers) -> None:
        if self.focused_text_box:
            if symbol in [pyglet.window.key.ESCAPE, pyglet.window.key.ENTER]:
                self.focused_text_box.unfocus()
                self.focused_text_box = None

    def on_key_release(self, symbol, modifiers) -> None:
        pass
    #-------------------------
    def on_text(self, text):
        if self.focused_text_box:
            self.focused_text_box.add(text)

    def on_text_motion(self, motion) -> None:
        if self.focused_text_box:
            if motion == pyglet.window.key.MOTION_BACKSPACE:
                self.focused_text_box.backspace()
    #-------------------------
    def on_click(self, x:int, y:int) -> None:
        self.click_behavior(x, y)
        for ui in self:#----------
            ui.on_click(x, y)

    def on_release(self, x:int, y:int) -> None:
        if self.dragged_color:
            target = self.element_at(x, y, DisplayColor)
            if (target) and (target != self.dragged_color) and (target.droppable):
                if (target.swappable) and (self.dragged_color.swappable): # Swap color
                    # print("color_swapped")
                    swap_colors(target, self.dragged_color)
                elif target.droppable: # Copy color to target
                    # print("color_copied")
                    target.color = self.dragged_color.color
            self.dragged_color = None
        for ui in self:#----------
            ui.on_release(x, y)

    def on_motion(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_motion(x, y)

    def on_drag(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_drag(x, y)

    def on_scroll(self, x:int, y:int, scroll) -> None:
        for ui in self:
            ui.on_scroll(x, y, scroll)
        if self.scrollable and not self.element_at(x, y):
            self.tab_scroll(scroll)
    #-------------------------
    def click_behavior(self, x:int, y:int) -> None:
        new_color:DisplayColor = self.element_at(x, y, DisplayColor)
        if self.dragged_color != new_color:
            self.dragged_color = new_color
        new_text_box:TextBox = self.element_at(x, y, TextBox)
        if self.focused_text_box != new_text_box:
            if self.focused_text_box:
                self.focused_text_box.unfocus()#TODO: find why it takes so much time to update
            if new_text_box:
                new_text_box.focus()
            self.focused_text_box = new_text_box

#===================================================

class SuperElement:
    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.batch = parent.batch
        self.groups = parent.groups
        self.mouse:Mouse = parent.mouse
        self._x = x
        self._y = y
        self.ui = {}

    #-Black-Magic----------
    @property
    def x(self):
        if callable(self._x):
            return self._x()
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        if callable(self._y):
            return self._y()
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    #-Black-Magic----------

    def __iter__(self): # __iter__ is so cool T-T
        for ui in self.ui.values():
            yield ui

    def __getitem__(self, key):
        return self.ui[key]

    def __setitem__(self, key, value):
        self.ui[key] = value

    def is_hovered(self, mouse_x:int, mouse_y:int) -> bool:
        return True

    def on_click(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_click(x, y)

    def on_release(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_release(x, y)

    def on_motion(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_motion(x, y)

    def on_drag(self, x:int, y:int) -> None:
        for ui in self:
            ui.on_drag(x, y)

    def on_scroll(self, x:int, y:int, scroll) -> None:
        for ui in self:
            ui.on_scroll(x, y, scroll)

    def update_coords(self) -> None:
        pass

#--------------------------------------------------

class ColorPicker(SuperElement):
    def __init__(self, parent, x=0, y=0):
        super().__init__(parent, x, y)
        self.ui = {
            "display_color": DisplayColor(self, (self.x + 300), (self.y - 25), 50, 50, swappable=False),
            "slider1": ColorSlider(self, (self.x), (self.y + 50), 256, 50),
            "slider2": ColorSlider(self, (self.x), (self.y - 25), 256, 50),
            "slider3": ColorSlider(self, (self.x), (self.y - 100), 256, 50),
        }

    def update_coords(self):
        self["display_color"].x = self.x + 300
        self["display_color"].y = self.y - 25
        self["slider1"].x = self.x
        self["slider1"].y = self.y + 50
        self["slider2"].x = self.x
        self["slider2"].y = self.y - 25
        self["slider3"].x = self.x
        self["slider3"].y = self.y - 100
        for ui in self:
            ui.update_coords()

#--------------------------------------------------

class ColorPalette(SuperElement):
    def __init__(self, parent, x=0, y=0, rows=3, columns=3):
        super().__init__(parent, x, y)
        self.rows = rows
        self.columns = columns
        self.ui = {
            "color_matrix": [
                [DisplayColor(self, (self.x + r*75), (self.y + c*75 + 75), 50, 50) for c in range(self.columns)] for r in range(self.rows)
                ],
            "save_button": Button(self, "Save", self.x, self.y, 100, 50, lambda: print("save")),
            "import_button": Button(self, "Import", (self.x + 125), self.y, 100, 50, lambda: print("import")),
            "reset_button": Button(self, "Reset", (self.x + 250), self.y, 100, 50, lambda: print("reset")),
        }

    def __iter__(self):
        for name, ui in self.ui.items():
            if name == "color_matrix":
                for i in range(self.rows):
                    for j in range(self.columns):
                        yield ui[i][j]
            else:
                yield ui

    #TODO
    def update_coords(self):
        return super().update_coords()

#--------------------------------------------------

class PaletteGenerator(SuperElement):
    def __init__(self, parent, x=0, y=0, number=5):
        super().__init__(parent, x, y)
        self.number = number

        self.ui = {
            "starting_color": DisplayColor(self, self.x, self.y, 50, 50, black, swappable=False),
            "palette": [DisplayColor(self, (self.x + i*50 + 75), self.y, 50, 50, black, droppable=False, swappable=False) for i in range(self.number)],
        }

    def __iter__(self):
        for name, ui in self.ui.items():
            if name == "palette":
                for i in range(self.number):
                    yield ui[i]
            else:
                yield ui

    #TODO
    def update_coords(self):
        return super().update_coords()
    
#===================================================

class Element:
    def __init__(self, parent, x=0, y=0, w=0, h=0):
        self.parent = parent
        self.batch = parent.batch
        self.groups = parent.groups
        self.mouse:Mouse = parent.mouse
        self._x = x
        self._y = y
        self.w = w
        self.h = h
        self.drawables = {}
        self.clicked = False

    #-Black-Magic----------
    @property
    def x(self):
        if callable(self._x):
            return self._x()
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        if callable(self._y):
            return self._y()
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    #-Black-Magic----------

    def __getitem__(self, key):
        return self.drawables[key]

    def __setitem__(self, key, value):
        self.drawables[key] = value

    def is_hovered(self, mouse_x:int, mouse_y:int) -> bool:
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h
    
    def animate(self, x:int, y:int) -> None:
        if self.is_hovered(x, y):
            self["outline"].color = settings["color"]["outline_hover"]
        else:
            self["outline"].color = settings["color"]["outline"]

    def on_click(self, x:int, y:int) -> None:
        if self.is_hovered(x, y):
            self.animate(x, y)
            self.clicked = True

    def on_release(self, x:int, y:int) -> None:
        self.animate(x, y)
        self.clicked = False

    def on_motion(self, x:int, y:int) -> None:
        self.animate(x, y)

    def on_drag(self, x:int, y:int) -> None:
        self.animate(x, y)

    def on_scroll(self, x, y, scroll) -> None:
        pass

    def update_coords(self) -> None:
        pass

#--------------------------------------------------

class Button(Element):
    def __init__(self, parent, text="", x=0, y=0, w=100, h=50, func=None):
        super().__init__(parent, x, y, w, h)
        self.text = text
        self.func = func
        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "button": pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, settings["color"]["button"], batch=self.batch, group=self.groups[1]),
            "text": pyglet.text.Label(self.text, (self.x + self.w/2), (self.y + self.h/2), anchor_x="center", anchor_y="center", font_size=settings["text_size"], color=settings["color"]["text"], batch=self.batch, group=self.groups[2]),
        }

    def animate(self, x:int, y:int) -> None:
        if self.is_hovered(x, y):
            for name, ui in self.drawables.items():
                ui.color = settings["color"][f"{name}_hover"]
        else:
            for name, ui in self.drawables.items():
                ui.color = settings["color"][name]

    def on_release(self, x:int, y:int) -> None:
        if self.is_hovered(x, y) and self.clicked:
            if callable(self.func):
                self.func()
        self.clicked = False

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        self.drawables["button"].x = self.x
        self.drawables["button"].y = self.y
        self.drawables["text"].x = self.x + self.w/2
        self.drawables["text"].y = self.y + self.h/2

#--------------------------------------------------

class TextBox(Element):
    def __init__(self, parent, x=0, y=0, w=0, h=0, numeric_only=True):
        super().__init__(parent, x, y, w, h)
        self._text = ""
        self.numeric_only = numeric_only
        self.focused = False

        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "button": pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, settings["color"]["button"], batch=self.batch, group=self.groups[1]),
            "text": pyglet.text.Label(self._text, (self.x + self.w/2), (self.y + self.h/2), anchor_x="center", anchor_y="center", font_size=settings["text_size"], color=settings["color"]["text"], batch=self.batch, group=self.groups[2]),
        }

    #----------------------
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        self._text = value
        self["text"].text = value
    #----------------------

    def animate(self, x:int, y:int) -> None:
        if self.focused:
            self["outline"].color = settings["color"]["outline_focus"]
        elif self.is_hovered(x, y):
            self["outline"].color = settings["color"]["outline_hover"]
        else:
            self["outline"].color = settings["color"]["outline"]

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        self.drawables["button"].x = self.x
        self.drawables["button"].y = self.y
        self.drawables["text"].x = self.x + self.w/2
        self.drawables["text"].y = self.y + self.h/2

    def add(self, text:str) -> None:
        if self.numeric_only and text in "0123456789.+-*/%()":
            self.text += text
        elif not self.numeric_only and text.isascii():
            self.text += text

    def backspace(self) -> None:
        var = self.text
        self.text = var[0:len(var)-1]

    def focus(self) -> None:
        self.focused = True
        self.animate(self.mouse.x, self.mouse.y)

    def unfocus(self) -> None:
        if valid_operation(self.text):
            try:
                self.text = str(eval(self.text))
            except ZeroDivisionError:
                pass
        self.focused = False
        self.animate(self.mouse.x, self.mouse.y)

#--------------------------------------------------

class OptionBox(Element):
    def __init__(self, parent, x=0, y=0, w=0, h=0, options=None):
        super().__init__(parent, x, y, w, h)
        self.options = options
        self.current = 0

        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "button": pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, settings["color"]["button"], batch=self.batch, group=self.groups[1]),
            "text": pyglet.text.Label(self.options[self.current], (self.x + self.w/2), (self.y + self.h/2), anchor_x="center", anchor_y="center", font_size=settings["text_size"], color=settings["color"]["text"], batch=self.batch, group=self.groups[2]),
        }

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        self.drawables["button"].x = self.x
        self.drawables["button"].y = self.y
        self.drawables["text"].x = self.x + self.w/2
        self.drawables["text"].y = self.y + self.h/2

    def on_click(self, x, y):
        if self.is_hovered(x, y):
            self.current = (self.current + 1) % len(self.options)
            self["text"].text = self.options[self.current]
            self.clicked = True
#--------------------------------------------------

class Toggle(Element):
    def __init__(self, parent, x=0, y=0, w=0, h=0, value=False):
        super().__init__(parent, x, y, w, h)
        self.value = value

        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "button": pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, settings["color"]["button"], batch=self.batch, group=self.groups[1]),
            "text": pyglet.text.Label(("X" if self.value else ""), (self.x + self.w/2), (self.y + self.h/2), anchor_x="center", anchor_y="center", font_size=settings["text_size"], color=settings["color"]["text"], batch=self.batch, group=self.groups[2]),
        }

    def on_release(self, x:int, y:int) -> None:
        if self.is_hovered(x, y) and self.clicked:
            self.toggle()
        self.clicked = False

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        self.drawables["button"].x = self.x
        self.drawables["button"].y = self.y
        self.drawables["text"].x = self.x + self.w/2
        self.drawables["text"].y = self.y + self.h/2

    def toggle(self):
        self.value = not self.value
        self["text"].text = "X" if self.value else ""

#--------------------------------------------------

class DisplayColor(Element):
    def __init__(self, parent, x=0, y=0, w=50, h=50, color=black, droppable=True, swappable=True):
        super().__init__(parent, x, y, w, h)
        self._color = color
        self.droppable = droppable
        self.swappable = swappable

        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "display": pyglet.shapes.Rectangle(self.x, self.y, self.w, self.h, self._color, batch=self.batch, group=self.groups[1]),
        }

    #----------------------
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value
        self["display"].color = value
    #----------------------

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        self.drawables["display"].x = self.x
        self.drawables["display"].y = self.y

#--------------------------------------------------

class ColorSlider(Element):
    def __init__(self, parent, x=0, y=0, w=256, h=50, value=0):
        super().__init__(parent, x, y, w, h)
        self.value = value

        self.drawables = {
            "outline": pyglet.shapes.Rectangle((self.x - t), (self.y - t), (self.w + 2*t), (self.h + 2*t), settings["color"]["outline"], batch=self.batch, group=self.groups[0]),
            "gradient": [
                pyglet.shapes.Rectangle((self.x + i), self.y, 1, self.h, black, batch=self.batch, group=self.groups[1]) for i in range(self.w)
            ],
            "cursor": pyglet.shapes.Rectangle(self.x, self.y, 1, self.h, white, batch=self.batch, group=self.groups[2])
        }

    def on_click(self, x, y):
        if self.is_hovered(x, y):
            self.clicked = True
            self.value = clamp(0, ((x - self.x)/(self.w - 1)), 1)
            self.update_cursor()

    def on_drag(self, x, y):
        if self.clicked:
            self.value = clamp(0, ((x - self.x)/(self.w - 1)), 1)
            self.update_cursor()

    def on_scroll(self, x, y, scroll):
        if self.is_hovered(x, y):
            self.value = clamp(0, (self.value - scroll/(self.w - 1)), 1)
            self.update_cursor()

    def update_coords(self) -> None:
        self.drawables["outline"].x = self.x - t
        self.drawables["outline"].y = self.y - t
        for i in range(self.w):
            self.drawables["gradient"][i].x = self.x + i
            self.drawables["gradient"][i].y = self.y
        self.update_cursor()

    def update_cursor(self) -> None:
        self.drawables["cursor"].x = self.x + self.value*(self.w - 1)
        self.drawables["cursor"].y = self.y

#===================================================

def get_all_instance_of(container, instance_type=None):
    """Made for the Tab class"""
    for child in container:
        if isinstance(child, SuperElement):
            yield from get_all_instance_of(child, instance_type)
        elif not instance_type:
            yield child
        elif isinstance(child, instance_type):
            yield child

#--------------------------------------------------

def swap_colors(display_color_1:"DisplayColor", display_color_2:"DisplayColor") -> None:
    display_color_1.color, display_color_2.color = display_color_2.color, display_color_1.color

#--------------------------------------------------

def clamp(mini, value, maxi):
    return max(mini, min(value, maxi))

#--------------------------------------------------

def valid_operation(string:str) -> bool:
    """Check if the string is a valid expression. Allowed characters: [0123456789.+-*/%()]"""
    string = string.replace(" ", "")
    if string == "":
        return False
    n = len(string)
    p_count = 0
    dot_count = 0
    for i, c in enumerate(string):
        if c == "(":
            p_count += 1
        elif c == ")":
            p_count -= 1
        elif c == ".":
            dot_count += 1
        elif c not in "0123456789":
            dot_count = 0

        if p_count < 0:
            return False # Number of parenthesis mismatch
        elif dot_count > 1:
            return False # More than 2 dots in a single number
        elif c == "(" and (i == n-1 or string[i+1] in "+-%*/)"):
            return False # Invalid character after a parenthesis
        elif c in "+-%" and (i == 0 or i == n-1 or string[i+1] in "+-%*/)"):
            return False # +, - or % in invalid places
        elif c in "*/" and (i == 0 or i == n-1 or string[i+1] in "+-%)" or string[i-1] + string[i+1] == c + c):
            return False # * or / in invalid places (except **  and //)

    return (p_count == 0)

#--------------------------------------------------

# txt = "2. + (.2 + .5) / 0"
# if valid_operation(txt):
#     try:
#         print(eval(txt))
#     except ZeroDivisionError:
#         print("can't divide by zero")
# else:
#     print("Invalid operation")

