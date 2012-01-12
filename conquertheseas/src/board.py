from unit import Unit
from action import Action
import pygame

class Board:
    def __init__(self, w, h):
        self.surface = pygame.Surface((w*30, h*30)) # TODO make a const for cell size
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # initialize the board size
        self.units = []
    
    def draw_board(self):
        for x in self.units:
            x.draw_sprite(self.surface)
    
    def get_cell_content(self, (x, y)):
        return self.cells[x][y]
    
    def place_unit(self, unit):
        for (x, y) in unit.get_cells():
            print "board.place_unit: adding "+str(x)+","+str(y)
            self.cells[x][y] = unit
            print self.cells[x][y]
    
    def take_turn(self):
        again = True
        while again:    # if anyone still has moves left
            again = False
            print "board.take_turn: NEW TURN"
            for x in self.units:
                again |= self.unit_take_action(x)   # if any unit moved, check all units again
            # TODO eventually there will be a pause here.
        print "board.take_turn: NO NEW MOVES"
    
    def lift_unit(self, unit):
        for (x, y) in unit.get_cells():
            self.cells[x][y] = None
            
    def unit_take_action(self, unit):
        if len(unit._actions) > 0:
            if unit._actions[0].action == Action.MOVE:
                self.move_unit(unit, unit._actions[0].loc)
                print "board.unit_take_action: MOVED"
            elif unit._actions[0].action == Action.SHOOT:
                pass    # TODO
            elif unit._action[0].action == Action.SPECIAL:
                pass    # TODO
            del unit._actions[0]
            return True
        return False
    
    def move_unit(self, unit, loc=None):
        self.lift_unit(unit)
        unit.update_position(loc)
        self.place_unit(unit)
    
    def add_unit(self, unit):
        self.units.append(unit)
        self.place_unit(unit)
    
    def remove_unit(self, unit):
        self.units.remove(unit)
        self.lift_unit(unit)
