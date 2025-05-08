import pygame, sys
from pygame.locals import *
import time

pygame.init()

WIDTH = 738 #738
HEIGHT = 512 #512
B = 40
C = 9
left = 10
right = WIDTH-10
top = 10
bottom = HEIGHT-10

fenetre = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font(pygame.font.get_default_font(), 36)
FPS = 60

background = (30,33,41)
white = (255,255,255)
b_gray = (93,95,103)
t_gray = (190,193,198)

fenetre.fill(background)

pygame.display.flip()

#--------------------------------------------------
def calcul(grid):
    new = []
    line = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            nb_cells = 0
            for i in range(-1, 2):
                for e in range(-1, 2):
                    if y+i != y or x+e != x:
                        
                        if y+i < len(grid) and x+e < len(grid[y]):
                            if grid[y+i][x+e] == "█":
                                nb_cells += 1

                        elif y+i >= len(grid):
                            if x+e >= len(grid[y]):
                                if grid[0][0] == "█":
                                    nb_cells += 1
                                    
                            elif grid[0][x+e] == "█":
                                nb_cells += 1
                                
                        elif x+e >= len(grid[y]):
                            if grid[y+i][0] == "█":
                                    nb_cells += 1
                                
            line.append(nb_cells)
        new.append(line)
        line = []
    return new
#--------------------------------------------------
def execute(grid, grid_tmp):
    new = []
    line = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "█":
                if 2 <= grid_tmp[y][x] <= 3:
                    line.append("█")
                else:
                    line.append(" ")
            else:
                if grid_tmp[y][x] == 3:
                    line.append("█")
                else:
                    line.append(" ")
        new.append(line)
        line = []
    return new
#--------------------------------------------------
def counter(grid):
    cells_count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "█":
                cells_count += 1
    return cells_count
#--------------------------------------------------
def show(grid):
    xg = len(grid[0])*(C+1)/2
    yg = len(grid)*(C+1)/2
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(fenetre,(14,15,19),((WIDTH/2)+(x*(C+1))-xg,(HEIGHT/2)+(y*(C+1))-yg,C,C))
            if grid[y][x] == "█":
                pygame.draw.rect(fenetre,(0,184,212),((WIDTH/2)+(x*(C+1))-xg,(HEIGHT/2)+(y*(C+1))-yg,C,C))
#--------------------------------------------------
def ui(gen, cells, game, mode, delay):
    text_gen = font.render(f"Gen {gen}", True, (t_gray))
    text_cells = font.render(f"Cells {cells}", True, (t_gray))
    text_button = font.render(f"{game}", True, (t_gray))
    fenetre.blit(text_gen, dest=(left,top))
    fenetre.blit(text_cells, dest=(left,top+B))
    fenetre.blit(text_button, dest=(20+B,bottom-B))
    play_button(game)
    step_button()
    extend_button(game, mode)
    speed_button(delay)
    size_button(C)
    clear_button()
#--------------------------------------------------
def play_button(game):
    button(left, bottom-B, "square")
    if game == "paused":
        pygame.draw.polygon(fenetre,(white),[(20,HEIGHT-45),(40,HEIGHT-30),(20,HEIGHT-15)],width=0)
    elif game == "playing":
        pygame.draw.rect(fenetre,(white),((left+5),(bottom-B+5),10,30))
        pygame.draw.rect(fenetre,(white),((left+25),(bottom-B+5),10,30))
#--------------------------------------------------
def step_button():
    if game == "paused":
        
        button(left+200, bottom-B, "square")
        pygame.draw.polygon(fenetre,(white),[(25+200,HEIGHT-40),(35+200,HEIGHT-30),(25+200,HEIGHT-20)],width=0)
        
        text_step = font.render("step", True, (t_gray))
        fenetre.blit(text_step, dest=((left+200+B+10),(bottom-B)))
#--------------------------------------------------
def extend_button(game, mode):
    if game == "paused":

        button(right-B, bottom-B-50, "more")
        button(right-B, bottom-B, "less")

        button(right-B-50, bottom-B, "square")
        text_mode = font.render(f"{mode}", True, (white))#white
        fenetre.blit(text_mode, dest=((right-B-50+8),(bottom-B+4)))
#--------------------------------------------------
def speed_button(delay):

    button(right-B, top, "more")
    button(right-B, top+B+10, "less")

    text_speed = font.render(f"{round(delay)} gen/s", True, (t_gray))
    fenetre.blit(text_speed, dest=((right-205),(top+5)))
#--------------------------------------------------
def size_button(px):

    button(left, (HEIGHT/2)-B-5, "more")
    button(left, (HEIGHT/2)+5, "less")

    text_size = font.render(f"{px} px", True, (t_gray))
    fenetre.blit(text_size, dest=((left),(HEIGHT/2)-B-36-15))
