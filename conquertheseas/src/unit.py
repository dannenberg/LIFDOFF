import pygame
class Unit:
    def __init__(self, (x, y), (w, h), imgsrc):
        S = 25
        self.addons = []
        self._tileset = pygame.image.load(imgsrc)
        self._size = (w, h)         # width/height
        self._spr_size = (w*S, h*S) # 
        self._loc = (x,y)
        self._spr_dest = (x*S, y*S) # 
        
    def draw_sprite(self, destsurface):
        for x in self.addons:
            x.draw_sprite(destsurface)
        destsurface.blit(self._tileset, self._spr_dest)
