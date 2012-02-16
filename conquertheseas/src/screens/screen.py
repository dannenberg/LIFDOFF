import pygame
from constants import COLORS, SIZE_X, SIZE_Y
from mousehitbox import MouseHitboxes

class Screen(object):
    """Screen initializes colors, mouse over/clicked events,
    and the display for launch
    nominally abstract"""
    
    def __init__(self, main):
        self.size = (SIZE_X, SIZE_Y)
        self.scale = 1
        self.main = main
        self.clickbox = MouseHitboxes()
        self.overbox = MouseHitboxes()

    def display(self, screen):
        """takes a screen draws screen state to screen"""
        screen.fill(COLORS["bg"])
    
    def abs_scale(self, size):
        self.scale = size
    
    def click(self, mpos):
        """handles click events"""
        mpos = (int(mpos[0]/self.scale), int(mpos[1]/self.scale))
        result = self.clickbox[mpos]
        if result != None:
            print "screen.click: "+str(mpos) + " " + str((mpos[0] - result["left"], mpos[1] - result["top"]))
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))
        else:
            print "screen.click: "+str(mpos)+": No item found"
    
    def over(self, mpos):
        """handles mouseover events"""
        mpos = (int(mpos[0]/self.scale), int(mpos[1]/self.scale))
        self.overbox.out(mpos)(self)
        result = self.overbox[mpos]
        if result != None:
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))
