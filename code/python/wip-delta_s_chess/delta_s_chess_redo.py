#Delta's Chess

# import pyglet
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from _libraries import keyboard as kb

print("Let's do chessing")

key = kb.key
while True:
    kb.update_keys(key)
    if key["l_click"].is_just_pressed():
        print("click")
    if key["r_click"].is_pressed():
        break