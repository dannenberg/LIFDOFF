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
        self.intro = IntroMovie(self)
        self.game = GameScreen(self)
        self.screens = {"intro":self.intro,
                   "game": self.game,
                   "main": MainScreen(self),
                   "credits":CreditsScreen(self),
                   "upgrade":UpgradeScreen(self),
                   "shop":ShopScreen(self)}

        pygame.display.set_caption("FRIENDS OF THE SEA")

        self.done=False
        clock = pygame.time.Clock()

        self.mainscreen = self.screens["game"]

        while not self.done:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done=True
                elif event.type == pygame.MOUSEMOTION:
                    self.mainscreen.over(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mainscreen.click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    pass
                elif event.type == pygame.KEYUP:
                    pass
            
            command = self.mainscreen.display(self.screen)
            if command == "exit":
                self.done = True
            try:
                if command.split()[0] == "transition":
                    self.mainscreen = screens[command.split()[1]]()
            except (AttributeError, IndexError):
                pass
            
            pygame.display.flip()

        pygame.quit ()

if __name__ == "__main__":
    Main()
