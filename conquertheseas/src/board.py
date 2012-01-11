import Unit
import pygame

class Board:
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # initialize the board size
        self.units = []
    
    def draw_board(self, destsurface):
        for x in self.units:
            x.draw_sprite(destsurface)
    
    def get_cell_content(self, (x, y)):
        return self.cells[x+y*self._h]
    
    def place_unit(self, unit):
        for (x, y) in unit.get_cells():
            self.cells[x][y] = unit
    
    def lift_unit(self, unit):
        for (x, y) in unit.get_cells():
            self.cells[x][y] = None
    
    def move_unit(self, unit, loc):
        self.lift_unit(unit)
        unit.update_position(loc)
        self.place_unit(unit)
    
    def add_unit(self, unit):
        self.units.append(unit)
        self.place_unit(unit)
    
    def remove_unit(self, unit):
        self.units.remove(unit)
        self.lift_unit(unit)
