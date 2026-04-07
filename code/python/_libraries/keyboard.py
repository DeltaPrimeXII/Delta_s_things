
import time
import win32api, win32con


# time.sleep(2)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 100)

#==================================================

class Key:

    key_list = {
        "l_click": win32con.VK_LBUTTON,
        "r_click": win32con.VK_RBUTTON,
        "a": ord("a"),
        "b": ord("b"),
        "c": ord("c"),
        "d": ord("d"),
        "e": ord("e"),
        "f": ord("f"),
        "g": ord("g"),
        "h": ord("h"),
        "i": ord("i"),
        "j": ord("j"),
        "k": ord("k"),
        "l": ord("l"),
        "m": ord("m"),
        "n": ord("n"),
        "o": ord("o"),
        "p": ord("p"),
        "q": ord("q"),
        "r": ord("r"),
        "s": ord("s"),
        "t": ord("t"),
        "u": ord("u"),
        "v": ord("v"),
        "w": ord("w"),
        "x": ord("x"),
        "y": ord("y"),
        "z": ord("z"),
        "echap": win32con.VK_ESCAPE,
        "shift": win32con.VK_SHIFT,
        "ctrl": win32con.VK_CONTROL,
        "alt": win32con.VK_MENU,
        "<": ord("<"),
        ",": ord(","),
        ";": ord(";"),
        ":": ord(":"),
        "!": ord("!"),
        "ù": ord("ù"),
        "^": ord("^"),
        "$": ord("$"),
        "*": ord("*"),

        "²": ord("²"),
        "&": ord("&"),
        "é": ord("é"),
        '"': ord('"'), #('  "  ')
        "'": ord("'"), #("  '  ")
        "(": ord("("),
        "-": ord("-"),
        "è": ord("è"),
        "_": ord("_"),
        "ç": ord("ç"),
        "à": ord("à"),
        ")": ord(")"),
        "=": ord("="),
    }

    def __init__(self, key:str):
        self.key = key
        self.last_state = False
        self.state = False

    def __repr__(self):
        return f"<Key {self.key} : {self.state}>"
    
    def update(self):
        self.last_state = self.state
        if win32api.GetAsyncKeyState(Key.key_list[self.key]) <= -32767:
            self.state = True
        else:
            self.state = False

    def is_pressed(self):
        return self.state
    
    def is_just_pressed(self):
        if self.state and not self.last_state:
            return True
        return False
    
    def is_just_released(self):
        if not self.state and self.last_state:
            return True
        return False

#--------------------------------------------------

def update_keys(key_list):
    for key in key_list:
        key.update()

#==================================================

if __name__ == "__main__":

    # state_list = {
    #     "just_pressed": -32768,
    #     "pressed": -32767,
    #     "just_released": 1,
    #     "released": 0
    # }

    key = {}
    for k in Key.key_list:
        key[k] = Key(k)

#==================================================
