#delta_s_image_editer

import pygame, sys
from pygame.locals import *
import tkinter
from tkinter import filedialog
from PIL import Image
from inspect import getmembers, isfunction, signature, _empty
import editing_filters as edit
import time

# param = signature(edit.blur)
# print(param)
# print(len(param.parameters))

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

#--------------------
black = (0,0,0)
gray_darker = (18,18,20)
gray_dark = (26,26,30)
gray = (33,34,38)
gray_light = (56,56,61)
gray_5 = (93,95,103)
gray_lighter = (155,155,162)
white = (255,255,255)
#--------------------
fenetre.fill(gray_darker)

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

def waiting_file(format):

    size = text_size("Click to open file")
    x = (WIDTH/2 - size[0]/2 - 5)
    y = (HEIGHT/2 - size[1]/2 - 5)
    while True:
        
        for event in pygame.event.get():
            security(event)
            #--------------------------------------------------
            if format == "image":
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

                fenetre.fill(gray_darker)
                button_text(gray_light, "Click to open file", white, (WIDTH/2-size[0]/2-5,HEIGHT/2-size[1]/2-5))
                pygame.display.flip()
            #--------------------------------------------------
            if format == "text":
                tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
                p = filedialog.askopenfilename()
                if p == "":
                    return False
                else:
                    if p[len(p)-4:len(p)] == ".txt":
                        return p

#====================================================================================================
def filters_ui():

    pygame.draw.rect(fenetre, (gray_dark), (WIDTH/2, 0, WIDTH, HEIGHT))
    pygame.draw.rect(fenetre, (gray_darker), (WIDTH/2, 0, WIDTH, 15+(5*50)))
    pygame.draw.rect(fenetre, (gray_darker), (WIDTH/2, HEIGHT-110, WIDTH, HEIGHT))

    #filters buttons
    for i in range(-2, 3):
        if i == 0:
            button_text(gray_light, (func_list[current].replace("_", " ").capitalize()), white, (WIDTH/2+10, 110))
        else:
            button_text(gray, (func_list[(current+i) % len(func_list)].replace("_", " ").capitalize()), gray_lighter, (WIDTH/2+10, 110+(i*50)))

    #parameters buttons
    if func_list[current] != "apply_palette":
        i = 0
        for e in options.keys():
            button_text(gray_light, f"{e.replace("_", " ")}: {options[e]}", white, (WIDTH/2+10, HEIGHT/2+(i*50)))
            i += 1
    if func_list[current] == "gradient":
        pygame.draw.rect(fenetre, (options["first_color"][0:3]), (WIDTH/2+30+text_size(f"first color: {options["first_color"]}")[0], HEIGHT/2+(1*50), 40, 40))
        pygame.draw.rect(fenetre, (options["second_color"][0:3]), (WIDTH/2+30+text_size(f"second color: {options["second_color"]}")[0], HEIGHT/2+(2*50), 40, 40))



    button_text(gray_light, "Test", white, (WIDTH/2+10, HEIGHT-text_size("Test")[1]-20))
    button_text(gray_light, "Clear filter", white, (WIDTH/2+10, HEIGHT-text_size("Clear filter")[1]-20-50))
    button_text(gray_light, "Apply", white, (WIDTH-text_size("Apply")[0]-20, HEIGHT-text_size("Apply")[1]-20))
    button_text(gray_light, "Save", white, (WIDTH-text_size("Save")[0]-20, HEIGHT-text_size("Save")[1]-20-50))
#====================================================================================================
def apply_filter(pix, opt):
    filt = getattr(edit, func_list[current])

    #--------------------
    if func_list[current] == "apply_palette":
        palette = waiting_file("text")
        if not palette:
            return False
        start = time.time()
        filt(pix, palette)
        return time.time() - start
    #--------------------
    start = time.time()
    if np == 1:
        filt(pix)
    else:
        filt(pix, *opt.values())
    return time.time() - start
#====================================================================================================
def param_func(param, func):
    print(func)
    dico = {}
    if func != "gradient":
        for i in param.parameters:
            if i == "pix":
                pass
            elif param.parameters[i].default == _empty:
                dico[i] = 0
            else:
                dico[i] = param.parameters[i].default
    else:
        dico["direction"] = "down"
        dico["first_color"] = (255,0,0,255)
        dico["second_color"] = (0,0,255,255)
    return dico
#////////////////////////////////////////////////////////////////////////////////////////////////////



file_path = waiting_file("image")
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
param = signature(func)
options = param_func(param, func_list[current])
last_update = ""

#====================================================================================================

