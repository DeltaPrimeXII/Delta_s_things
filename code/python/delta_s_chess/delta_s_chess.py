#Delta's Chess

import pygame, sys
from pygame.locals import *
import time

pygame.init()

WIDTH = 738
HEIGHT = 512

fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Delta's Chess")

font = pygame.font.Font(pygame.font.get_default_font(), 36)

background = (14,15,19)

fenetre.fill(background)
pygame.display.flip()


#==================================================

class Board:
    default_board = [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [" "," "," "," "," "," "," "," "],
        [" ","n"," ","q"," ","p"," "," "],
        ["r"," "," "," "," "," ","b"," "],
        [" "," "," "," ","k"," "," "," "],
        ["p","p","p","p","p","p","p","p"],
        ["r","n","b","q","k","b","n","r"]
    ]
    def __init__(self):
        board = []
        line = []
        for y in range(8):
            for x in range(8):
                if Board.default_board[y][x] != " ":
                    line.append(Case(x, y, piece_name[Board.default_board[y][x]](self, x, y, y > 3, Board.default_board[y][x]))) #This line is way too long
                else:
                    line.append(Case(x, y))
            board.append(line)
            line = []
        self.board = board
    
    def display_board(self):
        color = True
        for y in range(8):
            for x in range(8):
                if color:
                    pygame.draw.rect(fenetre, (0, 0, 0), (x*64, y*64, 64, 64))
                else:
                    pygame.draw.rect(fenetre, (255, 255, 255), (x*64, y*64, 64, 64))
                color = not color
            color = not color
    
    def display_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.board[y][x].piece:
                    if self.board[y][x].piece.color:
                        fenetre.blit(font.render(self.board[y][x].piece.name, True, (255,127,100)), dest=(x*64, y*64))
                    else:
                        fenetre.blit(font.render(self.board[y][x].piece.name, True, (100,127,255)), dest=(x*64, y*64))


    def update_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.board[y][x].piece:#I should not copy paste too much :P
                    self.board[y][x].piece.update_moves()


#==================================================

class Case:
    def __init__(self, x:int, y:int, piece:"Piece"=None):
        self.x = x
        self.y = y
        self.piece = piece
    
#==================================================

class Piece:
    def __init__(self, game:"Board", x:int, y:int, color:bool, name:str="p"):
        self.game = game
        self.x = x
        self.y = y
        self.color = color # False = black, True = white
        self.name = name
        self.moves = []
        self.abc = "ABC"
    
    def update_moves(self):
        self.moves = self.valid_move()
    
    def move(self, x, y):
        last_pos = (self.x, self.y)
        self.game.board[y][x].piece = self
        self.game.board[last_pos[1]][last_pos[0]].piece = None
        self.x, self.y = x, y
        
#==================================================

class Pawn(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="p", has_moved:bool=False):
        Piece.__init__(self, game, x, y, color, name)
        if color:
            self.move_options = [(0, -1), (0, -2)] # 1 or 2 cases forward (White)
        else: #NEVER USED :skull:
            self.move_options = [(0, 1), (0, 2)] # 1 or 2 cases forward (Black)
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        if self.color:
            c = -1
        else:
            c = 1
        # for i in self.move_options:
        #     while 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
        #         if self.game.board[self.y + i[1]][self.x + i[0]].piece == None:
        #             valid[(self.x + i[0], self.y + i[1])] = True
        #         else:
        #             break
        if 0 <= self.x <= 7 and 0 <= self.y + c <= 7: # normal move (1 case)
            if self.game.board[self.y + c][self.x].piece == None:
                valid.append((self.x, self.y + c))
                # first move (2 cases)
                if 0 <= self.x <= 7 and 0 <= self.y + c*2 <= 7 and not self.has_moved:
                    if self.game.board[self.y + c*2][self.x].piece == None:
                        valid.append((self.x, self.y + c*2))
        for i in range(-1, 2, 2):
            if 0 <= self.x + i <= 7 and 0 <= self.y + c <= 7: # eat move
                if self.game.board[self.y + c][self.x + i].piece and self.game.board[self.y + c][self.x + i].piece.color != self.color:
                    valid.append((self.x + i, self.y + c))
        return valid #RETURN VALID YOU PLONKER !!!!!

class Rook(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="r", has_moved:bool=False):
        Piece.__init__(self, game, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0)] # each direction horizontaly and verticaly
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class Bishop(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="b"):
        Piece.__init__(self, game, x, y, color, name)
        self.move_options = [(1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction diagonaly
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class Knight(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="n"):
        Piece.__init__(self, game, x, y, color, name)
        self.move_options = [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)] # L pattern
    def valid_move(self):
        valid = []
        for i in self.move_options:
            if 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
                if self.game.board[self.y + i[1]][self.x + i[0]].piece == None:
                    valid.append((self.x + i[0], self.y + i[1]))
                elif self.game.board[self.y + i[1]][self.x + i[0]].piece.color != self.color:
                    valid.append((self.x + i[0], self.y + i[1]))
        return valid

class Queen(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="q"):
        Piece.__init__(self, game, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction (Rook + Bishop)
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.game.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class King(Piece):
    def __init__(self, game:"Board", x:int=0, y:int=0, color:bool=False, name:str="k", has_moved:bool=False):
        Piece.__init__(self, game, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # Queen but bad
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        for i in self.move_options:
            if 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
                if self.game.board[self.y + i[1]][self.x + i[0]].piece == None:
                    valid.append((self.x + i[0], self.y + i[1]))
                elif self.game.board[self.y + i[1]][self.x + i[0]].piece.color != self.color:
                    valid.append((self.x + i[0], self.y + i[1]))
        return valid

#==================================================
piece_name = {
    "p": Pawn,
    "r": Rook,
    "b": Bishop,
    "n": Knight,
    "q": Queen,
    "k": King
}
#--------------------------------------------------
def security():
    if event.type == pygame.QUIT:
        pygame.display.quit()
        sys.exit()
#--------------------------------------------------

#--------------------------------------------------

#--------------------------------------------------

#--------------------------------------------------
game = Board()
game.display_board()
game.display_pieces()

selected_piece = None

while True :

    pos = pygame.mouse.get_pos()
    case_pos = ((pos[0])//64, (pos[1])//64)
    #================================#
    for event in pygame.event.get(): #
        security()                   #
    #================================# 
        if event.type == VIDEORESIZE:#
            WIDTH, HEIGHT = event.w, event.h
            fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    #================================#

        if event.type == MOUSEBUTTONDOWN:
            if 0 <= case_pos[0] <= 7 and 0 <= case_pos[1] <= 7:
                if selected_piece == game.board[case_pos[1]][case_pos[0]].piece:
                    selected_piece = None
                elif (selected_piece) and (case_pos in selected_piece.valid_move()):
                    selected_piece.move(case_pos[0], case_pos[1])
                else:
                    selected_piece = game.board[case_pos[1]][case_pos[0]].piece
                game.update_pieces()


    fenetre.fill(background)
    game.display_board()

    if selected_piece:
        # print(selected_piece.move_options)
        for i in selected_piece.moves:
            # print(i)
            pygame.draw.rect(fenetre, (0, 200, 100), (i[0]*64, i[1]*64, 64, 64))
    
    game.display_pieces()

    pygame.display.flip()