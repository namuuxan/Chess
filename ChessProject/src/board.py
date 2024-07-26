
from const import *
from piece import *
from move import Move
from square import Square

class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def __str__(self):
        s = '\n'
        for row in range(ROWS):
            s += '[ '
            for col in range(COLS):
                sqr = self.squares[row][col]
                s += '[ ]' if sqr.isempty() else str(sqr.piece)
                s += ' '
            s += ']\n'
        return s


    def move(self, piece, move):
        initial = move.initial
        final = move.final
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if piece.name == 'king':
            row = 0 if piece.color == 'black' else 7 
            diff = initial.col - final.col
            if diff == 2:
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    piece.moved = True
                    piece.moves = []
                    piece2 = self.squares[row][0].piece
                    initial = Square(row, 0)
                    final = Square(row, 3)
                    move2 = Move(initial, final)
                    self.move(piece2, move2)
            elif diff == -2:
                piece.moved = True
                piece.moves = []
                piece2 = self.squares[row][7].piece
                initial = Square(row, 7)
                final = Square(row, 5)
                move2 = Move(initial, final)
                self.move(piece2, move2)

      
        if piece.name == 'pawn':
            self.check_promotion(piece, final)

        piece.moved = True
        piece.moves = []

        self.last_move = move

    def check_promotion(self, piece, final):
        promote_row = 0 if piece.color == 'white' else 7

        if final.row == promote_row:
        
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):

        def pawn():
            piece = self.squares[row][col].piece
            if piece.color == 'black':
                if row != 1: piece.moved = True
            if piece.color == 'white':
                if row != 6: piece.moved = True
          
            steps = 1 if piece.moved else 2

          
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        
                        initial = Square(row, col)
                        final = Square(move_row, col, self.squares[move_row][col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            move_cols = [col - 1, col + 1]
            move_row = row + piece.dir
            for move_col in move_cols:
                if Square.in_range(move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                      
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def knight():
            possible_moves = [
            (row - 2, col + 1),
            (row - 1, col + 2),
            (row + 1, col + 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row + 1, col - 2),
            (row - 1, col - 2),
            (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline(incrs):
            for incr in incrs:
                row_inc, col_inc = incr
                move_row = row + row_inc
                move_col = col + col_inc
                while True:
                    if Square.in_range(move_row, move_col):
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        if self.squares[move_row][move_col].isempty():
                            piece.add_move(move)
                        else: 
                            if self.squares[move_row][move_col].has_rival_piece(piece.color):
                              
                                piece.add_move(move)
                            break
                    else: 
                        break
                
                   
                    move_row, move_col = move_row + row_inc, move_col + col_inc

        def king():
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]
            
            for adj in adjs:
                move_row, move_col = adj
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                       
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                
            if not piece.moved:
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    if not lRook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): break
                            if c == 3:
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                rRook = self.squares[row][7].piece
                if isinstance(rRook, Rook):
                    if not rRook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): break
                            if c == 6:
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

        if piece.name == 'pawn': 
            pawn()

        elif piece.name == 'knight': 
            knight()

        elif piece.name == 'bishop': 
            straightline([(-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'rook': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif piece.name == 'queen': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'king': 
            king()
        

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # KNIGHTS
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # BISHOPS
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # ROOKS
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # QUEEN
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # KING
        self.squares[row_other][4] = Square(row_other, 4, King(color))