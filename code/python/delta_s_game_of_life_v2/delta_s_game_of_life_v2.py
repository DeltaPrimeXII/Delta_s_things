#Delta's game of life v2

import pygame, sys
from pygame.locals import *
import time

pygame.init()

WIDTH = 738
HEIGHT = 512


fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Delta's Game of Life v2")

font = pygame.font.Font(pygame.font.get_default_font(), 36)
font_mini = pygame.font.Font(pygame.font.get_default_font(), 18)
# FPS = 60

B = 40
left = 10
right = WIDTH-10
top = 10
bottom = HEIGHT-10

background = (14,15,19)
l_gray = (30,33,41)
white = (255,255,255)
b_gray = (93,95,103)
t_gray = (190,193,198)

fenetre.fill(background)
pygame.display.flip()


#--------------------------------------------------
def security():
    if event.type == pygame.QUIT:
        pygame.display.quit()
        sys.exit()
#--------------------------------------------------
def draw_grid(px, offset):
    if not px <= 5:
        for x in range(0, WIDTH, px):
            pygame.draw.line(fenetre, l_gray, (x+(offset[0]%px), 0), (x+(offset[0]%px), HEIGHT))
        for y in range(0, HEIGHT, px):
            pygame.draw.line(fenetre, l_gray, (0, y+(offset[1]%px)), (WIDTH, y+(offset[1]%px)))
#--------------------------------------------------
def calcul(grid):
    calcul_grid = {}
    for i in grid:
        calcul_grid[i] = 0
    for i in grid:
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not (x==0 and y==0):
                    if not (i[0]+x, i[1]+y) in calcul_grid.keys():
                        # if x==0 and y==0:
                        #     calcul_grid[i] = [0, False]
                        # else:
                        calcul_grid[(i[0]+x, i[1]+y)] = 1
                    else:
                        calcul_grid[(i[0]+x, i[1]+y)] += 1
    # for i in grid:
    #     calcul_grid[i][1] = True
    return calcul_grid
#--------------------------------------------------
def execute(grid, temp_grid):
    calcul_grid = []

    for i in grid:
        if 2 <= temp_grid[i] <= 3:
            calcul_grid.append(i)
            temp_grid.pop(i)

    for k, v in temp_grid.items():
        if v == 3:
            calcul_grid.append(k)
    
    return calcul_grid
#--------------------------------------------------
def show_grid(grid, scale, off):
    for i in grid:
        pygame.draw.rect(fenetre,(0,184,212),(i[0]*scale+off[0], i[1]*scale+off[1], scale, scale))
#--------------------------------------------------
def new_gen():
    global cell_layer, calcul_layer, px, offset
    # print("before",cell_layer)
    # print("before",calcul_layer)
    calcul_layer = calcul(cell_layer)
    # print(calcul_layer)
    cell_layer = execute(cell_layer, calcul_layer)
    # print(cell_layer)
    # calcul_layer = {}

    # show_grid(cell_layer, px, offset)
#--------------------------------------------------
def update():
    global background, cell_layer, px, offset, delay, gen, cells, speed_size

    #Background
    fenetre.fill(background)
    #Elements
    show_grid(cell_layer, px, offset)
    draw_grid(px, offset)
    #UI
    cells = len(cell_layer)
    text_gen = font.render(f"Gen {gen}", True, (t_gray))
    text_cells = font.render(f"Cells {cells}", True, (t_gray))
    text_fps = font_mini.render(f"{last_fps} fps", True, (t_gray))
    fenetre.blit(text_fps, dest=(left,top+B+B))
    fenetre.blit(text_gen, dest=(left,top))
    fenetre.blit(text_cells, dest=(left,top+B))
    speed_button(delay, speed_size)
    if paused:
        step_button()
#--------------------------------------------------
def text_size(text):

    b_text = font.render(text, True, white)
    t_w = b_text.get_size()[0]
    t_h = b_text.get_size()[1]
    return (t_w, t_h)
#--------------------------------------------------
def speed_button(delay, speed_size):
    
    button(right-B, top, "more")
    button(right-B, top+B+10, "less")
    if delay == "max":
        text_speed = font.render(delay, True, (t_gray))
        fenetre.blit(text_speed, dest=((right-B-speed_size[0]-10),(top+5)))
    else:
        text_speed = font.render(f"{delay} gen/s", True, (t_gray))
        fenetre.blit(text_speed, dest=((right-B-speed_size[0]+10),(top+5)))
