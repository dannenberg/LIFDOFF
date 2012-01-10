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
        self._spr_dest = (x*S, y*S) # pixel location on the board (from top left of board)
        
    def draw_sprite(self, destsurface):
        for x in self.addons:           # drawing subpieces
            x.draw_sprite(destsurface)
        destsurface.blit(self._tileset, self._spr_dest, (self._spr_src, self._spr_size))
