import pygame
from ai import AI
from const import *
from board import Board
from config import Config
from square import Square
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.config = Config()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.gamemode = 'ai'
        self.selected_piece = None
        self.hovered_square = None

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    surface.blit(lbl, (5, 5 + row * SQSIZE))
                
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    surface.blit(lbl, (col * SQSIZE + SQSIZE - 20, HEIGHT - 20))
        
        if self.board.last_move:
            self.show_last_move(surface)

        if self.selected_piece:
            self.show_moves(surface)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.selected_piece:
                        piece.set_texture()
                        texture = piece.texture
                        img = pygame.image.load(texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.selected_piece:
            theme = self.config.theme

            for move in self.selected_piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            theme = self.config.theme

            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.col + pos.row) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, 3)

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def next_turn(self):
        self.next_player = 'black' if self.next_player == 'white' else 'white'

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def select_piece(self, piece):
        self.selected_piece = piece
    
    def unselect_piece(self):
        self.selected_piece = None

    def reset(self):
        self.__init__()
