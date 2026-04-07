
import win32api, win32con

#==================================================

class Key:

    def __init__(self, key:str, code:int):
        self.key = key
        self.code = code
        self.last_state = False
        self.state = False

    def __repr__(self):
        return f"<Key {self.key} : {self.state}>"
    
    def update(self):
        self.last_state = self.state
        if win32api.GetAsyncKeyState(self.code) <= -32767:
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

def update_keys(key_dict):
    for keys in key_dict.values():
        keys.update()

#==================================================

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

    "²": ord("²"), #²
    "&": ord("&"), #1
    "é": ord("é"), #2
    '"': ord('"'), #3 ( " )
    "'": ord("'"), #4 ( ' )
    "(": ord("("), #5
    "-": ord("-"), #6
    "è": ord("è"), #7
    "_": ord("_"), #8
    "ç": ord("ç"), #9
    "à": ord("à"), #0
    ")": ord(")"), #°
    "=": ord("="), #+
}

#key is the variable intended to be used in other scripts
key = {}
for k in key_list.keys():
    key[k] = Key(k, key_list[k])

#--------------------------------------------------

if __name__ == "__main__":

    pass

    # state_list = {
    #     "just_pressed": -32768,
    #     "pressed": -32767,
    #     "just_released": 1,
    #     "released": 0
    # }

#==================================================
