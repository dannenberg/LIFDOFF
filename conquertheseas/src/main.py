import pygame
import random
import math
from screens.screen import *
from screens.gamescreen import *
from screens.introscreen import *
from screens.mainscreen import *
from screens.creditsscreen import *
from screens.shopscreen import *

pygame.init()

size=(1280,800)
screen=pygame.display.set_mode(size)

screens = {"intro":IntroMovie,
           "game": GameScreen,
           "main": MainScreen,
           "credits":CreditsScreen,
           "shop":ShopScreen}

pygame.display.set_caption("LIFDOFF")

done=False
clock = pygame.time.Clock()

mainscreen = screens["game"]()

while not done:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.MOUSEMOTION:
            mainscreen.over(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mainscreen.click(pygame.mouse.get_pos())
    
    command = mainscreen.display(screen)
    if command == "exit":
        done = True
    try:
        if command.split()[0] == "transition":
            mainscreen = screens[command.split()[1]]()
    except:
        pass
    
    pygame.display.flip()

pygame.quit ()
