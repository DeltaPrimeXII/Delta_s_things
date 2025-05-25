# function file to import

from math import sqrt, cbrt, cos, sin, atan2

#----------------------------------------------------------------------------------------------------

# Lab linear_srgb_to_oklab(RGB c) 
# {
#   float l = 0.4122214708f * c.r + 0.5363325363f * c.g + 0.0514459929f * c.b;
# 	float m = 0.2119034982f * c.r + 0.6806995451f * c.g + 0.1073969566f * c.b;
# 	float s = 0.0883024619f * c.r + 0.2817188376f * c.g + 0.6299787005f * c.b;

#     float l_ = cbrtf(l);
#     float m_ = cbrtf(m);
#     float s_ = cbrtf(s);

#     return {
#         0.2104542553f*l_ + 0.7936177850f*m_ - 0.0040720468f*s_,
#         1.9779984951f*l_ - 2.4285922050f*m_ + 0.4505937099f*s_,
#         0.0259040371f*l_ + 0.7827717662f*m_ - 0.8086757660f*s_,
#     };
# }

matrix_rgb_to_lms = [
    [0.4122214708, 0.5363325363, 0.0514459929],
    [0.2119034982, 0.6806995451, 0.1073969566],
    [0.0883024619, 0.2817188376, 0.6299787005]
]

matrix_lms_to_oklab = [
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660]
]

#----------------------------------------------------------------------------------------------------

# RGB oklab_to_linear_srgb(Lab c) 
# {
#     float l_ = c.L + 0.3963377774f * c.a + 0.2158037573f * c.b;
#     float m_ = c.L - 0.1055613458f * c.a - 0.0638541728f * c.b;
#     float s_ = c.L - 0.0894841775f * c.a - 1.2914855480f * c.b;

#     float l = l_*l_*l_;
#     float m = m_*m_*m_;
#     float s = s_*s_*s_;

#     return {
# 		+4.0767416621f * l - 3.3077115913f * m + 0.2309699292f * s,
# 		-1.2684380046f * l + 2.6097574011f * m - 0.3413193965f * s,
# 		-0.0041960863f * l - 0.7034186147f * m + 1.7076147010f * s,
#     };
# }

matrix_oklab_to_lms = [
    [1, 0.3963377774, 0.2158037573],
    [1, -0.1055613458, -0.0638541728],
    [1, -0.0894841775, -1.2914855480]
]

matrix_lms_to_rgb = [
    [4.0767416621, -3.3077115913, 0.2309699292],
    [-1.2684380046, 2.6097574011, -0.3413193965],
    [-0.0041960863, -0.7034186147, 1.7076147010]
]

#====================================================================================================
def hex_to_rgb(hex):# "FF000000"
    r = int(hex[2:4],16)
    g = int(hex[4:6],16)
    b = int(hex[6:8],16)
    a = int(hex[0:2],16)
    return (r,g,b,a)
#====================================================================================================
def round_rgb(rgb):
    return (round(rgb[0]), round(rgb[1]), round(rgb[2]), rgb[3])
#====================================================================================================
def rgb_to_hsv(rgb):

    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255

    cmax, cmin = max(r,g,b), min(r,g,b)
    delta = cmax - cmin
    v = cmax

    if v == 0:
        s = 0
    else:
        s = delta/v
                
    if r == g and g == b:
        h = 0
    elif r == cmax:
        h = 60*((g-b)/(cmax-cmin))
    elif g == cmax:
        h = 60*((b-r)/(cmax-cmin)+2)
    elif b == cmax:
        h = 60*((r-g)/(cmax-cmin)+4)

    h = h % 360

    return (h, s, v, rgb[3])
#====================================================================================================
def hsv_to_rgb(hsv):

    h = hsv[0]
    s = hsv[1]
    v = hsv[2]

    c = v*s
    z = c*(1-abs((h/60)%2-1))
    m = v-c

    if 0 <= h < 60:
        r,g,b = c,z,0
    elif 60 <= h < 120:
        r,g,b = z,c,0
    elif 120 <= h < 180:
        r,g,b = 0,c,z
    elif 180 <= h < 240:
        r,g,b = 0,z,c
    elif 240 <= h < 300:
        r,g,b = z,0,c
    elif 300 <= h <= 360:
        r,g,b = c,0,z

    r = round((r+m)*255)
    g = round((g+m)*255)
    b = round((b+m)*255)

    return (r, g, b, hsv[3])
