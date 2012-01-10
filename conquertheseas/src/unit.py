import pygame
class Unit:
    def __init__(self, (x, y), (w, h), imgsrc):
        S = 25
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
