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
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
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
    
    def display(self):
        color = True
        for y in range(8):
            for x in range(8):
                if color:
                    pygame.draw.rect(fenetre, (0, 0, 0), (x*64, y*64, 64, 64))
                else:
                    pygame.draw.rect(fenetre, (255, 255, 255), (x*64, y*64, 64, 64))
                if self.board[y][x].piece:
                    fenetre.blit(font.render(self.board[y][x].piece.name, True, (127,127,127)), dest=(x*64, y*64))
                color = not color
            color = not color

#==================================================
class Case:
    def __init__(self, x:int, y:int, piece:"Piece"=None):
        self.x = x
        self.y = y
        self.piece = piece
    
#==================================================
class Piece:
    def __init__(self, board:"Board", x:int, y:int, color:bool, name:str="p"):
        self.board = board
        self.x = x
        self.y = y
        self.color = color # False = black, True = white
        self.name = name
        
#==================================================
class Pawn(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="p", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(0, 1), (0, 2)] # 1 or 2 cases forward
    def valid_move(self):
        valid = {}
        # for i in self.move:
        #     while 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
        #         if self.board.board[self.y + i[1]][self.x + i[0]].piece == None:
        #             valid[(self.x + i[0], self.y + i[1])] = True
        #         else:
        #             break
        if 0 <= self.x <= 7 and 0 <= self.y + 1 <= 7: # normal move
            if self.board.board[self.y + 1][self.x].piece == None:
                valid[(self.x, self.y + 1)] = True
        if 0 <= self.x <= 7 and 0 <= self.y + 2 <= 7 and not self.has_moved: # first move
            if self.board.board[self.y + 2][self.x].piece == None:
                valid[(self.x, self.y + 2)] = True
        for i in range(-1, 2, 2):
            if 0 <= self.x + i <= 7 and 0 <= self.y + 1 <= 7: # eat move
                if self.board.board[self.y + 1][self.x + i].piece and self.board.board[self.y + 1][self.x + i].piece.color != self.color:
                    valid[(self.x + i, self.y + 1)] = True

class Rook(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="r", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(0, 1), (1, 0), (0, -1), (-1, 0)] # each direction horizontaly and verticaly
    def valid_move(self):
        valid = {}
        for i in self.move:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                    break
                else:
                    break
                e += 1
        return valid

class Bishop(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="b"):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction diagonaly
    def valid_move(self):
        valid = {}
        for i in self.move:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                    break
                else:
                    break
                e += 1
        return valid

class Knight(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="n"):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)] # L pattern

class Queen(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="q"):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction (Rook + Bishop)
    def valid_move(self):
        valid = {}
        for i in self.move:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid[(self.x + i[0]*e, self.y + i[1]*e)] = True
                    break
                else:
                    break
                e += 1
        return valid

class King(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="k", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # Queen but bad
    def valid_move(self):
        valid = {}
        for i in self.move:
            if 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
                if self.board.board[self.y + i[1]][self.x + i[0]].piece == None:
                    valid[(self.x + i[0], self.y + i[1])] = True
                elif self.board.board[self.y + i[1]][self.x + i[0]].piece.color != self.color:
                    valid[(self.x + i[0], self.y + i[1])] = True
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
board = Board()
board.display()

while True :

    #================================#
    for event in pygame.event.get(): #
        security()                   #
    #================================# 
        if event.type == VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    #================================#
    fenetre.fill(background)
    board.display()
    pygame.display.flip()