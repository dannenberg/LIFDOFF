import pygame
from action import Action
from constants import SQUARE_SIZE

class UnitFactory(object):
    TADPOLE = 1
    YELLOW_SUB = 2
    BULLET = 3
    def __new__(_, idd, loc, fo_real = False):
        if idd == UnitFactory.TADPOLE:
            if fo_real:
                return Unit(loc, (1,1), "../img/tadpole.png", Unit.OFFENSE, 5, 5)
            else:
                return Unit(loc, (1,1), "../img/tadpole.png", Unit.STAGING, 5, 5, token=idd)
        if idd == UnitFactory.YELLOW_SUB:
            if fo_real:
                return Unit(loc, (2,2), "../img/yellow_sub.png", Unit.OFFENSE, 5, 5)
            else:
                return Unit(loc, (2,2), "../img/yellow_sub.png", Unit.STAGING, 5, 5, token=idd)
        if idd == UnitFactory.BULLET:
            return Unit(loc, (1,1), "../img/bullet.png", Unit.BULLET, 0, 0)
        raise ValueError("Unknown unit id "+str(idd))
    
    @staticmethod
    def get_shape_from_token(idd):	# returns the size of the unit (0,0),(0,1),(1,0),(1,1) for a 2x2 unit
        if idd == UnitFactory.TADPOLE:
            return [(0,0)]
        if idd == UnitFactory.YELLOW_SUB:
            return [(x,y) for x in xrange(2) for y in xrange(2)]
        raise ValueError("Unknown unit id "+str(idd))

class Unit(object):
    DEFENSE = 1
    OFFENSE = 2
    BULLET  = 3
    STAGING  = 0
    def __init__(self, (x,y), (w, h), imgsrc, cls, gold, val, parent=None, token=None):
        if parent != None:
            self._class = parent._class
            self._parent = parent
        else:
            self._parent = None
            self._class = cls
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
        self.moved = False
        self.health = 1
        
    def advance_sprite(self):
        x = self._spr_src[0]+self._spr_size[0]
        if x == self._spr_size[0]*3:
            x = 0
        self._spr_src = (x, self._spr_src[1])
        
    def draw_sprite(self, destsurface, loc = None):
        self.advance_sprite() # TODO wrong
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
            self._actions.append(Action(Action.MOVE, d))
            
    def queue_shoot(self):
        self._actions.append(Action(Action.SHOOT))
    
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
