import pygame
import random
import math
from displayscreen import *

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

screens = {"game": GameScreen(),
           "main": MainScreen()}

pygame.display.set_caption("LIFDOFF")

done=False
clock = pygame.time.Clock()

mainscreen = MainScreen()
gamescreen = GameScreen()

def limitByMultiple(x,y,s):
    return ((x-y)//s)*s+y

def mouseout(scr):
    scr.highlightSquare = None

def hold(scr, mpos):
    scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-scr.MAINY-1,0,scr.squaresize)+1),0)
gamescreen.overbox.append((200,69,1049,330),hold,mouseout)  # !?!?!?!?!?!

def hold(scr, mpos):
    scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-scr.MAINY-1,0,scr.squaresize)+1),1)
gamescreen.overbox.append((200,409,1049,330),hold,mouseout)

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
