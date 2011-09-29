# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
# Edited a little bit by Brian Shaginaw

# Import a library of functions called 'pygame'
import pygame

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]

pi=3.141592653

# Set the height and width of the screen
size=[400,500]
screen=pygame.display.set_mode(size)

cx = 0
cy = 0
rot = 0

pygame.display.set_caption("Orez's Stuff!")

#Loop until the user clicks the close button.
done=False
clock = pygame.time.Clock()

lr = 0
ud = 0
spd = 2

while done==False:

    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                ud = -1
            elif event.key == pygame.K_a:
                lr = -1
            if event.key == pygame.K_s:
                ud = 1
            elif event.key == pygame.K_d:
                lr = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                ud = max(0,ud)
            elif event.key == pygame.K_a:
                lr = max(0,lr)
            if event.key == pygame.K_s:
                ud = min(0,ud)
            elif event.key == pygame.K_d:
                lr = min(0,lr)
                
    cx += lr*spd
    cy += ud*spd
    
    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.
    
    # Clear the screen and set the screen background
    screen.fill(white)

    # Draw on the screen a green line from (0,0) to (100,100) 
    # 5 pixels wide.
    pygame.draw.line(screen,green,[0,0],[100,100],5)

    # Draw on the screen several green lines from (0,10) to (100,110) 
    # 5 pixels wide using a loop
    y_offset=0
    while y_offset < 100:
        pygame.draw.line(screen,red,[0,10+y_offset],[100,110+y_offset],5)
        y_offset=y_offset+10

    # Select the font to use. Default font, 25 pt size.
    font = pygame.font.Font(None, 25)

    # Render the text. "True" means anti-aliased text. 
    # Black is the color. This creates an image of the 
    # letters, but does not put it on the screen
    text = font.render("Press W",True,black)

    # Put the image of the text on the screen at 250x250
    screen.blit(text, [250,250])
    
    text = font.render("ASD",True,black)
    screen.blit(text, [290,267])

    # Draw a rectangle
    pygame.draw.rect(screen,black,[20,20,250,100],2)
    
    # Draw an ellipse, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen,black,[20,20,250,100],2) 

    # Draw an arc as part of an ellipse. 
    # Use radians to determine what angle to draw.
    pygame.draw.arc(screen,black,[20,220,250,200], 0, pi/2, 2)
    pygame.draw.arc(screen,green,[20,220,250,200], pi/2, pi, 2)
    pygame.draw.arc(screen,blue, [20,220,250,200], pi,3*pi/2, 2)
    pygame.draw.arc(screen,red, [20,220,250,200],3*pi/2, 2*pi, 2)
    
    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen,black,[[100,100],[0,200],[200,200]],5)
    
    # create a new surface, upon which to draw the player
    player = pygame.Surface((18,20))
    # fill it an ugly pink, and make that pink be considered transparent
    player.fill((255,0,255))
    player.set_colorkey((255,0,255))
    # this system is faster than alpha, but doesn't allow for fractional transparency
    pygame.draw.polygon(player,red,[[0,0],[17.32,10],[0,20]],5)
    
    # spin the player-surface by the appropriate amount
    player = pygame.transform.rotate(player, rot)
    rot += 5
    # put the player in the right coordinates (accounting for the transformed spin
    loc = [cx-(player.get_width()-18)/2,cy-(player.get_height()-20)/2]
    
    # print the player-surface to the main surface
    screen.blit(player,loc)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit ()
