# function file to import

from PIL import Image
from random import randint
#from copy import deepcopy
import re
import color_conversion as col
import mean_shift_clusturing as msc

palette_name = "palettes/brued.txt"
img_name = "image_2.png"
im = Image.open(img_name) # Can be many different formats.

#--------------------------#
if im.mode != "RGBA":      #
    im = im.convert("RGBA")#
#--------------------------#

img = im.load()
# w, h = im.size

#print(img[0, 0])  # Get the RGBA Value of the a pixel of an image
#pix[1, 0] = (0, 0, 0)  # Set the RGBA Value of the image (tuple)

white = (255,255,255,255)
black = (0,0,0,255)

# matrix_srgb_to_ciexyz = [
#     [0.4124564, 0.3575761, 0.1804375],
#     [0.2126729, 0.7151522, 0.0721750],
#     [0.0193339, 0.1191920, 0.9503041]
# ]

# matrix_ciexyz_to_lms = [
#     [0.8189330101, 0.3618667424, -0.1288597137],
#     [0.0329845436, 0.9293118715, 0.0361456387],
#     [0.0482003018, 0.2643662691, 0.6338517070]
# ]

# matrix_lms_to_oklab = [
#     [0.2104542553, 0.7936177850, -0.0040720468],
#     [1.9779984951, -2.4285922050, 0.4505937099],
#     [0.0259040371, 0.7827717662, -0.8086757660]
# ]

#==================================================
#--------------------------------------------------
def get_values(image, size):
    result = []
    line = []
    for y in range(size[1]):
        for x in range(size[0]):
            line.append(image[x, y])
        result.append(line)
        line = []
    return result
#--------------------------------------------------
def copy_values(pix):
    result = []
    line = []
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            line.append(pix[y][x])
        result.append(line)
        line = []
    return result
#--------------------------------------------------
def update_image(image, pix):
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            image[x, y] = pix[y][x]
    #return True
#--------------------------------------------------
# def convert_rgb_to_hsv(pix):

#     for y in range(len(pix)):
#         for x in range(len(pix[y])):
#             pix[y][x] = col.rgb_to_hsv(pix[y][x])
#--------------------------------------------------
# def convert_hsv_to_rgb(pix):

#     for y in range(len(pix)):
#         for x in range(len(pix[y])):
#             pix[y][x] = col.hsv_to_rgb(pix[y][x])
#--------------------------------------------------
def space_conversion(pix, my_function):

    for y in range(len(pix)):
        for x in range(len(pix[y])):
            pix[y][x] = my_function(pix[y][x])
    #return True
#--------------------------------------------------
# def rgb_to_srgb(rgb):

#     srgb = [
#         rgb[0]/255,
#         rgb[1]/255,
#         rgb[2]/255
#     ]

#     for i in range(len(srgb)):
#         if srgb[i] > 0.04045:
#             srgb[i] = ((srgb[i]+0.055)/1.055)**2.4
#         else:
#             srgb[i] = srgb[i]/12.92
    
#     srgb.append(rgb[3])

#     return srgb
#--------------------------------------------------
# def convert_rgb_to_srgb(pix):

#     for y in range(len(pix)):
#         for x in range(len(pix[y])):
#             pix[y][x] = rgb_to_srgb(pix[y][x])
#     #return True
#--------------------------------------------------
# def srgb_to_ciexyz(srgb):

#     ciexyz = []
#     for i in range(len(srgb)-1):
#         m = matrix_srgb_to_ciexyz[i]
#         ciexyz.append(srgb[0]*m[0] + srgb[1]*m[1] + srgb[2]*m[2])
#     ciexyz.append(srgb[3])

#     return ciexyz
#--------------------------------------------------
# def convert_srgb_to_ciexyz(pix):

#     for y in range(len(pix)):
#         for x in range(len(pix[y])):
#             pix[y][x] = srgb_to_ciexyz(pix[y][x])
#     #return True
#--------------------------------------------------
# def ciexyz_to_oklab(ciexyz):

