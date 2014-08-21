from unit import *
from action import Action
from constants import *


class DefensiveUnit(Unit):
    def __init__(self, idd, purple=False):
        #self.upgrades = ()[idd]()
        (x, y) = ((0, 1), (5, 5), (0, 9))[idd]
        if purple:
            super(DefensiveUnit, self).__init__(UnitFactory.PURPLE_SUB, (x, y), Unit.DEFENSE)
        else:
            super(DefensiveUnit, self).__init__(UnitFactory.YELLOW_SUB, (x, y), Unit.DEFENSE)
        self._move_speed = 5
        self.idd = idd  # TODO wrong
        self.moves_remaining = self._move_speed
        self._abilities = [Action.MOVE, Action.SHOOT]
        self.addons = []
        self.effects = []
        self.purple = purple
        self.dead = False

    def __setstate__(self, data):
        self.__dict__.update(data)
        self._tileset = pygame.image.load(UnitFactory.img[UnitFactory.PURPLE_SUB if self.purple else UnitFactory.YELLOW_SUB])

    def draw_sprite(self, destsurface, loc=None):
        self.advance_sprite()
        if loc is not None:             # determine correct relative positioning for addons and recursion
            loc = tuple(map(sum, zip(self._loc, loc)))  # sum the tuples
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
        if not self.moves_remaining:
            return [Action.UNDO]
        if self._actions:
            #print "defense get abilities: " , self._actions
            return self._abilities + [Action.UNDO]
        return self._abilities
