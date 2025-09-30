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
                    fenetre.blit(font.render(self.board[y][x].piece.name, True, (127,127,127)), dest=(x*64, y*64))


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
    def __init__(self, board:"Board", x:int, y:int, color:bool, name:str="p"):
        self.board = board
        self.x = x
        self.y = y
        self.color = color # False = black, True = white
        self.name = name
        self.moves = []
        self.abc = "ABC"
    
    def update_moves(self):
        self.moves = self.valid_move()
        
#==================================================

class Pawn(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="p", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(0, 1), (0, 2)] # 1 or 2 cases forward
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        # for i in self.move_options:
        #     while 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
        #         if self.board.board[self.y + i[1]][self.x + i[0]].piece == None:
        #             valid[(self.x + i[0], self.y + i[1])] = True
        #         else:
        #             break
        if 0 <= self.x <= 7 and 0 <= self.y + 1 <= 7: # normal move
            if self.board.board[self.y + 1][self.x].piece == None:
                valid.append((self.x, self.y + 1))
        if 0 <= self.x <= 7 and 0 <= self.y + 2 <= 7 and not self.has_moved: # first move
            if self.board.board[self.y + 2][self.x].piece == None:
                valid.append((self.x, self.y + 2))
        for i in range(-1, 2, 2):
            if 0 <= self.x + i <= 7 and 0 <= self.y + 1 <= 7: # eat move
                if self.board.board[self.y + 1][self.x + i].piece and self.board.board[self.y + 1][self.x + i].piece.color != self.color:
                    valid.append((self.x + i, self.y + 1))
        return valid #RETURN VALID YOU PLONKER !!!!!

class Rook(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="r", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0)] # each direction horizontaly and verticaly
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class Bishop(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="b"):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction diagonaly
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class Knight(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="n"):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)] # L pattern
    def valid_move(self):
        valid = []
        for i in self.move_options:
            if 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
                if self.board.board[self.y + i[1]][self.x + i[0]].piece == None:
                    valid.append((self.x + i[0], self.y + i[1]))
                elif self.board.board[self.y + i[1]][self.x + i[0]].piece.color != self.color:
                    valid.append((self.x + i[0], self.y + i[1]))
        return valid

class Queen(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="q"):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # each direction (Rook + Bishop)
    def valid_move(self):
        valid = []
        for i in self.move_options:
            e = 1
            while 0 <= self.x + i[0]*e <= 7 and 0 <= self.y + i[1]*e <= 7:
                if self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece == None:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                elif self.board.board[self.y + i[1]*e][self.x + i[0]*e].piece.color != self.color:
                    valid.append((self.x + i[0]*e, self.y + i[1]*e))
                    break
                else:
                    break
                e += 1
        return valid

class King(Piece):
    def __init__(self, board:"Board", x:int=0, y:int=0, color:bool=False, name:str="k", has_moved:bool=False):
        Piece.__init__(self, board, x, y, color, name)
        self.move_options = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)] # Queen but bad
        self.has_moved = has_moved
    def valid_move(self):
        valid = []
        for i in self.move_options:
            if 0 <= self.x + i[0] <= 7 and 0 <= self.y + i[1] <= 7:
                if self.board.board[self.y + i[1]][self.x + i[0]].piece == None:
                    valid.append((self.x + i[0], self.y + i[1]))
                elif self.board.board[self.y + i[1]][self.x + i[0]].piece.color != self.color:
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
board = Board()
board.display_board()
board.display_pieces()

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
                selected_piece = board.board[case_pos[1]][case_pos[0]].piece
                board.update_pieces()


    fenetre.fill(background)
    board.display_board()

    if selected_piece:
        for i in selected_piece.moves:
            print(i)
            pygame.draw.rect(fenetre, (255, 0, 0), (i[0]*64, i[1]*64, 64, 64))
    
    board.display_pieces()

    pygame.display.flip()