import pygame
class Unit:
    def __init__(self, (x, y), (w, h), imgsrc, parent=None):
        S = 30 # TODO move this to global or at least remove it from each unit
        self._parent = parent
        self.addons = []
        self._tileset = pygame.image.load(imgsrc)
        self._spr_src = (50,50)     # topleft of source tile
        self._size = (w, h)         # width/height
        self._spr_size = (w*S, h*S) # width and height in pixels
        self._loc = (x,y)           # location on the board
        
    def draw_sprite(self, destsurface, loc = None):
        if loc != None:             # determine correct relative positioning for addons and recursion
            loc = tuple(map(sum,zip(self._loc, loc))) #sum the tuples
        else:
            loc = self._loc
        for x in self.addons:           # drawing subpieces
            x.draw_sprite(destsurface, loc)
        destsurface.blit(self._tileset, [z*S for z in loc], (self._spr_src, self._spr_size))
    
    def update_position(self, pos):
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