#     lms = []
#     for i in range(len(ciexyz)-1):
#         m = matrix_ciexyz_to_lms[i]
#         lms.append(ciexyz[0]*m[0] + ciexyz[1]*m[1] + ciexyz[2]*m[2])
#     lms.append(ciexyz[3])

#     for i in range(len(lms)-1):
#         lms[i] = lms[i]**(1/3)
    
#     oklab = []
#     for i in range(len(lms)-1):
#         m = matrix_lms_to_oklab[i]
#         oklab.append(lms[0]*m[0] + lms[1]*m[1] + lms[2]*m[2])
#     oklab.append(lms[3])

#     return oklab
#--------------------------------------------------

# def rgb_to_oklab(rgb):

#     srgb = rgb_to_srgb(rgb)
#     ciexyz = srgb_to_ciexyz(srgb)
#     oklab = ciexyz_to_oklab(ciexyz)

#     return oklab
#--------------------------------------------------
def sort_palette(palette):
    return sorted(palette, key=lambda color: (col.rgb_to_hsv(color)[2],-(col.rgb_to_hsv(color)[1]),sum(color[0:3])/3))
#--------------------------------------------------
def grayscale(pix):# RGB values

    for y in range(len(pix)):
        for x in range(len(pix[y])):

            R = pix[y][x][0]
            G = pix[y][x][1]
            B = pix[y][x][2]
            A = pix[y][x][3]
            fbw = round(0.299*R+0.587*G+0.114*B)

            pix[y][x] = (fbw, fbw, fbw, A)
    #return True
#--------------------------------------------------
def hue_shifting(pix, shift=45):

    space_conversion(pix, col.rgb_to_hsv)

    for y in range(len(pix)):
        for x in range(len(pix[y])):

            H = pix[y][x][0]
            S = pix[y][x][1]
            V = pix[y][x][2]

            H = (H+shift)%360

            pix[y][x] = (H,S,V,pix[y][x][3])
    space_conversion(pix, col.hsv_to_rgb)
    #return True
#--------------------------------------------------
def ok_hue_shifting(pix, shift=45):

    space_conversion(pix, col.rgb_to_oklch)

    for y in range(len(pix)):
        for x in range(len(pix[y])):

            L = pix[y][x][0]
            C = pix[y][x][1]
            h = pix[y][x][2]

            if h >= 0:
                h -= ((shift%360)/100)*2
            else:
                h += ((shift%360)/100)*2

            pix[y][x] = (L,C,h,pix[y][x][3])
    space_conversion(pix, col.oklch_to_rgb)
    #return True
#--------------------------------------------------
def invert_colors(pix):

    for y in range(len(pix)):
        for x in range(len(pix[y])):

            R = 255 - pix[y][x][0]
            G = 255 - pix[y][x][1]
            B = 255 - pix[y][x][2]
            A = pix[y][x][3]

            pix[y][x] = (R,G,B,A)
    #return True
#--------------------------------------------------
def blur(pix, strengh=1):

    if strengh < 1:
        strengh = 1
    pix_copy = copy_values(pix)
    mean = []
    for y in range(len(pix_copy)):
        for x in range(len(pix_copy[y])):
            for a in range(-strengh, strengh+1):
                for b in range(-strengh, strengh+1):
                    if 0 <= y+a < len(pix) and 0 <= x+b < len(pix[y]):
                        mean.append(pix_copy[y+a][x+b])

            R = round(sum([i[0] for i in mean])/len(mean))
            G = round(sum([i[1] for i in mean])/len(mean))
            B = round(sum([i[2] for i in mean])/len(mean))
            A = round(sum([i[3] for i in mean])/len(mean))

            pix[y][x] = (R,G,B,A)
            mean = []
    #return True
