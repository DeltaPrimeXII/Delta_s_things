# File for storing specific values
from color_functions import hex_to_rgb
from pathlib import Path
from json import load

SETTINGS_PATH = Path(__file__).parent / "settings.json"
with open(SETTINGS_PATH, encoding="utf-8") as sett:
    settings = load(sett)

#---- Convert hexa colors to rgb ----
for k, v in settings["color"].items():
    settings["color"][k] = hex_to_rgb(v)
#------------------------------------

settings["rgb"] = {
    "slider1": {
        "relative": True,
    },
    "slider2": {
        "relative": True,
    },
    "slider3": {
        "relative": True,
    },
}

settings["hsv"] = {
    "slider1": {
        "relative": False,
    },
    "slider2": {
        "relative": True,
    },
    "slider3": {
        "relative": True,
    },
}

settings["oklch"] = {
    "slider1": {
        "relative": True,
    },
    "slider2": {
        "relative": True,
    },
    "slider3": {
        "relative": True,
    },
}