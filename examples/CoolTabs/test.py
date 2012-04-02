import pygame
from string import lowercase
import random
pygame.init()
size = (600, 600)
tabsize = (100, 30)
screen = pygame.display.set_mode(size)
done = False
numtabs = 9

words = [''.join([random.choice(lowercase) for _ in xrange(7)]).title() for _ in xrange(numtabs)]
tab_selected = None

def redraw_tab(tab, tabs, selected=False):
    global tab_selected
    if not (0 <= tab < numtabs):
        return
    if selected is not False:
        if tab_selected is not None:
            redraw_tab(tab_selected, tabs)    # deselect
        tab_selected = tab
    draw = ((10,0),(0,10),(0,tabsize[1]),tabsize,(tabsize[0],0))
    pygame.draw.polygon(tabs[tab], (0xFF, (selected is not False)*0xFF,0), draw)
    pygame.draw.polygon(tabs[tab], (0,0,0), draw, 3)
    tabs[tab].blit(font.render(words[tab], True, (0xFF,0xFF,0xFF)), (5,5))

def redraw(screen):
    screen.fill((0xFF,0xFF,0xFF))
    pygame.draw.rect(screen, (0,0,0), (tabsize[0]/2, 0, size[0]-tabsize[0], size[1]), 3)
    for i,x in enumerate(tabs):
        bx = (i*(size[0]-tabsize[0]*2))/(numtabs-1) + tabsize[0]/2  # default loc
        if mx is not None:
            val = min(tabsize[0]/2, max(0, ((bx-mx)**3)/(size[0]-tabsize[0]*2)))   # push away from the mouse
            if i==0:
                val = min(val, 0)
            if i==len(tabs)-1:
                val = max(val, 0)
            bx += val
        screen.blit(x, (bx,0))

mx = 0
tabs = []
font = pygame.font.Font(None, tabsize[1])
for x in xrange(numtabs):
    tabs.append(pygame.Surface(tabsize,pygame.SRCALPHA))
    redraw_tab(x, tabs)

clock = pygame.time.Clock()
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if y <= tabsize[1]: # can skip this check in the final code
                i = min(numtabs-1, ((numtabs-1)*(x-tabsize[0]/2))/(size[0]-tabsize[0]*2))
                redraw_tab(i, tabs, True) # inverse of bx's default loc in redraw
        if event.type == pygame.MOUSEMOTION:
            x,y = event.pos
            mx = None
            if y <= tabsize[1]:
                mx = x
    redraw(screen)
    pygame.display.flip()
pygame.quit()
