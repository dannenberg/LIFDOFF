import pygame
class Unit:
    def __init__(self):
        pass
        # self._cells = (x1,y1,x2,y2)
        # self._tileset = # image
        # self._spr_size = (x,y)
        # self._spr_src = (x,y)
        # self._spr_dest = 0,0
        
    def spr_dest(self):
        S = 25  # squaresize
        return (z*S for z in self._spr_dest)
        
    def draw_sprite(self, dest):
        pass
