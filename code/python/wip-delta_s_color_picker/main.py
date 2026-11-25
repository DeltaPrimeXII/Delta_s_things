import pyglet
from classes import Mouse, Tab, ColorPicker, ColorPalette, PaletteGenerator, DisplayColor, ColorSlider, Button, Toggle, TextBox, OptionBox
from classes import TAB, mode
from settings import settings
from random import randint

#Nearest-neighbor sampling by default
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

bg = settings["color"]["background"]

#============================================================

class ColorPickerApp(pyglet.window.Window):
    def __init__(self, width, height, title="Title", resizeable=True):
        super().__init__(width, height, title, resizeable)
        self.set_minimum_size(200, 150)
        pyglet.gl.glClearColor(bg[0]/255, bg[1]/255, bg[2]/255 , 1)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.mouse = Mouse()

        # ----------
        self.tabs = {
            TAB.MENU: Tab(self, TAB.MENU),
            TAB.PICKER: Tab(self, TAB.PICKER),
            TAB.SETTINGS: Tab(self, TAB.SETTINGS),
        }
        # ----------
        self.current_tab = self.tabs[TAB.MENU]
        # ----------
        with self.tabs[TAB.MENU] as parent:
            parent.ui = {
                "button_picker": Button(parent, "Color Picker", (lambda: self.width/2 - 50), (lambda: self.height/2 + 25), 100, 50, (lambda: self.change_tab(TAB.PICKER))),
                "button_settings": Button(parent, "Settings", (lambda: self.width/2 - 50), (lambda: self.height/2 - 75), 100, 50, (lambda: self.change_tab(TAB.SETTINGS))),
                "textbox": TextBox(parent, 25, 25, 200, 50, numeric_only=True),
                "toggle": Toggle(parent, 300, 25, 50, 50, False)
            }
        with self.tabs[TAB.PICKER] as parent:
            parent.ui = {
                "color_picker": ColorPicker(parent, 25, (lambda: self.height/2)),
                "color_palette": ColorPalette(parent, 450, 25, 3, 5),
                "palette_generator": PaletteGenerator(parent, 25, 25, 5)
            }
        with self.tabs[TAB.SETTINGS] as parent:
            parent.ui = {
                "option_default_width": TextBox(parent, 25, lambda: self.height - 75, 200, 50),
                "option_default_height": TextBox(parent, 25, lambda: self.height - 75*2, 200, 50),
                "option_color_mode": OptionBox(parent, 25, lambda: self.height - 75*3, 200, 50, ("RGB", "HSV", "OKLCH")),
            }


    #-------------------------
    def on_draw(self) -> None:
        self.clear() # fill the screen with background color
        self.current_tab.batch.draw() # draw current tab's elements on screen
    #-------------------------
    def on_resize(self, width, height):
        super().on_resize(width, height)
        if hasattr(self, "tabs"):
            for t in self.tabs.values():
                t.on_resize(width, height)
    #-------------------------
    def on_key_press(self, symbol, modifiers) -> None:
        if not self.current_tab.focused_text_box:
            if symbol == pyglet.window.key.ESCAPE:
                self.change_tab(TAB.MENU)
            #TEMPORARY ------------------------------------------------------------------- \
            if symbol == pyglet.window.key.SPACE and self.current_tab.name == TAB.PICKER:#  |
                self.current_tab.ui["color_picker"]["display_color"].color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.current_tab.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers) -> None:
        self.current_tab.on_key_release(symbol, modifiers)
    #-------------------------
    def on_text(self, text) -> None:
        self.current_tab.on_text(text)

    def on_text_motion(self, motion) -> None:
        self.current_tab.on_text_motion(motion)
    #-------------------------
    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.mouse.update(x, y)
        if button == pyglet.window.mouse.LEFT:
            self.current_tab.on_click()
    
    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.mouse.update(x, y)
        if button == pyglet.window.mouse.LEFT:
            self.current_tab.on_release()

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.mouse.update(x, y, dx, dy)
        self.current_tab.on_motion()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        self.mouse.update(x, y, dx, dy)
        self.current_tab.on_drag()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y) -> None:
        self.mouse.update(x, y, scroll_x=scroll_x, scroll_y=scroll_y)
        multiplier = 10 if (self.keys[pyglet.window.key.LSHIFT] or self.keys[pyglet.window.key.RSHIFT]) else 1
        self.current_tab.on_scroll(multiplier)
    #-------------------------
    def run(self) -> None:
        pyglet.app.run(1/60)
    #========================
    def change_tab(self, tab_name) -> None:
        print(f"{self.current_tab.name.value} --> {tab_name.value}")
        self.current_tab = self.tabs[tab_name]

#============================================================

if __name__ == '__main__':
    app = ColorPickerApp(settings["default_width"],
                         settings["default_height"],
                         title="Delta's Color Picker",
                         resizeable=True)
    app.run()
