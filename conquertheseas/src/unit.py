import pygame
from action import Action
from constants import SQUARE_SIZE

class UnitFactory(object):
    TADPOLE = 1
    YELLOW_SUB = 2
    def __new__(_, idd, loc):
        if idd == UnitFactory.TADPOLE:
            return Unit(loc, (1,1), "../img/tadpole.png")
        if idd == UnitFactory.YELLOW_SUB:
            return Unit(loc, (2,2), "../img/yellow_sub.png")
        raise ValueError("Unknown unit id "+str(idd))
    
    @staticmethod
    def get_shape_from_token(idd):
        if idd == UnitFactory.TADPOLE:
            return [(0,0)]
        if idd == UnitFactory.YELLOW_SUB:
            return [(x,y) for x in xrange(2) for y in xrange(2)]
        raise ValueError("Unknown unit id "+str(idd))

class Unit:
    def __init__(self, (x,y), (w, h), imgsrc, parent=None):
        self._parent = parent
        self.addons = []
        self._tileset = pygame.image.load(imgsrc)
        self._spr_src = (0,0)     # topleft of source tile
        self._size = (w, h)         # width/height
        self._spr_size = (w*SQUARE_SIZE, h*SQUARE_SIZE) # width and height in pixels
        self._loc = (x,y)           # location on the board
        self._actions = []
        self._abilities = [Action.MOVE, Action.SHOOT]
        
    def advance_sprite(self):
        x = self._spr_src[0]+self._spr_size[0]
        if x == self._spr_size[0]*3:
            x = 0
        self._spr_src = (x, self._spr_src[1])
        
    def draw_sprite(self, destsurface, loc = None):
        self.advance_sprite()
        if loc != None:             # determine correct relative positioning for addons and recursion
            loc = tuple(map(sum,zip(self._loc, loc))) #sum the tuples
        else:
            loc = self._loc
        for x in self.addons:           # drawing subpieces
            x.draw_sprite(destsurface, loc)
            #print "unit.draw_sprite: subpieces!"
        #print "unit.draw_sprite: drawin maself @ "+str([z*SQUARE_SIZE for z in loc])+", from "+str(self._spr_src)+" "+str(self._spr_size)
        destsurface.blit(self._tileset, [z*SQUARE_SIZE for z in loc], (self._spr_src, self._spr_size))
    
    def update_position(self, pos=None):
        self._loc = pos
        # TODO collisions

    def get_abilities(self):
        return self._abilities

    def get_coord(self):
        if self._parent:
            return tuple(map(sum,zip(self._loc, self._parent.get_coord())))
        return self._loc

    def get_cells(self):
        coord = self.get_coord()
        hold = [(coord[0]+x, coord[1]+y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]
        for x in self.addons:
            hold += x.get_cells()
        return hold
        
    def get_shape(self):
        hold = [(x, y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]
        for x in self.addons:
            hold += x.get_cells()
        return hold
    
    def queue_movements(self, dests):
        for d in dests:
            self._actions.append(Action(Action.MOVE, d))

    def on_click(self):
        #self._actions.append(Action(Action.MOVE, (self._loc[0]-1, self._loc[1])))   # TODO MAKE RELATIVE
        #self._actions.append(Action(Action.MOVE, (self._loc[0]-2, self._loc[1])))   # TODO MAKE RELATIVE
        #self._actions.append(Action(Action.MOVE, (self._loc[0]-3, self._loc[1])))   # TODO MAKE RELATIVE
        print "Unit.on_click: yay"
