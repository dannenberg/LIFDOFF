import pygame
from action import Action
from constants import SQUARE_SIZE

class UnitFactory(object):
    TADPOLE = 1
    YELLOW_SUB = 2
    BULLET = 3
    def __new__(_, idd, loc):
        if idd == UnitFactory.TADPOLE:
            return Unit(loc, (1,1), "../img/tadpole.png", Unit.OFFENSE)
        if idd == UnitFactory.YELLOW_SUB:
            return Unit(loc, (2,2), "../img/yellow_sub.png", Unit.OFFENSE)
        if idd == UnitFactory.BULLET:
            return Unit(loc, (1,1), "../img/tadpole.png", Unit.BULLET)
        raise ValueError("Unknown unit id "+str(idd))
    
    @staticmethod
    def get_shape_from_token(idd):
        if idd == UnitFactory.TADPOLE:
            return [(0,0)]
        if idd == UnitFactory.YELLOW_SUB:
            return [(x,y) for x in xrange(2) for y in xrange(2)]
        raise ValueError("Unknown unit id "+str(idd))

class Unit(object):
    DEFENSE = 1
    OFFENSE = 2
    BULLET  = 3
    def __init__(self, (x,y), (w, h), imgsrc, parent=None):
        if parent in (Unit.DEFENSE, Unit.OFFENSE, Unit.BULLET):
            self._class = parent
            self._parent = None
        else:
            self._parent = parent
        self._tileset = pygame.image.load(imgsrc)
        self._spr_src = (0,0)     # topleft of source tile
        self._size = (w, h)         # width/height
        self._spr_size = (w*SQUARE_SIZE, h*SQUARE_SIZE) # width and height in pixels
        self._loc = (x,y)           # location on the board
        self._actions = []
        self._move_speed = 3
        
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

    def create_move(self):
        if self._class == Unit.BULLET:
            for i in xrange(self._move_speed):  
                self._actions.append(Action(Action.MOVE, (self._loc[0] + i + 1, self._loc[1])))
        elif self._class == Unit.OFFENSE:
            for i in xrange(self._move_speed):  
                self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
