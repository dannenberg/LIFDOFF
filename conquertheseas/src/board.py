from unit import Unit,UnitFactory
from defense import DefensiveUnit
from action import Action
from constants import SQUARE_SIZE, BOARD_SQUARES_X, BOARD_SQUARES_Y
import pygame

class Board:
    def __init__(self, w, h, name, purple=False):
        self.name = name
        self.surface = pygame.Surface((w*SQUARE_SIZE, h*SQUARE_SIZE), pygame.SRCALPHA)
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # initialize the board size
        self.units = []
        self._actions = []
        self.exp = 20
        self.gold = 0
        self.next_terrain = 0
        
        for i in xrange(3):
            self.add_unit(DefensiveUnit(i, purple))
    
    def __getstate__(self):
        # !!!! CRITICALLY IMPORTANT !!!!
        # If we need to change the order or contents of the items in this function,
        # or the accompanying __setstate__, or really any sort of save/load helper
        # function, increment the VERSION number in constants.py
        return [self.name, self._w, self._h, self.cells, self.units, self._actions, self.exp, self.gold]
        
    def __setstate__(self, data):
        # !!!! CRITICALLY IMPORTANT !!!!
        # See above
        self.surface = pygame.Surface((w*SQUARE_SIZE, h*SQUARE_SIZE), pygame.SRCALPHA)
        self.name, self._w, self._h, self.cells, self.units, self._actions, self.exp, self.gold = data
    
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
    
    def take_turn(self, rand):
        for unit in self.units:
            if unit._class not in (Unit.STAGING, Unit.DEFENSE):
                unit.create_move(rand)
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
                    if collided is not None and collided is not unit:
                        # this is confusing as anything so comments
                        if collided._class == unit._class:
                            if collided.moved or (collided._actions and collided._actions[0].action != Action.MOVE): # he's moved already, or he's not GOING to move
                                print "in the if"
                                unit._actions = []  # bunp
                                unit.take_damage(self, 0)
                                # TODO : Take some damage: may i suggest len(collided.get_shape())*c
                                return False
                            else:   # if he's gonna move into you dats bad
                                print "in the else - this unit hasn't moved"
                                #print "collided._actions is " + str(collided._actions)
                                #print "collided._actions[0].action == Action.MOVE is " + str(collided._actions[0].action)
                                if collided._actions and collided._actions[0].action == Action.MOVE:
                                    print "in the if"
                                    cloc = collided._actions[0].loc
                                    for cx,cy in collided.get_shape():
                                        if (cx+cloc[0], cy+cloc[1]) in nextlocs:    # onoz!
                                            print "units actually colliding in the if"
                                            unit.take_damage(self, 0)   # same as prev TODO
                                            return False
                                # otherwise he'll resolve the collision on his turn
                        else:
                            if not unit.on_collision(collided, self):
                                return False
                            
                    #else:
                        #print "board.unit_take_action: No collision!"
                if unit in self.units:
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
    
    def clear_staging(self):
        for unit in self.units[:]:
            if unit._class == Unit.STAGING:
                self.remove_unit(unit)
    
    def remove_staging(self):
        for unit in self.units[:]:
            if unit._class == Unit.STAGING:
                self._actions.append(Action(Action.CREATE, unit._loc, unit._token))
                self.remove_unit(unit)
    
    def initialize_turn(self, rand):
        self.generate_terrain(rand)
        self.generate_gold(rand)
        for unit in self.units:
            if unit._class == Unit.DEFENSE:
                # apply effects
                for effect in unit.effects[:]:
                    # {type: speed, amount: x, left: y, default: z}
                    print "defensiveUnit has an effect", effect
                    if effect["type"] == 1:
                        if effect["default"] == None:
                            effect["default"] = unit._move_speed
                            unit._move_speed = effect["default"] - effect["amount"]
                        if effect["left"] == 0:
                            unit._move_speed = effect["default"]
                            unit.effects.remove(effect)
                            print "removing bad effect"
                        else:
                            effect["left"] -= 1
            unit._unaltered_loc = unit._loc
            unit.moves_remaining = unit._move_speed
    
    def generate_terrain(self, rand):
        temp = self.next_terrain
        randval = rand.randint(0,3)
        print "generate_terrain", randval
        if randval == 0:
            temp -= 1
        elif randval == 1:
            temp += 1
        temp = max(0, min(2, temp))
        
        for i in xrange(self.next_terrain):
            self.add_unit(UnitFactory(UnitFactory.TERRAIN1, (BOARD_SQUARES_X-1, BOARD_SQUARES_Y-i-1)))
            self.units[-1].level = 4
            if self.cells[BOARD_SQUARES_X-2][BOARD_SQUARES_Y-i-1] is not None and self.cells[BOARD_SQUARES_X-2][BOARD_SQUARES_Y-i-1]._class == Unit.TERRAIN:
                self.units[-1].level |= 8
            if temp-1 >= i:
                self.units[-1].level |= 2
            if self.next_terrain-1 > i:
                self.units[-1].level |= 1
            print "Level",self.units[-1].level
        
        self.next_terrain = temp
    
    def generate_gold(self, rand):
        randval = rand.randint(0,9)
        print "generate_gold", randval
        if randval == 0:
            randY = rand.randint(3,8)
            print "generate_gold", randY
            self.add_unit(UnitFactory(UnitFactory.GOLD, (BOARD_SQUARES_X-1, randY)))
        
    def move_unit(self, unit, loc=None):
        if loc == None:
            loc = unit._loc
        if loc[0] < 0 or loc[0] > BOARD_SQUARES_X-1 or loc[1] < 0 or loc[1] > BOARD_SQUARES_Y-1:
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
