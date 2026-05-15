#Delta's Chess

import pyglet

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

#==================================================
way = {
    0: 1,
    1: -1,
    }
#==================================================

class Coord:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    #---------------
    def __repr__(self):
        return f"Coord({self.x}, {self.y})"
    #---------------
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    #---------------
    def __add__(self, adder) -> "Coord":
        if type(adder) == tuple:
            return Coord(self.x + adder[0], self.y + adder[1])
        else:
            return Coord(self.x + adder.x, self.y + adder.y)
    #---------------    
    def __sub__(self, subber:tuple) -> "Coord":
        return Coord(self.x - subber[0], self.y - subber[1])
    #---------------
    def __mul__(self, factor) -> "Coord":
        if type(factor) == int or type(factor) == float:
            return Coord(self.x * factor, self.y * factor)
        elif type(factor) == tuple:
            return Coord(self.x * factor[0], self.y * factor[1])
        else:
            return Coord(self.x * factor.x, self.y * factor.y)

#==================================================

class Piece:

    def __init__(self, board:"Board", name:str, x=0, y=0, color= 0):# 0 == "white" and 1 == "black"
        self.board = board
        self.name = name
        self.pos = Coord(x, y)
        self.color = color
        self.moves = []
        self.controlled_squares = []
    #---------------
    def __repr__(self):
        return f"{'w' if self.color == 0 else 'b'}_{self.name}"
    #---------------
    def can_move(self, coord) -> bool:
            x, y = coord.x, coord.y
            if in_bound(x, y):# (in_bound)
                self.controlled_squares.append(coord)
                if self.board[x][y] is None:# (empty_case)
                    self.moves.append(coord)
                    return True
                elif self.board[x][y].color != self.color:
                    self.moves.append(coord)
                    return False
            return False
    #---------------
    def move(self, coord:"Coord"):
        x, y = coord.x, coord.y
        if self.board[x][y]:
            self.board.team_list[self.board[x][y].color].remove(self.board[x][y])
        self.board[x][y] = self
        self.board[self.pos.x][self.pos.y] = None
        self.pos = coord
        if hasattr(self, "has_moved"):
            self.has_moved = True
    #---------------
    def remove_illegal_moves(self):
        king = self.board.kings[self.color]
        if king.is_checked:

            for pin in king.pinned_pieces:
                if self == pin[0]:
                    possible = []
                    for m in self.moves:
                        if m in pin[1]:
                            possible.append(m)
                    self.moves = possible

            if king.attacking_piece:
                possible = []
                for m in self.moves:
                    if m in king.attacking_piece[1]:
                        possible.append(m)
                self.moves = possible

#--------------------------------------------------

class Pawn(Piece):

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "pawn", x, y, color)
        self.has_moved = False
    #---------------
    def move(self, coord:"Coord"):
        x, y = coord.x, coord.y

        if self.pos.x == x:
            if self.pos.y + 2*way[self.color] == y:
                self.board.en_passant = [coord - (0, (way[self.color]))]

        else:
            if self.board[x][y]:
                self.board.team_list[self.board[x][y].color].remove(self.board[x][y])
            else:
                self.board.team_list[self.board[x][y-way[self.color]].color].remove(self.board[x][y-way[self.color]])

        self.board[x][y] = self
        self.board[self.pos.x][self.pos.y] = None
        self.pos = coord
        self.has_moved = True
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        direction = (way[self.color])
        
        x, y = self.pos.x, self.pos.y + direction
        if in_bound(x, y) and self.board[x][y] is None:# 1 square
            self.moves.append(Coord(x, y))
            if (in_bound(x, y + direction)) and (not self.has_moved) and self.board[x][y + direction] is None:# 2 squares
                self.moves.append(Coord(x, y + direction))

        for i in range(-1, 2, 2):# diagonal attacks
            x, y = self.pos.x + i, self.pos.y + direction
            if in_bound(x, y):
                self.controlled_squares.append(Coord(x, y))
                if (self.board[x][y] and self.board[x][y].color != self.color) or Coord(x, y) in self.board.en_passant:
                    self.moves.append(Coord(x, y))

#--------------------------------------------------

class Knight(Piece):

    move_options = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                    (2, 1), (-2, 1), (2, -1), (-2, -1),]

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "knight", x, y, color)
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        for m in Knight.move_options:
            self.can_move(self.pos + m)

#--------------------------------------------------

class Bishop(Piece):

    move_options = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "bishop", x, y, color)
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        for m in Bishop.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m[0]*i, m[1]*i)
                if not self.can_move(target_pos):
                    break
                i += 1

#--------------------------------------------------

class Rook(Piece):

    move_options = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "rook", x, y, color)
        self.has_moved = False
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        for m in Rook.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m[0]*i, m[1]*i)
                if not self.can_move(target_pos):
                    break
                i += 1

#--------------------------------------------------

