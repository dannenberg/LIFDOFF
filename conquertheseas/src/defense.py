from unit import Unit
from action import Action
from constants import *

class DefensiveUnit(Unit):
    def __init__(self, idd):
        (x,y) = ((0,0),(5,5),(0,9))[idd]
        (w,h) = ((2,2),(2,2),(2,2))[idd]
        imgsrc = ("../img/yellow_sub.png","../img/yellow_sub.png","../img/yellow_sub.png")[idd]
        super(DefensiveUnit, self).__init__((x,y), (w,h), imgsrc, Unit.DEFENSE)
        self._abilities = [Action.MOVE, Action.SHOOT]
        self.addons = []

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

    def get_abilities(self):
        return self._abilities
