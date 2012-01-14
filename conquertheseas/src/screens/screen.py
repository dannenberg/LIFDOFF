import pygame
from mousehitbox import MouseHitboxes

class Screen(object):
    """Screen initializes colors, mouse over/clicked events,
    and the display for launch
    nominally abstract"""
    color= {"black"     :(0x00, 0x00, 0x00),
            "white"     :(0xFF, 0xFF, 0xFF),
            "submergedt":(0xFF, 0x99, 0x66),
            "water"     :(0x00, 0x66, 0x99),
            "bg"        :(0x33, 0x33, 0x33),
            "highlight" :(0xCC, 0xCC, 0x00),
            "lines"     :(0x00, 0x00, 0x00),
            "sky"       :(0xCC, 0xFF, 0xFF),
            "sand"      :(0xFF, 0xCC, 0x66),
            "attackbut" :(0xCC, 0xCC, 0xCC),
            "shopbg"    :(0x99, 0xCC, 0xFF)}
    
    _instance = {}
    def __new__(cls):   # Create Screen and all subclasses as Singletons
        if cls not in Screen._instance: # first creation
            Screen._instance[cls] = super(Screen, cls).__new__(cls)   # create a new one
        return Screen._instance[cls]  # return the old one
    
    def __init__(self):
        self.size = (1280, 800)
        self.clickbox = MouseHitboxes()
        self.overbox = MouseHitboxes()

    def display(self, screen):
        """takes a screen draws screen state to screen"""
        screen.fill(Screen.color["bg"])
    
    def click(self, mpos):
        """handles click events"""
        result = self.clickbox[mpos]
        if result != None:
            print "screen.click: "+str(mpos) + " " + str((mpos[0] - result["left"], mpos[1] - result["top"]))
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))
        else:
            print "screen.click: "+str(mpos)+": No item found"
    
    def over(self, mpos):
        """handles mouseover events"""
        self.overbox.out(mpos)(self)
        result = self.overbox[mpos]
        if result != None:
            result["on"](self, (mpos[0] - result["left"], mpos[1] - result["top"]))
