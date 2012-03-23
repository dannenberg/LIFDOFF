import pygame
from action import Action
from constants import SQUARE_SIZE

class UnitFactory(object):
    MINE = 1
    CRAB = 2
    SQUIDDLE = 3
    MERMAID = 4
    BULLET = 5
    TADPOLE = 6
    ANGRYFISH = 7
    unitsize = {TADPOLE:(1,1), MINE:(2,2), CRAB:(1,1), SQUIDDLE:(1,1), MERMAID:(2,1), BULLET:(1,1), ANGRYFISH:(1,1)}
    
    def __new__(_, idd, loc, fo_real=False):
        utype = Unit.OFFENSE if fo_real else Unit.STAGING
        utoken = None if fo_real else idd
        if idd == UnitFactory.TADPOLE:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/tadpole.png", utype, 5, 5, token=utoken)
        if idd == UnitFactory.MINE:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/mine.png", utype, 5, 5, token=utoken)
        if idd == UnitFactory.CRAB:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/crab.png", utype, 5, 5, token=utoken)
        if idd == UnitFactory.SQUIDDLE:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/squiddle.png", utype, 5, 5, token=utoken)
        if idd == UnitFactory.MERMAID:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/mermaid.png", utype, 10, 5, token=utoken)
        if idd == UnitFactory.ANGRYFISH:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/angryfish.png", utype, 10, 5, token=utoken)
        if idd == UnitFactory.BULLET:
            return Unit(idd, loc, UnitFactory.unitsize[idd], "../img/bullet.png", Unit.BULLET, 0, 0)
        raise ValueError("Unknown unit id "+str(idd))
    
    @staticmethod
    def get_shape_from_token(idd):	# returns the size of the unit (0,0),(0,1),(1,0),(1,1) for a 2x2 unit
        return [(x,y) for x in xrange(UnitFactory.unitsize[idd][0]) for y in xrange(UnitFactory.unitsize[idd][1])]

class Unit(object):
    DEFENSE = 1
    OFFENSE = 2
    BULLET  = 3
    STAGING  = 0
    def __init__(self, idd, (x,y), (w, h), imgsrc, cls, gold, val, parent=None, token=None):
        if parent != None:
            self._class = parent._class
            self._parent = parent
        else:
            self._parent = None
            self._class = cls
        self.idd = idd
        self._tileset = pygame.image.load(imgsrc)
        self._token = token
        self._spr_src = (0,0)     # topleft of source tile
        self._size = (w, h)         # width/height
        self._spr_size = (w*SQUARE_SIZE, h*SQUARE_SIZE) # width and height in pixels
        self._loc = (x,y)           # location on the board
        self._unaltered_loc = (x,y)
        self._actions = []
        self.exp_value = val
        self.cash_value = gold
        self._move_speed = 3
        self.moves_remaining = self._move_speed
        self.health = 1
        
        def __getstate__(self):
        # !!!! CRITICALLY IMPORTANT !!!!
        # If we need to change the order or contents of the items in this function,
        # or the accompanying __setstate__, or really any sort of save/load helper
        # function, increment the VERSION number in constants.py
        
                    self._parent = None
            self._class = cls
        self.idd = idd
        self._tileset = pygame.image.load(imgsrc)
        self._token, self._spr_src, self._size, self._spr_size, self._loc, self._unaltered_loc, self._actions, self.exp_value, self.cash_value, self._move_speed, self.moves_remaining, self.health
        return [self._w, self._h, self.cells, self.units, self._actions, self.exp, self.gold]
        
    def __setstate__(self, data):
        # !!!! CRITICALLY IMPORTANT !!!!
        # See above
        self._w, self._h, self.cells, self.units, self._actions, self.exp, self.gold = data
        
    def advance_sprite(self):
        x = self._spr_src[0]+self._spr_size[0]
        if x == self._spr_size[0]*3:
            x = 0
        self._spr_src = (x, self._spr_src[1])
        
    def draw_sprite(self, destsurface, loc = None):
        #self.advance_sprite() # TODO wrong
        if loc != None: # for drawing an addon using relative position
            loc = tuple(map(sum,zip(self._loc, loc))) #sum the tuples
        else:
            loc = self._loc
        destsurface.blit(self._tileset, [z*SQUARE_SIZE for z in loc], (self._spr_src, self._spr_size))
    
    def update_position(self, pos=None):
        self._loc = pos
        # TODO collisions

    def get_coord(self):
        if self._parent:
            return tuple(map(sum,zip(self._loc, self._parent.get_coord())))
        return self._loc

    def get_cells(self):
        coord = self.get_coord()
        return [(coord[0]+x, coord[1]+y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]
        
    def get_shape(self):
        return [(x, y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]
    
    def queue_movements(self, dests):
        for d in dests:
            self.moves_remaining -= 1
            self._actions.append(Action(Action.MOVE, d))
            
    def queue_shoot(self):
        self.moves_remaining -= 1
        self._actions.append(Action(Action.SHOOT))
    
    def reset_moves(self, board):
        board.move_unit(self, self._unaltered_loc)
        self.moves_remaining = self._move_speed
        self._loc = self._unaltered_loc
        self._actions = []

    def take_damage(self, board, dmg=None):
        """ Returns remaining health """
        print "unit.take_damage: Taking",dmg,"damage"
        if dmg is None or self.health-dmg <= 0:
            board.gold+=self.cash_value
            board.exp+=self.exp_value
            board.remove_unit(self) # D:
            self.health = 0
        else:
            self.health -= dmg
        return self.health
    
    def on_collision(self, opposed, board):
        """ Returns damage done to opponent """
        opposed.take_damage(board, 5)   # TODO: 5?
        self.take_damage(board)
        return 5
    
    def create_move(self):
        if self._class == Unit.BULLET:
            for i in xrange(self._move_speed):
                self._actions.append(Action(Action.MOVE, (self._loc[0] + i + 1, self._loc[1])))
        elif self._class == Unit.OFFENSE:
            for i in xrange(self._move_speed):
                self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
