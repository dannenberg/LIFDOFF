import pygame
import random
import math
from displayscreen import Screen

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

pygame.display.set_caption("LIFDOFF")

done=False
clock = pygame.time.Clock()

def mainscreenInit(self):
    buttonOffset = 3
    self.squaresize=30
    self.waterLevel=0
    self.waterRange=self.squaresize/4
    self.MAINY=-10
    
    self.myBoard = pygame.Surface((1050,330))
    self.enemyBoard = pygame.Surface((1050,330))
    
    self.highlightSquare = None
    self.highlight = pygame.Surface((self.squaresize,self.squaresize))  # the size of your rect
    self.highlight.set_alpha(128)                # alpha level
    self.highlight.fill(color["highlight"])           # this fills the entire surface
    
    mmbutton = pygame.image.load("img/mainmenu.png")
    ubutton  = pygame.image.load("img/upgrades.png")
    sbutton  = pygame.image.load("img/shop.png")
    abutton  = pygame.image.load("img/action.png")
    
    self.buttonBar = pygame.Surface((1280,60))
    self.buttonBar.fill(color["bg"])
    cblit = size[0]+buttonOffset
    for x in (mmbutton, ubutton, sbutton):
        cblit -= x.get_size()[0]+buttonOffset
        self.buttonBar.blit(x, (cblit,0))
    self.buttonBar.blit(abutton, (0,0))
    
    self.boardSansButtons = pygame.Surface((1280,742))
    
    self.gridlines = pygame.Surface((1050,330), pygame.SRCALPHA)   # per-pixel alpha
    for x in xrange(0,1079,self.squaresize):
        pygame.draw.line(self.gridlines,(0,0,0,64),(x,0),(x,330),2)   # v gridline
        pygame.draw.line(self.gridlines,(0,0,0,64),(0,x),(1050,x),2)  # h gridline

def mainscreenDisplay(self, screen):
    self.boardSansButtons.fill(color["bg"])
    
    pygame.draw.rect(self.enemyBoard,color["sky"],(0,0,1050,330))
    pygame.draw.rect(self.myBoard,color["sky"],(0,0,1050,330))
    
    self.waterLevel = (self.waterLevel+(math.pi/180))%(math.pi*2)
    modifier = int(self.squaresize*2.5+math.sin(self.waterLevel)*self.waterRange)
    pygame.draw.rect(self.myBoard,color["water"],(0,modifier,1050,330-modifier))
    pygame.draw.rect(self.enemyBoard,color["water"],(0,modifier,1050,330-modifier))
    
    
    pygame.draw.rect(self.boardSansButtons,color["attackbut"],(0,70,201,335))
    for x in xrange(0,201,67):  # attacker list
        pygame.draw.line(self.boardSansButtons,color["lines"],(x,70),(x,405),2)
    for x in xrange(70,410,67): # same but horiz
        pygame.draw.line(self.boardSansButtons,color["lines"],(0,x),(201,x),2)
    
    if self.highlightSquare != None:
        if not self.highlightSquare[1]:
            self.myBoard.blit(self.highlight, self.highlightSquare[0])
        else:
            self.enemyBoard.blit(self.highlight, self.highlightSquare[0])
    self.myBoard.blit(self.gridlines, (0,0))
    self.enemyBoard.blit(self.gridlines, (0,0))
    self.boardSansButtons.blit(self.myBoard, (201,70))
    self.boardSansButtons.blit(self.enemyBoard, (201,410))
    
    pygame.draw.line(self.boardSansButtons,color["lines"],( 201,  70),( 201, 740),2)  # side line
    pygame.draw.line(self.boardSansButtons,color["lines"],(   0,  70),(1250,  70),2)  # top line
    pygame.draw.line(self.boardSansButtons,color["lines"],( 201, 400),(1250, 400),2)  # center line t
    pygame.draw.line(self.boardSansButtons,color["lines"],(1250, 400),(1250,  70),2)  # right line t
    pygame.draw.line(self.boardSansButtons,color["lines"],(   0, 405),( 201, 405),2)  # center line c
    pygame.draw.line(self.boardSansButtons,color["lines"],( 201, 410),(1250, 410),2)  # center line b
    pygame.draw.line(self.boardSansButtons,color["lines"],(1250, 740),(1250, 410),2)  # right line b
    pygame.draw.line(self.boardSansButtons,color["lines"],(   0, 740),(1280, 740),2)  # bottom line
    
    screen.blit(self.boardSansButtons, (0,self.MAINY))
    screen.blit(self.buttonBar, (0, 740))

mainscreen = Screen(mainscreenInit, mainscreenDisplay)

def limitByMultiple(x,y,s):
    return ((x-y)//s)*s+y

def mouseout(scr):
    scr.highlightSquare = None

def hold(scr, mpos):
    scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-scr.MAINY-1,0,scr.squaresize)+1),0)
mainscreen.overbox.append((200,69,1049,330),hold,mouseout)  # !?!?!?!?!?!

def hold(scr, mpos):
    scr.highlightSquare = ((limitByMultiple(mpos[0]-1,0,scr.squaresize)+1,limitByMultiple(mpos[1]-scr.MAINY-1,0,scr.squaresize)+1),1)
mainscreen.overbox.append((200,409,1049,330),hold,mouseout)

while not done:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.MOUSEMOTION:
            mainscreen.over(pygame.mouse.get_pos())
    
    screen.fill(color["bg"])
    mainscreen.display(screen)
    
    pygame.display.flip()

pygame.quit ()
