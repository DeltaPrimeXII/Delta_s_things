#Delta's Chess

class Coord:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
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

    def __init__(self, board:"Board", name:str, x=0, y=0, color=True):#True == "white" and False == "black"
        self.board = board
        self.name = name
        self.pos = Coord(x, y)
        self.color = color
        self.moves = []
    
    def __repr__(self):
        return f"{"white" if self.color else "black"} {self.name}"
    
    def can_move(self, coord) -> bool:#return (in_bound) and (empty_case or opponent_piece)
            return (
                (0 <= coord.x < 8 and 0 <= coord.y < 8) and 
                (self.board.case[coord.y][coord.x] == None or 
                self.board.case[coord.y][coord.x].color != self.color if self.name != "pawn" else False)
            )

    #TODO
    def remove_illegal_moves(self):
        pass

    def update_moves(self):
        self.possible_moves()
        self.remove_illegal_moves()

#--------------------------------------------------

class Pawn(Piece):

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "pawn", x, y, color)
        self.has_moved = False

    def possible_moves(self):
        moves = []
        if self.can_move(self.pos + (0, 1)):
            moves.append(self.pos + (0, 1))
            if not self.has_moved and self.can_move(self.pos + (0, 2)):
                moves.append(self.pos + (0, 2))
        for i in range(-1, 2, 2):#i = (-1, 1)
            if self.can_move(self.pos + (i, 1)):
                moves.append(self.pos + (i, 1))
        self.moves = moves

#--------------------------------------------------

class Knight(Piece):

    move_options = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                    (2, 1), (-2, 1), (2, -1), (-2, -1),]

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "knight", x, y, color)

    def possible_moves(self):
        moves = []
        for m in Knight.move_options:
            if self.can_move(self.pos + m):
                moves.append(self.pos + m)
        self.moves = moves

#--------------------------------------------------

class Bishop(Piece):

    move_options = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "bishop", x, y, color)

    def possible_moves(self):
        moves = []
        for m in Bishop.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m*i)
                if self.can_move(target_pos):
                    moves.append(target_pos)
                    if self.board.case[target_pos.y][target_pos.x]:
                        break
                else:
                    break
                i += 1
        self.moves = moves

#--------------------------------------------------

class Rook(Piece):

    move_options = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "rook", x, y, color)

    def possible_moves(self):
        moves = []
        for m in Rook.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m*i)
                if self.can_move(target_pos):
                    moves.append(target_pos)
                    if self.board.case[target_pos.y][target_pos.x]:
                        break
                else:
                    break
                i += 1
        self.moves = moves

#--------------------------------------------------

class Queen(Piece):

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "queen", x, y, color)

    def possible_moves(self):
        moves = []
        for m in Bishop.move_options + Rook.move_options:
            i = 1
            while i < 8:
                target_pos = self.pos + (m*i)
                if self.can_move(target_pos):
                    moves.append(target_pos)
                    if self.board.case[target_pos.y][target_pos.x]:
                        break
                else:
                    break
                i += 1
        self.moves = moves

#--------------------------------------------------

class King(Piece):

    def __init__(self, board:"Board", x=0, y=0, color=True):
        Piece.__init__(self, board, "king", x, y, color)

    def possible_moves(self):
        moves = []
        for m in Bishop.move_options + Rook.move_options:
            if self.can_move(self.pos + m):
                moves.append(self.pos + m)
        self.moves = moves

    #TODO override the method for the king
    def remove_illegal_moves(self):
        return super().remove_illegal_moves()

#==================================================

default_board = [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        ["p","p","p","p","p","p","p","p"],
        ["r","n","b","q","k","b","n","r"],
    ]

default_pieces = {
    "p": Pawn,
    "n": Knight,
    "b": Bishop,
    "r": Rook,
    "q": Queen,
    "k": King,
}

class Board:

    def __init__(self):
        self.case = [[None]*8 for _ in range(8)]
        for y in range(len(default_board)):
            for x in range(len(default_board[0])):
                if default_board[y][x] in default_pieces:
                    self.case[y][x] = default_pieces[default_board[y][x]](self, x, y, True)

#==================================================

def test():
    pass

#==================================================

yes = Board()
print(yes.case)