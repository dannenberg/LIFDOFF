import Unit
import pygame

class Board:
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self.cells = [None for z in xrange(w*h)]    # initialize the board size
        
    def draw_board(self, destsurface):
        pass
