import pygame
import random
import math

pygame.init()

size=(1280,800)
screen=pygame.display.set_mode(size)
# don't put things like "black" in here.
# if something is black, name it after the something
color= {"water"    :(0x00,0x66,0x99),\
        "bg"       :(0x33,0x33,0x33),\
        "highlight":(0xCC,0xCC,0x00),\
        "lines"    :(0x00,0x00,0x00),\
        "sky"      :(0xCC,0xFF,0xFF)}

pygame.display.set_caption("LIFDOFF")

done=False
clock = pygame.time.Clock()

buttonOffset = 3
squaresize = 30
waterLevel = 0
waterRange = squaresize/4
MAINY = -10

currentScreen = 1

mmbutton = pygame.image.load("img/mainmenu.png")
ubutton  = pygame.image.load("img/upgrades.png")
sbutton  = pygame.image.load("img/shop.png")
abutton  = pygame.image.load("img/action.png")

buttonBar = pygame.Surface((1280,60))
buttonBar.fill(color["bg"])
cblit = size[0]+buttonOffset
for x in (mmbutton, ubutton, sbutton):
    cblit -= x.get_size()[0]+buttonOffset
    buttonBar.blit(x, (cblit,0))
buttonBar.blit(abutton, (0,0))

highlightSquare = None
highlight = pygame.Surface((squaresize,squaresize))  # the size of your rect
highlight.set_alpha(128)                # alpha level
highlight.fill(color["highlight"])           # this fills the entire surface

boardSansButtons = pygame.Surface((1280,742))

gridlines = pygame.Surface((1079,330), pygame.SRCALPHA)   # per-pixel alpha
for x in xrange(0,1079,squaresize):
    pygame.draw.line(gridlines,(0,0,0,64),(x,0),(x,330),2)   # v gridline
    pygame.draw.line(gridlines,(0,0,0,64),(0,x),(1079,x),2)  # h gridline

def limitByMultiple(x,y,s):
    return ((x-y)//s)*s+y

while not done:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.MOUSEMOTION:
            mpos = pygame.mouse.get_pos()
            if 201<=mpos[0]<limitByMultiple(1280,201,squaresize) and 70<=mpos[1]-MAINY+1<limitByMultiple(400,70,squaresize):
                highlightSquare = (limitByMultiple(mpos[0]+1,201,squaresize)+1,limitByMultiple(mpos[1]-MAINY+1,70,squaresize)+1)
            elif 201<=mpos[0]<limitByMultiple(1280,201,squaresize) and 410<=mpos[1]-MAINY+1<limitByMultiple(740,410,squaresize):
                highlightSquare = (limitByMultiple(mpos[0]+1,201,squaresize)+1,limitByMultiple(mpos[1]-MAINY+1,410,squaresize)+1)
            else:
                highlightSquare = None
    if currentScreen == 1:
        screen.fill(color["bg"])
        boardSansButtons.fill(color["bg"])
        
        pygame.draw.rect(boardSansButtons,color["sky"],(201,70,1079,330))
        pygame.draw.rect(boardSansButtons,color["sky"],(201,410,1079,330))
        
        waterLevel = (waterLevel+(math.pi/180))%(math.pi*2)
        modifier = int(squaresize*2.75+math.sin(waterLevel)*waterRange)
        pygame.draw.rect(boardSansButtons,color["water"],(201,70+modifier,1079,330-modifier))
        pygame.draw.rect(boardSansButtons,color["water"],(201,410+modifier,1079,330-modifier))
        
        pygame.draw.line(boardSansButtons,color["lines"],( 201,  70),( 201, 740),2)  # side line
        pygame.draw.line(boardSansButtons,color["lines"],(   0,  70),(1280,  70),2)  # top line
        pygame.draw.line(boardSansButtons,color["lines"],( 201, 400),(1280, 400),2)  # center line t
        pygame.draw.line(boardSansButtons,color["lines"],(   0, 405),( 201, 405),2)  # center line c
        pygame.draw.line(boardSansButtons,color["lines"],( 201, 410),(1280, 410),2)  # center line b
        pygame.draw.line(boardSansButtons,color["lines"],(   0, 740),(1280, 740),2)  # bottom line
        if highlightSquare != None:
            boardSansButtons.blit(highlight, highlightSquare)
        boardSansButtons.blit(gridlines, (201,70))
        boardSansButtons.blit(gridlines, (201,410))
        
        screen.blit(boardSansButtons, (0,MAINY))
        screen.blit(buttonBar, (0, 740))
    
    pygame.display.flip()

pygame.quit ()