#--------------------------------------------------
def edge_detection(pix):

    blurry_pix = copy_values(pix)
    blur(blurry_pix)

    for y in range(len(pix)):
        for x in range(len(pix[y])):
            R = abs(pix[y][x][0]-blurry_pix[y][x][0])
            G = abs(pix[y][x][1]-blurry_pix[y][x][1])
            B = abs(pix[y][x][2]-blurry_pix[y][x][2])
            A = pix[y][x][3]

            pix[y][x] = (R,G,B,A)
    #return True
#--------------------------------------------------
def threshold(pix, value=127):

    grayscale(pix)
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            if pix[y][x][0] >= value:
                pix[y][x] = (255,255,255,255)
            else:
                pix[y][x] = (0,0,0,255)
    #return True
#--------------------------------------------------
def simple_posterization(pix, level=8):

    if level < 1:
        level = 1

    for y in range(len(pix)):
        for x in range(len(pix[y])):
            R = int(round(pix[y][x][0]/(256/level))*(256/level))
            G = int(round(pix[y][x][1]/(256/level))*(256/level))
            B = int(round(pix[y][x][2]/(256/level))*(256/level))

            pix[y][x] = (R,G,B,255)
    #return True
#--------------------------------------------------
def randomizer(pix, chance=50):# in %

    pix_copy = copy_values(pix)
    for y in range(len(pix_copy)):
        for x in range(len(pix_copy[y])):
            if randint(1, 100) <= chance:
                a = randint(-1,1)
                b = randint(-1,1)
                if 0 <= y+a < len(pix) and 0 <= x+b < len(pix[y]):
                    pix[y][x] = pix_copy[y+a][x+b]
                    pix[y+a][x+b] = pix_copy[y][x]
    #return True
#--------------------------------------------------
def negate_blend(pix):

    for y in range(len(pix)):
        for x in range(len(pix[y])):
            R = round(255 - abs(255 - (2 * pix[y][x][0])))
            G = round(255 - abs(255 - (2 * pix[y][x][1])))
            B = round(255 - abs(255 - (2 * pix[y][x][2])))
            A = pix[y][x][3]

            pix[y][x] = (R,G,B,A)
    #return True
#--------------------------------------------------
def apply_palette(pix, p_name):
    
    palette = open(p_name,"r")

    used_colors = []
    color_list = []

    line = palette.readline()[0:8+3]
    while line != "":
        if re.search(";", line):
            pass
        elif re.search("[a-fA-F0-9]{8,8}", line):
            color = col.hex_to_rgb(re.search("[a-fA-F0-9]{8,8}", line).group())
            color_list.append(color)
        line = palette.readline()[0:8]
    
    for i in range(len(color_list)):
        if color_list[i] != white:
            used_colors.append(color_list[i])
        elif i < len(color_list)-1 and color_list[i+1] != white:
            used_colors.append(color_list[i])

    used_colors = sort_palette(used_colors)
    
    palette.close()

    grayscale(pix)
    simple_posterization(pix, len(used_colors)-1)

    color_total = []
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            if pix[y][x] not in color_total:
                color_total.append(pix[y][x])
    color_total.sort() # dark --> light

    # print("total color", color_total)
    # print("color list", color_list)
    # print("used colors", used_colors)

    for y in range(len(pix)):
        for x in range(len(pix[y])):
            for e in range(len(color_total)):
                # print("total ",e)
                if pix[y][x] == color_total[e]:
                    pix[y][x] = used_colors[e]
    #return True
#--------------------------------------------------
direction_list = ["up", "right", "down", "left"]
direction_map = {"up":(0,-1), "right":(1,0), "down":(0,1), "left":(-1,0)}