#--------------------------------------------------
def step_button():

    button(left, bottom-B, "square")
    pygame.draw.polygon(fenetre,(white),[(25,HEIGHT-40),(35,HEIGHT-30),(25,HEIGHT-20)],width=0)

    text_step = font.render("step", True, (t_gray))
    fenetre.blit(text_step, dest=((left+B+10),(bottom-B)))
#--------------------------------------------------
def button(x, y, value):
    if value == "more":
        pygame.draw.rect(fenetre,(b_gray),((x),(y),B,B))
        pygame.draw.rect(fenetre,(white),((x+15),(y+5),10,30))
        pygame.draw.rect(fenetre,(white),((x+5),(y+15),30,10))

    elif value == "less":
        pygame.draw.rect(fenetre,(b_gray),((x),(y),B,B))
        pygame.draw.rect(fenetre,(white),((x+5),(y+15),30,10))

    elif value == "square":
        pygame.draw.rect(fenetre,(b_gray),((x),(y),B,B))
#--------------------------------------------------

cell_layer = []
calcul_layer = {}
cells = len(cell_layer)
gen = 0

offset = (0,0)
moving = False
drawing = False
erasing = False

px = 20

delay = 5 #per second
speed_size = text_size(f"{delay} gens/s")
chrono = time.time()
fps_chrono = time.time()
fps = 0
last_fps = ""

paused = True
#======================================================================

update()

while True :

    pos = pygame.mouse.get_pos()
    cell = ((pos[0]-offset[0])//px, (pos[1]-offset[1])//px)
    keys = pygame.key.get_pressed()
    #================================#
    for event in pygame.event.get(): #
        security()                   #
    #================================# 
        if event.type == VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            # left = 10
            right = WIDTH-10
            # top = 10
            bottom = HEIGHT-10
            update()
    #================================#


                #----------PAUSE/UNPAUSE
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused

                #----------RESET
        if paused:
            if event.type == KEYDOWN:
                if event.key == K_r:
                    cell_layer = []
                    gen = 0
                    update()

                #----------MOVEMENT
        if event.type == MOUSEBUTTONDOWN and event.button == 2:
            moving = True
            starting_pos = pos
            starting_offset = offset
        if event.type == MOUSEBUTTONUP and event.button == 2:
            moving = False

        if moving:
            offset = (starting_offset[0] + (pos[0] - starting_pos[0]), starting_offset[1] + (pos[1] - starting_pos[1]))
            # show_grid(cell_layer, px, offset)
            # draw_grid() #REALLY FUNNY
            update()

                #----------ZOOM
        if event.type == MOUSEWHEEL:
            if 1 <= (px + event.y) <= 100:
                if px + event.y*5 > 100:
                    pass
                elif px + event.y > 20:
                    px += event.y*5
                else:
                    px += event.y

                cell_pos = (cell[0]*px, cell[1]*px)
                offset = (pos[0]-cell_pos[0]-(px//2), pos[1]-cell_pos[1]-(px//2))
                update()

                #----------SPEED
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if (right-B) <= pos[0] <= (right) and (top) <= pos[1] <= (top+B):
                    if delay == "max":
                        pass
                    elif keys[K_LSHIFT] or keys[K_LCTRL]:
                        delay = "max"
                    elif delay < 100:
                        if delay != 1:
                            delay += 5
                        else:
                            delay += 4
                    else:
                        delay = "max"
                    
                elif (right-B) <= pos[0] <= (right) and (top+B+10) <= pos[1] <= (top+2*B+10):
                    if delay == "max":
                        delay = 100
                    elif delay > 1:
                        if delay != 5:
                            delay += -5
                        else:
                            delay += -4

                elif paused and (left) <= pos[0] <= (left+B) and (bottom-B) <= pos[1] <= (bottom):
                    new_gen()
                    update()

                #----------DRAW-CELLS
                else:
                    drawing = True
            elif event.button == 3:
                erasing = True

            if delay != "max":
                speed_size = text_size(f"{delay} gens/s")
            else:
                speed_size = text_size(f"{delay}")

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
            elif event.button == 3:
                erasing = False

                #----------MODIFY-CELLS
        if paused:
            if drawing and (not cell in cell_layer):
                cell_layer.append(cell)
            elif erasing and (cell in cell_layer):
                cell_layer.remove(cell)
            update()
    #======================================================================
    if not paused:

        if delay == "max":
            fenetre.fill(background)
            new_gen()
            gen += 1
            update()

        elif time.time() - chrono >= (1/delay): #"delay" times per seconde
            chrono = time.time()

            fenetre.fill(background)
            new_gen()
            gen += 1
            update()

    if time.time() - fps_chrono >= 1:
        fps_chrono = time.time()
        last_fps = str(fps)
        fps = 0
        update()
    fps += 1

    pygame.display.flip()