while True : #TODO fix gradient's parameters + optimization(maybe not)
    
    for event in pygame.event.get():
        security(event)



        if event.type == MOUSEBUTTONDOWN and event.button == 1 :

            mouse_co = pygame.mouse.get_pos()
            #--------------------------------------------------
            #click on "Test" button
            if (WIDTH/2+10) <= mouse_co[0] <= (WIDTH/2+text_size("Test")[0]+20) and (HEIGHT-text_size("Test")[1]-20) <= mouse_co[1] <= (HEIGHT-10):

                pixel_list = edit.copy_values(pixel_real)
                update_time = apply_filter(pixel_list, options)
                edit.update_image(img, pixel_list)

                edited = pygame.image.frombytes(im.tobytes(), im.size, im.mode)
                edited = pygame.transform.scale_by(edited, round((WIDTH/2)/im.size[0], 1)-0.1)
                if update_time:
                    last_update = f"updated in {round((update_time)*1000)} ms"
                else:
                    last_update = ""
            #--------------------------------------------------
            #click on "Apply" button
            if (WIDTH-text_size("Apply")[0]-20) <= mouse_co[0] <= (WIDTH-10) and (HEIGHT-text_size("Apply")[1]-20) <= mouse_co[1] <= (HEIGHT-10):
                
                start = time.time()

                pixel_real = edit.copy_values(pixel_list)
                edit.update_image(img, pixel_list)

                last_update = f"applied in {round((time.time() - start)*1000)} ms"
            #--------------------------------------------------
            #click on "Clear filter" button
            if (WIDTH/2+10) <= mouse_co[0] <= (WIDTH/2+text_size("Clear filter")[0]+20) and (HEIGHT-text_size("Clear filter")[1]-20-50) <= mouse_co[1] <= (HEIGHT-10-50):
                
                start = time.time()

                pixel_list = edit.copy_values(pixel_real)
                edit.update_image(img, pixel_list)

                edited = pygame.image.frombytes(im.tobytes(), im.size, im.mode)
                edited = pygame.transform.scale_by(edited, round((WIDTH/2)/im.size[0], 1)-0.1)

                last_update = f"cleared in {round((time.time() - start)*1000)} ms"
            #--------------------------------------------------
            #click on "Save" button
            if (WIDTH-text_size("Save")[0]-20) <= mouse_co[0] <= (WIDTH-10) and (HEIGHT-text_size("Save")[1]-20-50) <= mouse_co[1] <= (HEIGHT-10-50):
                
                im.save(f"{file_path[0:len(file_path)-4]}_new{file_path[len(file_path)-4:len(file_path)]}")
                last_update = "image saved"
            #--------------------------------------------------



        if event.type == MOUSEWHEEL:

            mouse_co = pygame.mouse.get_pos()
            #--------------------------------------------------
            #scroll on filters
            if WIDTH/2 <= mouse_co[0] <= WIDTH and 0 <= mouse_co[1] <= 10+(5*50):

                current = (current - event.y) % len(func_list)
                func = getattr(edit, func_list[current])
                np = len(signature(func).parameters)
                param = signature(func)
                options = param_func(param, func_list[current])
            #--------------------------------------------------
            #scroll on filters' parameters
            i = 0
            for e in options:
                if (WIDTH/2+10) <= mouse_co[0] <= (WIDTH/2+10+text_size(f"{e}: {options[e]}")[0]+10) and (HEIGHT/2+(i*50)) <= mouse_co[1] <= (HEIGHT/2+(i*50)+text_size(f"{e}: {options[e]}")[1]+10):
                    keys = pygame.key.get_pressed()
                    if func_list[current] != "gradient":
                        if keys[K_LSHIFT] or keys[K_RSHIFT]:#if shift is held down, scroll 10x faster
                            options[e] -= event.y * 10
                        else:
                            options[e] -= event.y
                    else:
                        if i == 0:
                            options[e] = edit.direction_list[(edit.direction_list.index(options[e]) - event.y) % len(edit.direction_list)]
                        else:
                            if keys[K_LSHIFT] or keys[K_RSHIFT]:#if shift is held down, scroll 10x faster
                                if keys[K_r]:
                                    options[e] = (options[e][0]-(event.y*10), options[e][1], options[e][2], options[e][3])
                                if keys[K_g]:
                                    options[e] = (options[e][0], options[e][1]-(event.y*10), options[e][2], options[e][3])
                                if keys[K_b]:
                                    options[e] = (options[e][0], options[e][1], options[e][2]-(event.y*10), options[e][3])
                                if keys[K_a]:
                                    options[e] = (options[e][0], options[e][1], options[e][2], options[e][3]-(event.y*10)) 
                            else:
                                if keys[K_r]:
                                    options[e] = (options[e][0]-event.y, options[e][1], options[e][2], options[e][3])
                                if keys[K_g]:
                                    options[e] = (options[e][0], options[e][1]-event.y, options[e][2], options[e][3])
                                if keys[K_b]:
                                    options[e] = (options[e][0], options[e][1], options[e][2]-event.y, options[e][3])
                                if keys[K_a]:
                                    options[e] = (options[e][0], options[e][1], options[e][2], options[e][3]-event.y)
                            rgba = [options[e][0], options[e][1], options[e][2], options[e][3]]
                            
                            for x in range(4):
                                if rgba[x] > 255:
                                    rgba[x] = 255
                                if rgba[x] < 0:
                                    rgba[x] = 0
                                options[e] = (rgba[0], rgba[1], rgba[2], rgba[3])
                i += 1
            #--------------------------------------------------



    fenetre.fill(black)# 1
    filters_ui()# 2
    text(last_update, gray_5, ((WIDTH-WIDTH/4-text_size(last_update)[0]/2), HEIGHT-text_size(last_update)[1]-15))
    fenetre.blit(edited, (((WIDTH/2)-edited.get_width())/2, (HEIGHT/2)-(edited.get_height()/2)))

    pygame.display.flip()

#====================#====================#====================#====================#================
pygame.display.quit()#   
sys.exit()           #
#====================#
