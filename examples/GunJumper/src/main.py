import pygame
import random
import math
from screen import *
from gamescreen import *
from introscreen import *
from mainscreen import *
from creditsscreen import *

pygame.init()

size=(1280,800)
screen=pygame.display.set_mode(size)
# don't put things like "black" in here.
# if something is black, name it after the something
color= {"water"     :(0x00,0x66,0x99),\
        "bg"        :(0x33,0x33,0x33),\
        "highlight" :(0xCC,0xCC,0x00),\
        "lines"     :(0x00,0x00,0x00),\
        "sky"       :(0xCC,0xFF,0xFF),\
        "sand"      :(0xFF,0xCC,0x66),\
        "attackbut" :(0xCC,0xCC,0xCC)}

screens = {"intro":IntroMovie(),
           "game": GameScreen(),
           "main": MainScreen(),
           "credits":CreditsScreen()}

pygame.display.set_caption("LIFDOFF")

done=False
clock = pygame.time.Clock()

mainscreen = screens["main"]

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
            mainscreen = screens[command.split()[1]]
    except:
        pass
    
    pygame.display.flip()

pygame.quit ()