class Queen(Piece):

    move_options = Bishop.move_options + Rook.move_options

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "queen", x, y, color)
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        for m in Queen.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m[0]*i, m[1]*i)
                if not self.can_move(target_pos):
                    break
                i += 1

#--------------------------------------------------
# TODO fix pinned piece (exemple avec le fou)
# TODO fix knight check (can't eat the knight)
class King(Piece):

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "king", x, y, color)
        self.has_moved = False
        self.is_checked = 0 #number of pieces checking the king
        self.impossible_moves = []
        self.pinned_pieces = [] #[(piece, line), ...]
        self.attacking_piece = () #(piece, line)
    #---------------
    def move(self, coord:"Coord"):
        x, y = coord.x, coord.y

        if self.pos.y == y and abs(self.pos.x - x) >= 2:
            match x:
                case 2:
                    self.board[3][self.pos.y], self.board[0][self.pos.y] = self.board[0][self.pos.y], None
                    self.board[3][self.pos.y].pos = Coord(3, self.pos.y)
                case 6:
                    self.board[5][self.pos.y], self.board[7][self.pos.y] = self.board[7][self.pos.y], None
                    self.board[5][self.pos.y].pos = Coord(5, self.pos.y)

        elif self.board[x][y]:
            self.board.team_list[self.board[x][y].color].remove(self.board[x][y])

        self.board[x][y] = self
        self.board[self.pos.x][self.pos.y] = None
        self.pos = coord
        self.has_moved = True
    #---------------
    def set_all_moves(self) -> None:
        self.moves = []
        self.controlled_squares = []
        for m in Queen.move_options:
            self.can_move(self.pos + m)
        
        #Castle
        if not self.has_moved:
            for i in range(-1, 2, 2):
                line = self.get_line(Coord(i, 0))
                piece = self.board[line[-1].x][line[-1].y]
                if type(piece) is Rook and (piece.color == self.color) and (not piece.has_moved):
                    if [self.board[c.x][c.y] for c in line[0:-1]] == [None]*(len(line)-1):

                        opponents = self.board.team_list[1 - self.color]
                        controlled_squares = []
                        for p in opponents:
                            controlled_squares += p.controlled_squares

                        castle = True
                        for e in range(0, 3):#including king itself
                            if Coord(self.pos.x + i*e, self.pos.y) in controlled_squares:
                                castle = False
                        
                        if castle:
                            self.moves.append(Coord(self.pos.x + i*2, self.pos.y))
    #---------------
    def get_line(self, dir:"Coord") -> list:#TODO repair get_line() + its usage in detect_c_a_p()
        line = []
        for i in range(1, 8):
            x, y = self.pos.x + dir.x*i, self.pos.y + dir.y*i
            if in_bound(x, y):
                if self.board[x][y] and self.board[x][y].color != self.color:
                    line.append(Coord(x, y))
                    break
                line.append(Coord(x, y))
        return line
    #---------------
    def detect_check_and_pins(self):
        self.is_checked = 0
        self.pinned_pieces = []
        self.impossible_moves = []

        for m in Knight.move_options:
            x, y = self.pos.x + m[0], self.pos.y + m[1]
            if in_bound(x, y) and self.board[x][y] and self.board[x][y].color != self.color and type(self.board[x][y]) is Knight:
                self.is_checked += 1
                attacking = (self.board[x][y], [])

        for m in Bishop.move_options:
            line = self.get_line(Coord(m[0], m[1]))
            if line:
                last = self.board[line[-1].x][line[-1].y]
                if last and last.color != self.color and (type(last) is Bishop or type(last) is Queen):
                    count = 0
                    for pos in line:
                        if self.board[pos.x][pos.y] and self.board[pos.x][pos.y].color == self.color:
                            count += 1
                            pinned = self.board[pos.x][pos.y]
                    if count == 0:
                        self.is_checked += 1
                        attacking = (last, line)
                        self.impossible_moves.append(self.pos + Coord(m[0], m[1])*-1)
                    elif count == 1:
                        self.pinned_pieces.append((pinned, line))

        for m in Rook.move_options:
            line = self.get_line(Coord(m[0], m[1]))
            if line:
                last = self.board[line[-1].x][line[-1].y]
                if last and last.color != self.color and (type(last) is Rook or type(last) is Queen):
                    count = 0
                    for pos in line:
                        if self.board[pos.x][pos.y] and self.board[pos.x][pos.y].color == self.color:
                            count += 1
                            pinned = self.board[pos.x][pos.y]
                    if count == 0:
                        self.is_checked += 1
                        attacking = (last, line)
                        self.impossible_moves.append(self.pos + Coord(m[0], m[1])*-1)
                    elif count == 1:
                        self.pinned_pieces.append((pinned, line))
        
        for i in range(-1, 2, 2):
            x, y = self.pos.x + i, self.pos.y + (way[self.color])
            if in_bound(x, y) and self.board[x][y]:
                if self.board[x][y].color != self.color and type(self.board[x][y]) == Pawn:
                    self.is_checked += 1
                    attacking = (self.board[x][y], [])
        
        if self.is_checked == 1:
            self.attacking_piece = attacking

    #---------------
    def remove_illegal_moves(self):

        opponents = self.board.team_list[1 - self.color]
        controlled_squares = []

        for p in opponents:
            controlled_squares += p.controlled_squares

        possible = []
        for m in self.moves:
            if not m in controlled_squares and not m in self.impossible_moves:
                possible.append(m)
        self.moves = possible