def gradient(pix, direction, first_color, second_color):

    # first_color = col.rgb_to_oklab(first_color)
    # second_color = col.rgb_to_oklab(second_color)

    delta = (second_color[0] - first_color[0],
             second_color[1] - first_color[1],
             second_color[2] - first_color[2],
             second_color[3] - first_color[3])
    
    if direction == "up" or direction == "down":
        lenght = len(pix)
    else:
        lenght = len(pix[0])+1

    step = (delta[0]/(lenght),
            delta[1]/(lenght),
            delta[2]/(lenght),
            delta[3]/(lenght))
    
    g_color = first_color
    g_list = [g_color]

    for i in range(lenght-1):
        g_color = (g_color[0] + step[0],
                   g_color[1] + step[1],
                   g_color[2] + step[2],
                   g_color[3] + step[3])
        g_list.append(g_color)

    if direction == "up" or direction == "left":
        i = 0
    else:
        i = -1

    for y in range(len(pix)):
        i += direction_map[direction][1]
        for x in range(len(pix[y])):
            i += direction_map[direction][0]
            direction_map[direction]
            pix[y][x] = (round(pix[y][x][0] - ((pix[y][x][0]-g_list[i][0])*(g_list[i][3]/255))),
                         round(pix[y][x][1] - ((pix[y][x][1]-g_list[i][1])*(g_list[i][3]/255))),
                         round(pix[y][x][2] - ((pix[y][x][2]-g_list[i][2])*(g_list[i][3]/255))),
                         round(pix[y][x][3] + (g_list[i][3]*(g_list[i][3]/255))))
        if direction == "right" or direction == "left":
            i = 0

    # for i in range(len(g_list)):
    #     pix[0][i] = g_list[i]

    #return True
#--------------------------------------------------
def clustering_posterization(pix, cell= 8, radius= 16):

    color_list = msc.mean_shift_clusturing(pix, cell, radius)
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            nearest = (color_list[0], msc.distance(pix[y][x], color_list[0]))
            for i in color_list:
                if msc.distance(pix[y][x], i) < nearest[1]:
                    nearest = (i, msc.distance(pix[y][x], i))
            pix[y][x] = nearest[0]
    #return True
#--------------------------------------------------
def bloom(pix, threshold_value=127, blur_strengh=1, bloom_strengh=64):
    pix_copy = copy_values(pix)
    grayscale(pix_copy)
    threshold(pix_copy, threshold_value)
    blur(pix_copy, blur_strengh)
    for y in range(len(pix)):
        for x in range(len(pix[y])):
            R = pix[y][x][0] + round(pix_copy[y][x][0] * (bloom_strengh/255))
            G = pix[y][x][1] + round(pix_copy[y][x][1] * (bloom_strengh/255))
            B = pix[y][x][2] + round(pix_copy[y][x][2] * (bloom_strengh/255))
            A = pix[y][x][3]

            if R > 255:
                R = 255
            if G > 255:
                G = 255
            if B > 255:
                B = 255

            pix[y][x] = (R,G,B,A)
    #return True
#==================================================
if img[0, 0] == 0:   #
    exit()           #
#--------------------#
# pixel_list = get_values(img, im.size)

# print("pixel_list[0][0] >>>", pixel_list[0][0])

#print(ciexyz_to_oklab(srgb_to_ciexyz(rgb_to_srgb((255,128,32,255)))))
#print(ciexyz_to_oklab((0,1,0,255)))
#print(oklab_to_oklch(rgb_to_oklab((255,128,32,255))))

# gradient(pixel_list, "right", (255,0,0,255), (0,0,255,64))

# print(msc.mean_shift(msc.celled_list(pixel_list), (255,127,0,255)))
# print(msc.mean_shift_clusturing(pixel_list, 8, 16))
# print(msc.celled_list(pixel_list))
# clustering_posterization(pixel_list)

# col.abc_print("functions work correctly")
# grayscale(pixel_list)

# update_image(img, pixel_list)

#==================================================

# Save the modified pixels as .png
# im.save(f"{img_name[0:len(img_name)-4]}_new{img_name[len(img_name)-4:len(img_name)]}")

#==================================================

print("editing_filters.py LOADED")


