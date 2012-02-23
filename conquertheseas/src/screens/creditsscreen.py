import pygame
import math
from mousehitbox import MouseHitboxes
from screen import Screen
from constants import COLORS
from bg_waves import Waves

class CreditsScreen(Screen):
    """ Main menu screen """
    def __init__(self, main):
        Screen.__init__(self, main)
        self.waves = Waves()
        self.smallerfont = pygame.font.Font(None, 50) #font for menu items
        def go_back(someone, mpos):
            self.main.change_screen("main")
        self.clickbox.append((30,650,102,50), go_back)
        
    def display(self, screen):
        Screen.display(self, screen) #calls super
        self.waves.display(screen)
        
        ####################################
        
        textbox = pygame.Surface((1220, 430), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 128))
        for i,x in enumerate(("-- Credits --\nMatt Dannenberg - Version Control\nBrian Shaginaw - Coding, in its entirety.\nBenson 'Team Leader' Perry - Fuckall"\
                             +"\nPyGame\nPython\nEgoraptor").split("\n")):
            text = self.smallerfont.render(x, True, COLORS["white"])
            textbox.blit(text, (10,10+i*50))
        
        screen.blit(textbox, (30, 200))
        
        text = self.smallerfont.render("Back", True, COLORS["white"])
        backbox = pygame.Surface((text.get_width()+20,50), pygame.SRCALPHA)
        backbox.fill((0,0,0,128))
        backbox.blit(text, (10,10))
        screen.blit(backbox, (30, 650))