#--------------------------------------------------

class Board:

    default_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self, player=0):
        self.player = player
        self.turn_played = False #For multiplayer purpose
        self.case = [[None]*8 for _ in range(8)]
        self.team_list = [[], []]
        self.kings = []
        self.turn = 0
        self.selected_piece = None
        self.en_passant = []

        for x in range(8):
            for y in range(8):
                if y <= 1 or y >= 6:

                    if y == 1 or y == 6:
                        self.case[x][y] = Pawn(self, x, y, 0 if y < 4 else 1)
                    else:
                        self.case[x][y] = Board.default_pieces[x](self, x, y, 0 if y < 4 else 1)
                        if type(self.case[x][y]) == King:
                            self.kings.append(self.case[x][y])

                    if y < 4:
                        self.team_list[0].append(self.case[x][y])
                    else:
                        self.team_list[1].append(self.case[x][y])
        self.update_pieces()
    #---------------
    def update_pieces(self):
        for t in self.team_list:
            for p in t:
                if not type(p) is King:
                    p.set_all_moves()
        
        for k in self.kings:
            k.set_all_moves()
            k.detect_check_and_pins()
        
        for t in self.team_list:
            for p in t:
                p.remove_illegal_moves()
    #---------------
    #Called for each mouse click
    def clicked(self, x, y):
        side = 0
        if self.player == 1:
            side = 7
        ax, ay = abs(side - int(x/64)), abs(side - int(y/64))
        piece = self.selected_piece
        if in_bound(ax, ay):
            if self[ax][ay] == piece:
                self.selected_piece = None
            elif piece and Coord(ax, ay) in piece.moves:
                self.play(piece, Coord(ax, ay))
                self.selected_piece = None
            elif self[ax][ay] and is_piece_turn(self[ax][ay], self.turn):
                self.selected_piece = self[ax][ay]
            else:
                self.selected_piece = None
        else:
            self.selected_piece = None
    #---------------
    def play(self, piece:"Piece", coord:"Coord"):
        # if is_piece_turn(piece, self.turn):
        if piece.color == self.player:
            self.en_passant = []
            piece.move(coord)
            self.turn += 1
            self.update_pieces()
            self.turn_played = True
    #---------------
    def __repr__(self):
        for x in range(7, -1, -1):
            for y in range(8):
                print(self.case[y][x], end=" ")
            print("")
        print(self.team_list)
        return ""
    #---------------
    def __getitem__(self, key):
        return self.case[key]
    #---------------
    def __len__(self):
        return len(self.case)
    #---------------
    def render(self):
        render_board(self)
        render_moves(self, self.player)    
        render_pieces(self, self.player)

#==================================================

def render_board(board:"Board"):
    color = ((0,0,0,0), (245, 245, 245, 255), (10, 10, 10, 255))
    e = 1
    i = 1
    for x in range(len(board)):
        for y in range(len(board[0])):
            pyglet.shapes.Rectangle(x=x*64, y=y*64, width=64, height=64, color=color[i]).draw()
            i = -i
        e = -e
        i = e
    pyglet.shapes.Rectangle(x=8*64 + 8, y=0, width=16, height=64*8, color=color[1 if board.turn%2 == 0 else -1]).draw()
#---------------
def render_pieces(board:"Board", player):
    side = 0
    if player == 1:
        side = 7
    for t in board.team_list:
        for p in t:
            a = pyglet.sprite.Sprite(img=pyglet.image.load(f'{dir_path}/textures/{p.name}{"_b" if p.color == 1 else ""}.png'),
                                     x=abs(side - p.pos.x)*64, y=abs(side - p.pos.y)*64)
            a.scale = 4
            a.draw()
#---------------
def render_moves(board:"Board", player):
    if board.selected_piece:
        side = 0
        if player == 1:
            side = 7
        for m in board.selected_piece.moves:
            pyglet.shapes.Rectangle(x=abs(side - m.x)*64 + 8, y=abs(side - m.y)*64 + 8, width=48, height=48, color=(100, 255, 100, 255)).draw()
        for m in board.selected_piece.controlled_squares:
            pyglet.shapes.Rectangle(x=abs(side - m.x)*64 + 16, y=abs(side - m.y)*64 + 16, width=32, height=32, color=(255, 100, 100, 255)).draw()

#--------------------------------------------------

def in_bound(x, y) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

#--------------------------------------------------

def is_piece_turn(piece, turn) -> bool:
    return piece.color == turn%2

#==================================================
