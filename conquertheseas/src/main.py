import pygame
import random
import math
from screens.screen import *
from screens.gamescreen import *
from screens.introscreen import *
from screens.mainscreen import *
from screens.creditsscreen import *
from screens.shopscreen import *
from screens.upgradescreen import *

class Main():
    def __init__(self):
        pygame.init()

        size=(1280,800)
        self.screen=pygame.display.set_mode(size)
        self.screens = {"intro": IntroMovie(self),
                        "game": GameScreen(self),
                        "main": MainScreen(self),
                        "credits":CreditsScreen(self),
                        "upgrade":UpgradeScreen(self),
                        "shop":ShopScreen(self)}

        pygame.display.set_caption("FRIENDS OF THE SEA")

        self.done=False
        clock = pygame.time.Clock()

        self.mainscreen = self.screens["main"]

        self.keys = set()

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
                elif event.type == pygame.KEYUP:
                    self.keys.discard(event.key)
            
            self.mainscreen.display(self.screen)
            
            pygame.display.flip()

        pygame.quit ()
    
    def change_screen(self, screen):
        self.mainscreen = self.screens[screen]

    def exit(self):
        self.done = True

if __name__ == "__main__":
    Main()