#--------------------------------------------------
def clear_button():
    if game == "paused":
        pygame.draw.rect(fenetre,(b_gray),((WIDTH/2)-(B*3/2),(top),B*3,B))

        text_clear = font.render(f"clear", True, (white))
        fenetre.blit(text_clear, dest=((WIDTH/2)-(B*3/2)+(12), top+4))
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
def new_grid(nb_x, nb_y):
    line = []
    new = []
    for y in range(nb_y):
        for x in range(nb_x):
            line.append(" ")
        new.append(line)
        line = []
    return new
#--------------------------------------------------
def extend(grid, value, mode):
    xL = len(grid[0])
    yL = len(grid)
    new = []
    line = []
    
    if mode == "X":
        if value == 1:
            for y in range(yL):
                for x in range(xL):
                    if grid[y][x] == " ":
                        line.append(" ")
                    else:
                        line.append("█")
                line.append(" ")
                new.append(line)
                line = []

        else:
            for y in range(yL):
                for x in range(xL-1):
                    if grid[y][x] == " ":
                        line.append(" ")
                    else:
                        line.append("█")
                new.append(line)
                line = []

    if mode == "Y":
        if value == 1:
            for i in range(xL):
                line.append(" ")
            new.append(line)
            line = []
            for y in range(yL):
                for x in range(xL):
                    if grid[y][x] == " ":
                        line.append(" ")
                    else:
                        line.append("█")
                new.append(line)
                line = []

        else:
            for y in range(1, yL):
                for x in range(xL):
                    if grid[y][x] == " ":
                        line.append(" ")
                    else:
                        line.append("█")
                new.append(line)
                line = []

    return new
#--------------------------------------------------
def move(grid, direction):
    xL = len(grid[0])
    yL = len(grid)
    new = []
    line = []
    if direction == "UP":
        for y in range(1, yL):
            for x in range(xL):
                if grid[y][x] == " ":
                    line.append(" ")
                else:
                    line.append("█")
            new.append(line)
            line = []
        for i in range(xL):
            line.append(" ")
        new.append(line)
        line = []

    if direction == "DOWN":
        for i in range(xL):
            line.append(" ")
        new.append(line)
        line = []
        for y in range(yL-1):
            for x in range(xL):
                if grid[y][x] == " ":
                    line.append(" ")
                else:
                    line.append("█")
            new.append(line)
            line = []

    if direction == "LEFT":
        for y in range(yL):
            for x in range(1, xL):
                if grid[y][x] == " ":
                    line.append(" ")
                else:
                    line.append("█")
            line.append(" ")
            new.append(line)
            line = []

    if direction == "RIGHT":
        for y in range(yL):
            line.append(" ")
            for x in range(xL-1):
                if grid[y][x] == " ":
                    line.append(" ")
                else:
                    line.append("█")
            new.append(line)
            line = []

    return new  
#//////////////////////////////////////////////////////////////////////

x_size = 40
y_size = 20
grid = new_grid(x_size, y_size)

grip_tmp = [] #transitional grid

gen = 0
cells = counter(grid)
game = "paused"
mode = "X"

delay = 5
chrono = time.time()
#======================================================================
pause = True
play = False

