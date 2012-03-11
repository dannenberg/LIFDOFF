from unit import Unit,UnitFactory
from defense import DefensiveUnit
from action import Action
from constants import SQUARE_SIZE, BOARD_SQUARES_X, BOARD_SQUARES_Y
import pygame

class Board:
    def __init__(self, w, h, purple=False):
        self.surface = pygame.Surface((w*SQUARE_SIZE, h*SQUARE_SIZE), pygame.SRCALPHA)
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # initialize the board size
        self.units = []
        self._actions = []
        self.exp = 0
        self.gold = 0
        for i in xrange(3):
            self.add_unit(DefensiveUnit(i, purple))
    
    def draw_board(self):
        for x in self.units:
            x.draw_sprite(self.surface)
    
    def get_cell_content(self, (x, y)):
        return self.cells[x][y]
    
    def place_unit(self, unit):
        failure = False
        for (x, y) in unit.get_cells():
            #print "board.place_unit: adding "+str(x)+","+str(y)
            try:
                if self.cells[x][y] != None:    # We're intersecting another unit: ABORT
                    failure = True
                    break
            except IndexError:
                failure = True
                break
            self.cells[x][y] = unit
            #print "board.place_unit "+str(self.cells[x][y])
        if failure:
            for (xr, yr) in unit.get_cells():
                try:
                    if self.cells[xr][yr] == unit:
                        self.cells[xr][yr] = None
                except IndexError:
                    pass
        return not failure
    
    def take_turn(self):
        for unit in self.units:
            if unit._class not in (Unit.STAGING, Unit.DEFENSE):
                unit.create_move()
        for action in self._actions:
            if action.action == Action.CREATE:
                unit = UnitFactory(action.extra, action.loc, True)
                self.add_unit(unit)
        self._actions = []
        again = True
        while again:    # if anyone still has moves left
            again = False
            #print "board.take_turn: NEW TURN"
            for x in self.units[:]:
                again |= self.unit_take_action(x)   # if any unit moved, check all units again
                x.moved = True
            for x in self.units:
                x.moved = False
            # TODO eventually there will be a pause here.
        #print "board.take_turn: NO NEW MOVES"
    
    def lift_unit(self, unit):
        for (x, y) in unit.get_cells():
            self.cells[x][y] = None
            
    def unit_take_action(self, unit):
        if unit not in self.units:  # This, unfortuntately, is a concern
            return False
        if len(unit._actions) > 0:
            if unit._actions[0].action == Action.MOVE:
                mloc = unit._actions[0].loc
                nextlocs = [(x+mloc[0],y+mloc[1]) for x,y in unit.get_shape()]
                for ux,uy in nextlocs:  # this is serverside stuff :(
                    if not (0<=ux<BOARD_SQUARES_X and 0<=uy<BOARD_SQUARES_Y):
                        continue
                    collided = self.cells[ux][uy]
                    if collided != None and collided != unit:
                        # this is confusing as anything so comments
                        if collided._class > unit._class:   # bullet on offense or offense on defense
                            collided.on_collision(unit, self)
                        elif collided._class == unit._class:
                            if unit.moved or unit._actions[0].action != Action.MOVE: # he's moved already, or he's not GOING to move
                                unit._actions = []  # bunp
                                unit.take_damage(self, 0)
                                # TODO : Take some damage: may i suggest len(collided.get_shape())*c
                                return False
                            else:   # if he's gonna move into you dats bad
                                cloc = collided._actions[0].loc
                                for cx,cy in collided.get_shape():
                                    if (cx+cloc[0], cy+cloc[1]) in nextlocs:    # onoz!
                                        unit.take_damage(self, 0)   # same as prev TODO
                                        return False
                                # otherwise he'll resolve the collision on his turn
                        else: # collided._class < unit._class
                            collided.on_collision(unit, self)   # TODO: probably wrong
                    #else:
                        #print "board.unit_take_action: No collision!"
                self.move_unit(unit, mloc)  # the movement
                #print "board.unit_take_action: MOVED"
            elif unit._actions[0].action == Action.SHOOT:
                u = UnitFactory(UnitFactory.BULLET, (unit._loc[0]+3, unit._loc[1]))
                self.add_unit(u)
                pass    # TODO
            elif unit._actions[0].action == Action.SPECIAL:
                pass    # TODO
            del unit._actions[0]
            return True
        return False
    
    def remove_staging(self):
        for unit in self.units[:]:
            if unit._class == Unit.STAGING:
                self._actions.append(Action(Action.CREATE, unit._loc, unit._token))
                self.remove_unit(unit)
    
    def store_cur_pos(self):
        for unit in self.units:
            unit._unaltered_loc = unit._loc

    def move_unit(self, unit, loc=None):
        if loc == None:
            loc = unit._loc
        if loc[0] < 0 or loc[0] > 34 or loc[1] < 0 or loc[1] > 10:
            if unit._class != Unit.DEFENSE:
                self.remove_unit(unit)
        else:
            self.lift_unit(unit)
            unit.update_position(loc)
            self.place_unit(unit)
    
    def add_unit(self, unit):
        if self.place_unit(unit):
            self.units.append(unit)
            return True
        return False
    
    def remove_unit(self, unit):
        self.units.remove(unit)
        self.lift_unit(unit)
        
    def __getattr__(self, name):
        def anon(*args):
            print name,"didn't exist"
            return None
        return anon
