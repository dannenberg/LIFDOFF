import pygame
from action import Action

class UnitFactory(object):
    TADPOLE = 1
    def __new__(_, idd, loc):
        if idd == UnitFactory.TADPOLE:
            return Unit(loc, (1,1), "../img/tadpole.png")
        else:
            raise ValueError("Unknown unit id "+idd)

class Unit:
    def __init__(self, (x,y), (w, h), imgsrc, parent=None):
        S = 30 # TODO move this to global or at least remove it from each unit
        self._parent = parent
        self.addons = []
        self._tileset = pygame.image.load(imgsrc)
        self._spr_src = (0,0)     # topleft of source tile
        self._size = (w, h)         # width/height
        self._spr_size = (w*S, h*S) # width and height in pixels
        self._loc = (x,y)           # location on the board
        self._actions = []
        
    def advance_sprite(self):
        x = self._spr_src[0]+30
        if x == 90:
            x = 0
        self._spr_src = (x, self._spr_src[1])
        
    def draw_sprite(self, destsurface, loc = None):
        S = 30
        self.advance_sprite()
        if loc != None:             # determine correct relative positioning for addons and recursion
            loc = tuple(map(sum,zip(self._loc, loc))) #sum the tuples
        else:
            loc = self._loc
        for x in self.addons:           # drawing subpieces
            x.draw_sprite(destsurface, loc)
            #print "unit.draw_sprite: subpieces!"
        #print "unit.draw_sprite: drawin maself @ "+str([z*S for z in loc])+", from "+str(self._spr_src)+" "+str(self._spr_size)
        destsurface.blit(self._tileset, [z*S for z in loc], (self._spr_src, self._spr_size))
    
    def update_position(self, pos=None):
        self._loc = pos
        # TODO collisions

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

    def on_click(self):
        self._actions.append(Action(Action.MOVE, (self._loc[0]-1, self._loc[1])))   # TODO MAKE RELATIVE
        self._actions.append(Action(Action.MOVE, (self._loc[0]-2, self._loc[1])))   # TODO MAKE RELATIVE
        self._actions.append(Action(Action.MOVE, (self._loc[0]-3, self._loc[1])))   # TODO MAKE RELATIVE
        print "Unit.on_click: yay"
