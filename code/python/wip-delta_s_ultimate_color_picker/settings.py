# File for storing specific values
from color_functions import hex_to_rgb
from json import load

with open("settings.json", encoding="utf-8") as sett:
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