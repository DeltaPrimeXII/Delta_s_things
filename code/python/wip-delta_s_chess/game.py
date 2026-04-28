#Delta's Chess

# import pyglet

class Coord:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, adder:tuple) -> "Coord":
        return Coord(self.x + adder[0], self.y + adder[1])
    
    def __sub__(self, subber:tuple) -> "Coord":
        return Coord(self.x - subber[0], self.y - subber[1])

    #TODO change this
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
        self.controled_cases = []
    
    def __repr__(self):
        return f"{"w" if self.color == 0 else "b"}_{self.name}"
    
    def can_move(self, coord) -> bool:
            x, y = coord.x, coord.y
            if in_bound(x, y):# (in_bound)
                self.controled_cases.append(coord)
                if self.board[x][y] is None:# (empty_case)
                    self.moves.append(coord)
                    return True
                elif self.board[x][y].color != self.color:
                    self.moves.append(coord)
                    return True
            return False

    # #TODO
    # def remove_illegal_moves(self):
    #     pass

    # def update_moves(self):
    #     self.set_all_moves()
    #     self.remove_illegal_moves()

    def move(self, coord:"Coord"):
        x, y = coord.x, coord.y
        if self.board[x][y]:
            self.board.team_list[self.board[x][y].color].remove(self.board[x][y])
        self.board[x][y] = self
        self.board[self.pos.x][self.pos.y] = None
        self.pos = coord
        if hasattr(self, "has_moved"):
            self.has_moved = True

#--------------------------------------------------

class Pawn(Piece):

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "pawn", x, y, color)
        self.has_moved = False


    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
        direction = (1 if self.color == 0 else -1)
        
        x, y = self.pos.x, self.pos.y + direction
        if in_bound(x, y) and self.board[x][y] is None:# 1 square
            self.moves.append(Coord(x, y))
            if (in_bound(x, y + direction)) and (not self.has_moved) and self.board[x][y + direction] is None:# 2 squares
                self.moves.append(Coord(x, y + direction))

        for i in range(-1, 2, 2):# diagonal attacks
            x, y = self.pos.x + i, self.pos.y + direction
            if in_bound(x, y):
                self.controled_cases.append(Coord(x, y))
                if self.board[x][y]:
                    self.moves.append(Coord(x, y))

#--------------------------------------------------

class Knight(Piece):

    move_options = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                    (2, 1), (-2, 1), (2, -1), (-2, -1),]

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "knight", x, y, color)

    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
        for m in Knight.move_options:
            self.can_move(self.pos + m)

#--------------------------------------------------

class Bishop(Piece):

    move_options = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "bishop", x, y, color)

    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
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
        self.has_moved

    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
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

    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
        for m in Queen.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m[0]*i, m[1]*i)
                if not self.can_move(target_pos):
                    break
                i += 1

#--------------------------------------------------

class King(Piece):

    def __init__(self, board:"Board", x=0, y=0, color= 0):
        Piece.__init__(self, board, "king", x, y, color)
        self.has_moved = False
        self.is_checked = 0 #number of pieces checking the king
        self.pinned_pieces = [] #(piece, line)

    def set_all_moves(self) -> None:
        self.moves = []
        self.controled_cases = []
        for m in Queen.move_options:
            self.can_move(self.pos + m)
    
    def get_line(self, dir:"Coord") -> list:
        line = []
        for i in range(8):
            x, y = dir.x*i, dir.y*i
            if in_bound(x, y) and self.board[x][y] and self.board[x][y].color != self.color:
                line.append(Coord(x, y))
                break
            line.append(Coord(x, y))
        return line

    def detect_check_and_pins(self):
        self.is_checked = 0
        self.pinned_pieces = []

        for m in Knight.move_options:
            x, y = self.pos + m
            if in_bound(x, y) and self.board[x][y] is Knight:
                self.is_checked += 1

        for m in Bishop.move_options:
            line = self.get_line(Coord(m[0], m[1]))
            if line:
                last = self.board[line[-1].x][line[-1].y]
                if last is Bishop or last is Queen:
                    count = 0
                    for p in line:
                        if p and p.color == self.color:
                            count += 1
                            pinned = p
                    if count == 0:
                        self.is_checked += 1
                    elif count == 1:
                        self.pinned_pieces.append((pinned, line))

        for m in Rook.move_options:
            line = self.get_line(Coord(m[0], m[1]))
            if line:
                last = self.board[line[-1].x][line[-1].y]
                if last is Rook or last is Queen:
                    count = 0
                    for p in line:
                        if p and p.color == self.color:
                            count += 1
                            pinned = p
                    if count == 0:
                        self.is_checked += 1
                    elif count == 1:
                        self.pinned_pieces.append((pinned, line))
        
        for i in range(-1, 2, 2):
            x, y = self.pos.x + i, self.pos + (1 if self.color == 0 else -1)
            if self.board[x][y] and self.board[x][y] is Pawn:
                self.is_checked += 1


    #TODO override the method for the king
    def remove_illegal_moves(self):
        pass

#--------------------------------------------------

class Board:

    default_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self):
        self.case = [[None]*8 for _ in range(8)]
        self.team_list = [[], []]
        self.kings = []
        self.turn = 0
        self.selected_piece = None

        for x in range(8):
            for y in range(8):
                if y <= 1 or y >= 6:

                    if y == 1 or y == 6:
                        self.case[x][y] = Pawn(self, x, y, 0 if y < 4 else 1)
                    else:
                        self.case[x][y] = Board.default_pieces[x](self, x, y, 0 if y < 4 else 1)
                        if self.case[x][y] is King:
                            self.kings.append(self.case[x][y])

                    if y < 4:
                        self.team_list[0].append(self.case[x][y])
                    else:
                        self.team_list[1].append(self.case[x][y])
    
    def __repr__(self):
        for x in range(7, -1, -1):
            for y in range(8):
                print(self.case[y][x], end=" ")
            print("")
        print(self.team_list)
        return ""

    def __getitem__(self, key):
        return self.case[key]

#==================================================

def in_bound(x, y) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

#--------------------------------------------------

def is_piece_turn(piece, turn) -> bool:
    return piece.color == turn%2

#==================================================

# yes = Board()
# print(yes)
