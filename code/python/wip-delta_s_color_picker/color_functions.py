from math import sqrt, cbrt, cos, sin, atan2, pi

max_range = 0.33

#====================================================================================================
def normalized_rgb_to_rgb(r, g, b):
    return (round(r*255), round(g*255), round(b*255))
#----------------------------------------------------------------------------------------------------
# "FF FFFFFF" -> (255, 255, 255)
def hex_to_rgb(hex_str:str):
    hex = hex_str.lstrip('#')
    offset = 0
    if len(hex) == 8:
        a = int(hex[0:2],16)
        offset = 2
    r = int(hex[0+offset:2+offset],16)
    g = int(hex[2+offset:4+offset],16)
    b = int(hex[4+offset:6+offset],16)
    return (r, g, b)
#----------------------------------------------------------------------------------------------------
# (255, 255, 255) -> "FFFFFF"
def rgb_to_hex(r:int, g:int, b:int) -> str:
    # I trust Gemini on this one
    return f"{r:02x}{g:02x}{b:02x}"

#========== Every input/output should be normalized =================================================

def srgb_to_linear(c):
    if c >= 0.04045:
        return ((c + 0.055) / 1.055) ** 2.4
    return c / 12.92
#----------------------------------------------------------------------------------------------------
def linear_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1 / 2.4)) - 0.055
#====================================================================================================
def rgb_to_rgb(r, g, b):
    return (r, g, b)
#====================================================================================================
def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    rang = maxc - minc
    
    v = maxc
    if minc == maxc:
        return (0.0, 0.0, v)
    
    s = rang / maxc
    
    if r == maxc:
        h = (g - b) / rang
    elif g == maxc:
        h = 2.0 + (b - r) / rang
    else:
        h = 4.0 + (r - g) / rang
        
    h = (h / 6.0) % 1.0
    return (h, s, v)
#===========================================================================
def hsv_to_rgb(h_, s, v):
    h = h_ * 360
    c = v * s
    z = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, z, 0
    elif 60 <= h < 120:
        r, g, b = z, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, z
    elif 180 <= h < 240:
        r, g, b = 0, z, c
    elif 240 <= h < 300:
        r, g, b = z, 0, c
    elif 300 <= h <= 360:
        r, g, b = c, 0, z
    else:
        r, g, b = 0, 0, 0

    return (r + m, g + m, b + m)
#====================================================================================================
def rgb_to_oklab(r, g, b):
    rl = srgb_to_linear(r)
    gl = srgb_to_linear(g)
    bl = srgb_to_linear(b)

    l = 0.4122214708 * rl + 0.5363325363 * gl + 0.0514459929 * bl
    m = 0.2119034982 * rl + 0.6806995451 * gl + 0.1073969566 * bl
    s = 0.0883024619 * rl + 0.2817188376 * gl + 0.6299787005 * bl

    l_ = cbrt(l)
    m_ = cbrt(m)
    s_ = cbrt(s)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return (L, a, b)
#--------------------------------------------------
def oklab_to_oklch(l, a, b):
    c = sqrt(a**2 + b**2)
    h_rad = atan2(b, a)
    if h_rad < 0:
        h_rad += 2 * pi
    h = h_rad / (2*pi)
    return (h, c/max_range, l)
#--------------------------------------------------
def rgb_to_oklch(r, g, b):
    return oklab_to_oklch(*rgb_to_oklab(r, g, b))
#===========================================================================
def oklab_to_rgb(l, a, b):
    L = (1*l + 0.3963377774*a + 0.2158037573*b)**3
    m = (1*l + -0.1055613458*a + -0.0638541728*b)**3
    s = (1*l + -0.0894841775*a + -1.2914855480*b)**3

    rl = 4.0767416621*L + -3.3077115913*m + 0.2309699292*s
    gl = -1.2684380046*L + 2.6097574011*m + -0.3413193965*s
    bl = -0.0041960863*L + -0.7034186147*m + 1.7076147010*s

    # Black when outside rgb range
    if rl > 1.0 or gl > 1.0 or bl > 1.0 or rl < 0.0 or gl < 0.0 or bl < 0.0:
        return (0.0, 0.0, 0.0) #TODO change later, fix color gamut outside of range

    r = linear_to_srgb(rl)
    g = linear_to_srgb(gl)
    b = linear_to_srgb(bl)

    return (r, g, b)
#--------------------------------------------------
def oklch_to_oklab(h_normalized, c, l):
    c = c*max_range
    h_rad = h_normalized * 2 * pi
    return (l, c * cos(h_rad), c * sin(h_rad))
#--------------------------------------------------
def oklch_to_rgb(h, c, l):
    return oklab_to_rgb(*oklch_to_oklab(h, c, l))
#====================================================================================================
#==================================================

if __name__ == '__main__':
    pass
