#delta-s_image_editer

import pygame, sys
from pygame.locals import *
import tkinter
from tkinter import filedialog
from PIL import Image
from inspect import getmembers, isfunction, signature
from math import floor
import editing_filters as edit
import time

param = signature(edit.blur)
print(param)
print(len(param.parameters))

func_list = [i[0] for i in getmembers(edit, isfunction)]
for e in ["copy_values", "get_values", "sort_palette", "space_conversion", "update_image"]:
    func_list.remove(e)

#////////////////////////////////////////////////////////////////////////////////////////////////////

pygame.init()

screen_size = pygame.display.Info()
# print(screen_size)

format_list = [".png", ".jpeg", ".jpg", ".webp"]

FPS = 60
WIDTH = screen_size.current_w - (screen_size.current_w//10)
HEIGHT = screen_size.current_h - (screen_size.current_h//10)

pygame.display.set_caption("Delta's image editor")
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(pygame.font.get_default_font(), 32)

white = (255,255,255)
black = (0,0,0)
b_gray = (93,95,103)
t_gray = (190,193,198)
b_color = (40,40,45)
t_color = (100,101,110)
ui_top = (12,12,15)
background = (18,18,20)

fenetre.fill(background)

pygame.display.flip()

#////////////////////////////////////////////////////////////////////////////////////////////////////

def security(e):
    if e.type == pygame.QUIT:
        pygame.display.quit()    
        sys.exit()

#====================================================================================================

def button(color, co, size):
    pygame.draw.rect(fenetre, color, (co[0], co[1], size[0], size[1]))

#====================================================================================================

def text(taxt, color, co):
    t = font.render(taxt, True, color) 
    fenetre.blit(t, dest=(co[0], co[1]))

#====================================================================================================

def button_text(color, text, t_color, t_co):

    b_text = font.render(text, True, t_color)
    t_w = b_text.get_size()[0]
    t_h = b_text.get_size()[1]
    # print(b_text.get_size())
    button(color, (t_co[0], t_co[1]), (t_w+10, t_h+10))
    fenetre.blit(b_text, dest=((t_co[0]+5),(t_co[1]+5)))

#====================================================================================================
def text_size(text):
    b_text = font.render(text, True, white)
    t_w = b_text.get_size()[0]
    t_h = b_text.get_size()[1]
    return (t_w, t_h)
#====================================================================================================

def waiting_file():

    size = text_size("click to open file")
    x = (WIDTH/2 - size[0]/2 - 5)
    y = (HEIGHT/2 - size[1]/2 - 5)
    while True:

        for event in pygame.event.get():
            security(event)


            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                mouse_co = pygame.mouse.get_pos()
                print(f"x{mouse_co[0]}   y{mouse_co[1]}")
                
                #----------PAUSE/PLAY
                if x <= mouse_co[0] <= x+size[0]+10 and y <= mouse_co[1] <= y+size[1]+10:
                    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
                    p = filedialog.askopenfilename()
                    if p != "":
                        for i in format_list:
                            if p[len(p)-len(i):len(p)] in format_list:
                                return p
                        print("invalid format")

        fenetre.fill(background)
        button_text(b_color, "click to open file", white, (WIDTH/2-size[0]/2-5,HEIGHT/2-size[1]/2-5))
        pygame.display.flip()

#====================================================================================================
def change_file():
    pass
#====================================================================================================
def filters_ui():

    pygame.draw.rect(fenetre, (background), (WIDTH/2, 0, WIDTH, HEIGHT))
    pygame.draw.rect(fenetre, (ui_top), (WIDTH/2, 0, WIDTH, 15+(5*50)))
    text((f"{str(np)} {param}"), white, (WIDTH/2, HEIGHT/2-60))

    for i in range(-2, 3):
        if i == 0:
            button_text(b_color, func_list[current], white, (WIDTH/2+10, 110))
        else:
            button_text(b_color, func_list[(current+i) % len(func_list)], t_color, (WIDTH/2+10, 110+(i*50)))

    for i in range(len(options)):
        button_text(b_color, str(options[i]), white, (WIDTH-WIDTH/4, HEIGHT/2+(i*50)))

    button_text(b_color, "Test", white, (WIDTH/2+10, HEIGHT-text_size("Test")[1]-20))
    button_text(b_color, "Clear filter", white, (WIDTH/2+10, HEIGHT-text_size("Clear filter")[1]-20-50))
    button_text(b_color, "Apply", white, (WIDTH-text_size("Apply")[0]-20, HEIGHT-text_size("Apply")[1]-20))
#====================================================================================================
def apply_filter(pix, opt):
    filt = getattr(edit, func_list[current])

    if np == 1:
        print("ok")
        filt(pix)
    else:
        filt(pix, *opt)
#////////////////////////////////////////////////////////////////////////////////////////////////////


# print(func_list)
file_path = waiting_file()
# print("ABC",file_path)
im = Image.open(file_path)

#--------------------------#
if im.mode != "RGBA":      #
    im = im.convert("RGBA")#
#--------------------------#

img = im.load()
pixel_list = edit.get_values(img, im.size)
pixel_real = edit.copy_values(pixel_list)

edited = pygame.image.frombytes(im.tobytes(), im.size, im.mode)
edited = pygame.transform.scale_by(edited, round((WIDTH/2)/im.size[0], 1)-0.1)

print(round((WIDTH/2)/im.size[0], 1))

current = 0
func = getattr(edit, func_list[current])
np = len(signature(func).parameters)
param = str(signature(func))
options = [0 for _ in range(np-1)]
last_update = ""

#====================================================================================================

while True :
    
    for event in pygame.event.get():
        security(event)



        if event.type == MOUSEBUTTONDOWN and event.button == 1 :

            mouse_co = pygame.mouse.get_pos()
            #--------------------------------------------------
            #click on "Test" button
            if (WIDTH/2+10) <= mouse_co[0] <= (WIDTH/2+text_size("Test")[0]+20) and (HEIGHT-text_size("Test")[1]-20) <= mouse_co[1] <= (HEIGHT-10):

                start = time.time()

                pixel_list = edit.copy_values(pixel_real)
                apply_filter(pixel_list, options)
                # edit.hue_shifting(pixel_list, 45)
                edit.update_image(img, pixel_list)

                edited = pygame.image.frombytes(im.tobytes(), im.size, im.mode)
                edited = pygame.transform.scale_by(edited, round((WIDTH/2)/im.size[0], 1)-0.1)

                last_update = f"updated in {round((time.time() - start)*1000)} ms"
            #--------------------------------------------------
            #click on "Apply" button
            if (WIDTH-text_size("Apply")[0]-20) <= mouse_co[0] <= (WIDTH-10) and (HEIGHT-text_size("Apply")[1]-20) <= mouse_co[1] <= (HEIGHT-10):
                
                start = time.time()

                pixel_real = edit.copy_values(pixel_list)
                edit.update_image(img, pixel_list)

                last_update = f"updated in {round((time.time() - start)*1000)} ms"
            #--------------------------------------------------
            #click on "Clear filter" button
            if (WIDTH/2+10) <= mouse_co[0] <= (WIDTH/2+text_size("Clear filter")[0]+20) and (HEIGHT-text_size("Clear filter")[1]-20-50) <= mouse_co[1] <= (HEIGHT-10-50):
                
                start = time.time()

                pixel_list = edit.copy_values(pixel_real)
                edit.update_image(img, pixel_list)

                edited = pygame.image.frombytes(im.tobytes(), im.size, im.mode)
                edited = pygame.transform.scale_by(edited, round((WIDTH/2)/im.size[0], 1)-0.1)

                last_update = f"updated in {round((time.time() - start)*1000)} ms"
            #--------------------------------------------------


        if event.type == MOUSEWHEEL:

            mouse_co = pygame.mouse.get_pos()
            #--------------------------------------------------
            #scroll on filters
            if WIDTH/2 <= mouse_co[0] <= WIDTH and 0 <= mouse_co[1] <= 10+(5*50):

                current = (current - event.y) % len(func_list)
                func = getattr(edit, func_list[current])
                np = len(signature(func).parameters)
                param = str(signature(func))
                options = [0 for _ in range(np-1)]
            #--------------------------------------------------
            #scroll on filters' parameters
            for e in range(len(options)):
                if (WIDTH-WIDTH/4) <= mouse_co[0] <= (WIDTH-WIDTH/4+text_size(str(options[e]))[0]+10) and (HEIGHT/2+(e*50)) <= mouse_co[1] <= (HEIGHT/2+(e*50)+text_size(str(options[e]))[1]):
                    keys = pygame.key.get_pressed()

                    if keys[K_LSHIFT] or keys[K_RSHIFT]:#if shift is held down, scroll is 10x faster
                        options[e] -= (event.y)*10
                    else:
                        options[e] -= event.y

                    # abc = pygame.key.get_pressed()
                    # print(abc)
                    # print(type(abc))
                    # print(abc[pygame.K_LSHIFT])







    fenetre.fill(black)# 1
    filters_ui()# 2
    text(last_update, b_gray, ((WIDTH-WIDTH/4-text_size(last_update)[0]/2), HEIGHT-text_size(last_update)[1]-15))
    fenetre.blit(edited, (((WIDTH/2)-edited.get_width())/2, (HEIGHT/2)-(edited.get_height()/2)))

    pygame.display.flip()

#====================#====================#====================#====================#================
pygame.display.quit()#   
sys.exit()           #
#====================#