while True :

    while play :
    
    #====================================#
        for event in pygame.event.get(): #
            if event.type == pygame.QUIT:#
                pygame.display.quit()    #
                sys.exit()               #
    #====================================#
                                         #
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                mouse_co = pygame.mouse.get_pos()
                
                #----------PAUSE/PLAY
                if (left) <= mouse_co[0] <= (left+B) and (bottom-B) <= mouse_co[1] <= (bottom):
                    game = "paused"
                    pause, play = True, False
                #----------SPEED
                elif (right-B) <= mouse_co[0] <= (right) and (top) <= mouse_co[1] <= (top+B):
                    if delay < 50:
                        if delay != 1:
                            delay += 5
                        else:
                            delay += 4
                elif (right-B) <= mouse_co[0] <= (right) and (top+B+10) <= mouse_co[1] <= (top+2*B+10):
                    if delay > 1:
                        if delay != 5:
                            delay += -5
                        else:
                            delay += -4
                #----------SIZE
                elif (left) <= mouse_co[0] <= (left+B) and (HEIGHT/2-B-5) <= mouse_co[1] <= (HEIGHT/2-5):
                    if C < 20:
                        C += 1
                elif (left) <= mouse_co[0] <= (left+B) and (HEIGHT/2+5) <= mouse_co[1] <= (HEIGHT/2+B+5):
                    if C > 9:
                        C += -1
            #[][][][][][][][][][]PAUSE/PLAY
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game = "paused"
                    pause, play = True, False
                                         #    
    #====================================#
        fenetre.fill(background)
        show(grid)
        #-------------------------
        if time.time() - chrono >= (1/delay): #"delay" times per seconde
            chrono = time.time()
    
            grid_tmp = calcul(grid)
            grid = execute(grid, grid_tmp)
            grid_tmp = []
    
            gen += 1
            cells = counter(grid)
        #-------------------------
        ui(gen, cells, game, mode, delay)
        pygame.display.flip()#DISPLAY
    #======================================================================
    while pause :
    
    #====================================#
        for event in pygame.event.get(): #
            if event.type == pygame.QUIT:#
                pygame.display.quit()    #
                sys.exit()               #
    #====================================#
                                         #
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                mouse_co = pygame.mouse.get_pos()
                x_click = int((mouse_co[0]-(WIDTH/2-len(grid[0])*(C+1)/2))//(C+1))
                y_click = int((mouse_co[1]-(HEIGHT/2-len(grid)*(C+1)/2))//(C+1))

                #----------PAUSE/PLAY
                if (left) <= mouse_co[0] <= (left+B) and (bottom-B) <= mouse_co[1] <= (bottom):
                    game = "playing"
                    pause, play = False, True
                #----------STEP
                if (left+200) <= mouse_co[0] <= (left+200+B) and (bottom-B) <= mouse_co[1] <= (bottom):

                    grid_tmp = calcul(grid)
                    grid = execute(grid, grid_tmp)
                    grid_tmp = []
    
                    gen += 1
                    cells = counter(grid)
                #----------SPEED
                elif (right-B) <= mouse_co[0] <= (right) and (top) <= mouse_co[1] <= (top+B):
                    if delay < 50:
                        if delay != 1:
                            delay += 5
                        else:
                            delay += 4
                elif (right-B) <= mouse_co[0] <= (right) and (top+B+10) <= mouse_co[1] <= (top+2*B+10):
                    if delay > 1:
                        if delay != 5:
                            delay += -5
                        else:
                            delay += -4
                #----------SWITCH MODE
                elif (right-2*B-10) <= mouse_co[0] < (right-B-10) and (bottom-B) <= mouse_co[1] < (bottom):
                    if mode == "X":
                        mode = "Y"
                    else:
                        mode = "X"
                #----------EXTEND/INPEND
                elif (right-B) <= mouse_co[0] < (right) and (bottom-B) <= mouse_co[1] < (bottom):
                    if mode == "X" and len(grid[0]) > 1:
                        grid = extend(grid, -1, mode)
                        x_size += -1
                    elif mode == "Y" and len(grid) > 1:
                        grid = extend(grid, -1, mode)
                        y_size += -1
                elif (right-B) <= mouse_co[0] < (right) and (bottom-2*B-10) <= mouse_co[1] < (bottom-B-10):
                    grid = extend(grid, 1, mode)
                    if mode == "X":
                        x_size += 1
                    elif mode == "Y":
                        y_size += 1
                #----------SIZE
                elif (left) <= mouse_co[0] <= (left+B) and (HEIGHT/2-B-5) <= mouse_co[1] <= (HEIGHT/2-5):
                    if C < 20:
                        C += 1
                elif (left) <= mouse_co[0] <= (left+B) and (HEIGHT/2+5) <= mouse_co[1] <= (HEIGHT/2+B+5):
                    if C > 9:
                        C += -1
                #----------CLEAR
                elif (WIDTH/2-B*3/2) <= mouse_co[0] <= (WIDTH/2-B*3/2)+(B*3) and (top) <= mouse_co[1] <= (top+B):
                    grid = new_grid(x_size, y_size)
                #----------ADD/REMOVE CELLS
                elif 0 <= x_click < len(grid[0]) and 0 <= y_click < len(grid):
                    if grid[y_click][x_click] == " ":
                        grid[y_click][x_click] = "█"
                    else:
                        grid[y_click][x_click] = " "
            #[][][][][][][][][][]PAUSE/PLAY
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game = "playing"
                    pause, play = False, True

                if event.key == K_UP or event.key == K_z:
                    grid = move(grid, "UP")
                if event.key == K_DOWN or event.key == K_s:
                    grid = move(grid, "DOWN")
                if event.key == K_LEFT or event.key == K_q:
                    grid = move(grid, "LEFT")
                if event.key == K_RIGHT or event.key == K_d:
                    grid = move(grid, "RIGHT")
                                         #
    #====================================#
        fenetre.fill(background)
        show(grid)

        ui(gen, cells, game, mode, delay)
        pygame.display.flip()#DISPLAY
#======================================================================
pygame.display.quit()#
sys.exit()           #
#====================#