#====================================================================================================
def rgb_to_oklab(rgb):

    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255

    # oklab = []
    # lms = []
    # for i in range(3):
    #     lms.append(matrix_rgb_to_lms[i][0]*r
    #                + matrix_rgb_to_lms[i][1]*g
    #                + matrix_rgb_to_lms[i][2]*b)
    
    l = cbrt(matrix_rgb_to_lms[0][0]*r + matrix_rgb_to_lms[0][1]*g + matrix_rgb_to_lms[0][2]*b)
    m = cbrt(matrix_rgb_to_lms[1][0]*r + matrix_rgb_to_lms[1][1]*g + matrix_rgb_to_lms[1][2]*b)
    s = cbrt(matrix_rgb_to_lms[2][0]*r + matrix_rgb_to_lms[2][1]*g + matrix_rgb_to_lms[2][2]*b)
    
    # for i in range(3):
    #     lms[i] = lms[i]**(1/3)
    
    # for i in range(3):
    #     oklab.append(matrix_lms_to_oklab[i][0]*lms[0]
    #                  + matrix_lms_to_oklab[i][1]*lms[1]
    #                  + matrix_lms_to_oklab[i][2]*lms[2])
        
    L = matrix_lms_to_oklab[0][0]*l + matrix_lms_to_oklab[0][1]*m + matrix_lms_to_oklab[0][2]*s
    a = matrix_lms_to_oklab[1][0]*l + matrix_lms_to_oklab[1][1]*m + matrix_lms_to_oklab[1][2]*s
    b = matrix_lms_to_oklab[2][0]*l + matrix_lms_to_oklab[2][1]*m + matrix_lms_to_oklab[2][2]*s
    
    # oklab.append(rgb[3])
    return (L, a, b, rgb[3])
#====================================================================================================
def oklab_to_rgb(oklab):

    L = oklab[0]
    a = oklab[1]
    b = oklab[2]

    l = (matrix_oklab_to_lms[0][0]*L + matrix_oklab_to_lms[0][1]*a + matrix_oklab_to_lms[0][2]*b)**(3)
    m = (matrix_oklab_to_lms[1][0]*L + matrix_oklab_to_lms[1][1]*a + matrix_oklab_to_lms[1][2]*b)**(3)
    s = (matrix_oklab_to_lms[2][0]*L + matrix_oklab_to_lms[2][1]*a + matrix_oklab_to_lms[2][2]*b)**(3)

    r = round((matrix_lms_to_rgb[0][0]*l + matrix_lms_to_rgb[0][1]*m + matrix_lms_to_rgb[0][2]*s)*255)
    g = round((matrix_lms_to_rgb[1][0]*l + matrix_lms_to_rgb[1][1]*m + matrix_lms_to_rgb[1][2]*s)*255)
    b = round((matrix_lms_to_rgb[2][0]*l + matrix_lms_to_rgb[2][1]*m + matrix_lms_to_rgb[2][2]*s)*255)

    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255

    return (r, g, b, oklab[3])
#====================================================================================================
def oklab_to_oklch(oklab):
    
    L = oklab[0]
    a = oklab[1]
    b = oklab[2]

    C = sqrt((a**2)+(b**2))
    h = atan2(b, a)

    return (L, C, h, oklab[3])
#====================================================================================================
def oklch_to_oklab(oklch):

    L = oklch[0]
    C = oklch[1]
    h = oklch[2]

    a = C * cos(h)
    b = C * sin(h)

    return (L, a, b, oklch[3])
#====================================================================================================
def rgb_to_oklch(rgb):
    oklab = rgb_to_oklab(rgb)
    return oklab_to_oklch(oklab)
#====================================================================================================
def oklch_to_rgb(oklch):
    oklab = oklch_to_oklab(oklch)
    return oklab_to_rgb(oklab)
#////////////////////////////////////////////////////////////////////////////////////////////////////

# print("HEX ",hex_to_rgb("FF4E118B"))

# print("HSV ",rgb_to_hsv((255,128,32,255)))

# print("RGB ",hsv_to_rgb((182,0.85,0.71,255)))

# print("OKLAB ",rgb_to_oklab((128,255,32,255)))
# >>> OKLAB  (0.9250689770584022, -0.12471383990366397, 0.15199924064383585, 255)

# print('RGB ',oklab_to_rgb((0.9250689770584022, -0.12471383990366397, 0.15199924064383585, 255)))
# >>> RGB  (128, 255, 32, 255)

# print("OKLCH ",oklab_to_oklch((0.9250689770584022, -0.12471383990366397, 0.15199924064383585, 255)))
# >>> OKLCH  (0.9250689770584022, 0.19661462565083873, 2.2579068312281776, 255)

# print("OKLAB ",oklch_to_oklab((0.9250689770584022, 0.19661462565083873, 2.2579068312281776, 255)))
# OKLAB  (0.9250689770584022, -0.12471383990366397, 0.15199924064383585, 255)

# print(rgb_to_hsv((255,0,0,255)))
# print(rgb_to_oklch((255,0,0,255)))

# print(rgb_to_hsv((0,255,255,255)))
# print(rgb_to_oklch((0,255,255,255)))

# print(oklch_to_rgb((0.5,0.37,(30/360),255)))

print("color_conversion.py LOADED")



