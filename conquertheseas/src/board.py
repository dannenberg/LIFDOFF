import Unit
import pygame

class Board:
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self.cells = [None for z in xrange(w*h)]    # initialize the board size
        self.units = []
        
    def draw_board(self, destsurface):
        for x in self.units:
            x.draw_sprite(destsurface)
