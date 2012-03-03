import pygame
import random
import math
import re
from constants import SIZE_X,SIZE_Y
from screens.screen import *
from screens.gamescreen import *
from screens.introscreen import *
from screens.mainscreen import *
from screens.creditsscreen import *
from screens.shopscreen import *
from screens.upgradescreen import *
from screens.lobbyscreen import *
from screens.joinscreen import *

class Main():
    def __init__(self):
        pygame.init()

        self.server = None
        self.client = None
        self.stdsize=(SIZE_X,SIZE_Y)
        self.size=self.stdsize
        self.scale = 1
        self.screen=pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.screens = {"intro": IntroMovie(self),
                        "game": GameScreen(self),
                        "main": MainScreen(self),
                        "credits":CreditsScreen(self),
                        "upgrade":UpgradeScreen(self),
                        "shop":ShopScreen(self),
                        "lobby":LobbyScreen(self),
                        "join":JoinScreen(self)}

        pygame.display.set_caption("FRIENDS OF THE SEA")

        self.done=False
        clock = pygame.time.Clock()

        self.mainscreen = self.screens["main"]

        pygame.key.set_repeat(500,20)   # half second delay, 20 second interval
        self.keys = set()
        preblit = pygame.Surface((self.stdsize))
        preblit2 = None
        
        font = pygame.font.Font(None, 16)
        
        while not self.done:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done=True
                elif event.type == pygame.MOUSEMOTION:
                    self.mainscreen.over(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.mainscreen.click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.keys.add(event.key)
                    self.mainscreen.notify_key(event)
                elif event.type == pygame.KEYUP:
                    self.keys.discard(event.key)
                elif event.type == pygame.VIDEORESIZE:
                    self.size,self.scale = self.resize(event.w, event.h)
                    self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
                    self.mainscreen.abs_scale(self.scale)
            
            self.mainscreen.display(preblit)
            preblit.blit(font.render(str(clock.get_fps()), True, (0xFF,0,0)), (0,0))
            preblit2 = pygame.transform.scale(preblit, self.size)
            self.screen.blit(preblit2, (0,0))
            pygame.display.flip()
        pygame.quit()
    
    def change_screen(self, screen):
        self.mainscreen = self.screens[screen]
        if screen == "lobby":
            self.screens[screen].join_lobby()
        self.mainscreen.abs_scale(self.scale)

    def exit(self):
        self.done = True
        
    def reset_screen(self, screen):
        self.screens[screen] = self.screens[screen].__class__(self)
        
    def resize(self, w, h):
        if w==self.size[0]:  # width was constant
            scale = float(h)/self.stdsize[1]
            return ((int(scale*self.stdsize[0]),h),scale)
        scale = float(w)/self.stdsize[0]
        return ((w,int(scale*self.stdsize[1])),scale)
    
    def valid_nick(self, newnick):
        return re.match(r"^[A-Z][A-Z0-9 ]{0,20}[A-Z0-9]$", newnick, re.I)

if __name__ == "__main__":
    Main()
