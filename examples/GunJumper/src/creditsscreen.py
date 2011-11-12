import pygame
import math
from mousehitbox import MouseHitboxes
from screen import Screen

class CreditsScreen(Screen):
    """ Main menu screen """
    def __init__(self):
        Screen.__init__(self)
        self.waterLevel = 0 #defines the height of the water in the background
        self.waterRange = 16 #how much the water level fluctuates
        self.smallerfont = pygame.font.Font(None, 50) #font for menu items
        def go_back(someone, mpos):
            self.command = "transition main"
        self.clickbox.append((30,650,102,50), go_back)
        self.command = ""
        
    def display(self, screen):
        Screen.display(self, screen) #calls super
        
        self.waterLevel = (self.waterLevel + (math.pi / 180)) % (math.pi * 2) #movement in rads for waterlevel (since it is based on sin)
        modifier = int(math.sin(self.waterLevel) * self.waterRange) #actual change
        
        font = pygame.font.Font(None, 170) #title text defined and two colored versions created
        text = font.render("CONQUER THE SEAS", True, Screen.color["black"])
        whitetext = font.render("CONQUER THE SEAS", True, Screen.color["submergedt"])
        
        #draws the sky, water, and text
        screen.fill(Screen.color["sky"])
        water = pygame.Surface((1280, 700 - modifier))
        water.fill(Screen.color["water"])
        screen.blit(text, [20, 50])
        water.blit(whitetext, [20,  -50 - modifier])
        screen.blit(water, [0, modifier + 100])
        
        ####################################
        
        textbox = pygame.Surface((1220, 430), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 128))
        for i,x in enumerate(("-- Credits --\nMatt Dannenberg - Version Control\nBrian Shaginaw - Coding, in its entirety.\nBenson 'Team Leader' Perry - Fuckall"\
                             +"\nPyGame\nPython\nEgoraptor").split("\n")):
            text = self.smallerfont.render(x, True, Screen.color["white"])
            textbox.blit(text, (10,10+i*50))
        
        screen.blit(textbox, (30, 200))
        
        text = self.smallerfont.render("Back", True, Screen.color["white"])
        backbox = pygame.Surface((text.get_width()+20,50), pygame.SRCALPHA)
        backbox.fill((0,0,0,128))
        backbox.blit(text, (10,10))
        screen.blit(backbox, (30, 650))
        
        hold = self.command
        self.command = ""
        return hold