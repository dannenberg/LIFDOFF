import pygame
import random
import math

##########################
# Line of Sight Test:    #
#   Except it turned out #
#   to look better as a  #
#   3d effect.           #
# \author Brian Shaginaw #
##########################

pygame.init()

black = (0x00,0x00,0x00)
shade = (0x11,0x11,0x11)
white = (0xFF,0xFF,0xFF)
clear = (0xFF,0x00,0xFF)

size=(500,500)  # size of the screen
px,py = 0,0     # player location

# Position of the walls, this just makes two rows of 5
walls = [[(-50+x*150,-150*y),(-50+x*150,-100*y),(-100+x*150,-100*y),(-100+x*150,-150*y),x+1.1,True] for x in xrange(5) for y in xrange(-1,2,2)]
walls.append([(-300,-300),(-300,-350),(700,-350),(700,-300),2,True])
walls.append([(-300,300),(-300,350),(700,350),(700,300),2,True])
walls.append([(-300,-350),(-300,350),(-350,350),(-350,-350),2,True])
walls.append([(700,-350),(700,350),(750,350),(750,-350),2,True])

screen=pygame.display.set_mode(size)
cap = pygame.Surface(size)
cap.set_colorkey(clear)

pygame.display.set_caption("Orez Pillars")

done=False
clock = pygame.time.Clock()
step = 3                        # move speed
diagstep = step/math.sqrt(2)    # move speed diagonally
moving = 0                      # direction you are moving
movekeys = {pygame.K_w:1,\
            pygame.K_a:2,\
            pygame.K_s:4,\
            pygame.K_d:8}

# Call this to redraw the scene.
# Redrawing the scene is expensive: only do this when you move or something changes.
def redraw():
    screen.fill(white)
    cap.fill(clear)
    pygame.draw.circle(screen, black, (size[0]/2, size[1]/2), 10)   # Your character, always in the center of the screen.
    for j,x in enumerate(walls): # Draw each wall and each wall's 'shadow'
        botsq = [(y[0]+px+size[0]/2,y[1]+py+size[1]/2) for i,y in enumerate(x) if i<4] # The screen coordinates of the base squares, as defined in walls
        
        result = [1,1,1,1]
        for z in [(y[0]<0, y[1]<0, y[0]>size[0], y[1]>size[1]) for y in botsq]:
            result = [w and z[i] for i,w in enumerate(result)]
        if True in result:  # if the object in question is deemed to be off the screen.
            walls[j][5] = False
            continue
        walls[j][5] = True
        
        topsq = [((y[0]-size[0]/2)*x[4]+size[0]/2, (y[1]-size[1]/2)*x[4]+size[1]/2) for y in botsq] # the projected tops of the squares:
        # essentially we're projecting a ray from the player to the corners of the base square to a distance of the height of the walls.
        sx1 = (botsq[0],botsq[2],topsq[2],topsq[0]) # draw a 'plane' from the opposite corners of the base to the cooresponding corners of the top.
        sx2 = (botsq[1],botsq[3],topsq[3],topsq[1]) # same, except the other opposite corners.
        pygame.draw.polygon(screen, black, botsq)
        pygame.draw.polygon(screen, black, sx1)
        pygame.draw.polygon(screen, black, sx2)
        pygame.draw.polygon(cap,    shade, topsq)
    screen.blit(cap,(0,0))

def collisionDetection(revert):
    global px,py
    actual = (px,py)
    for x in walls:
        if not x[5]:
            continue
        
        hold = [(revert[0],actual[1]),(actual[0],revert[1]),revert]
        while min(x[0][0],x[2][0])-5 < -px < max(x[0][0],x[2][0])+5 and min(x[0][1],x[2][1])-5 < -py < max(x[0][1],x[2][1])+5:
            px,py = hold[0]
            del hold[0]
            if len(hold) == 0:
                return
        actual = px,py

redraw()            # initial drawing
while not done:     # main loop
    clock.tick(60)  # 60 fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.KEYDOWN:
            if event.key in movekeys:
                moving |= movekeys[event.key]   # add your direction to the moving mess.
        elif event.type == pygame.KEYUP:
            if event.key in movekeys:
                moving &= ~movekeys[event.key]  # remove your direction from the moving mess
    
    if moving:  # this block isn't good code but don't want to fix it
        tm = moving
        if tm&1 and tm&4:   # moving in two opposite directions in once, take em out
            tm &= ~(1|4)    # I recognize this check is done by just adding and subtracting step,
        if tm&2 and tm&8:   # but you would get the wrong speed (the diagonal speed)
            tm &= ~(2|8)
            
        tstep = step
        if (tm&1 or tm&4) and (tm&2 or tm&8):   # if you're moving in two cardinal directions, you move slower in each
            tstep = diagstep
        if tm:  # the actual moving.
            revert = (px,py)
            if tm&1:
                py += tstep
            elif tm&4:
                py -= tstep
            if tm&2:
                px += tstep
            elif tm&8:
                px -= tstep
            
            collisionDetection(revert)
            redraw()
    
    pygame.display.flip()
