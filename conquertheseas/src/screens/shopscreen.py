import pygame
from screen import Screen
from constants import COLORS
from mousehitbox import MouseHitboxes

class ShopScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.prices_and_values = [{"name":"Mine","desc":"Basic nautical weaponry, drop it off and hope for the best. These ones have seen better days.","flav":"During the American Civil War, hundreds of these mines were laid along various rivers. After the war, they were collected by legitimate businesses and put on the market, although almost no one has been crazy enough to buy them."},
                                  {"name":"Angry Fish","desc":"This angry fish will start moving slowly, but will charge forward when it sees an enemy ship.","flav":"Angry Fish were created by mad scientists, in order to stop those who would oppose them. Unfortunately, mad scientists do not have any allies, so Angry Fish have been conditioned to attack all ships."},
                                  {"name":"Squiddle","desc":"Beware of this tanglebuddy's entangling tentacles!","flav":"Squiddles are the My Little Pony of the sea. They spread their joy and love to all that they see, whether they like it or not."},
                                  {"name":"Pufferfish","desc":"The pufferfish will expand and contract its pointy quills. Timing is key!","flav":"Under normal circumstances, the puffer fish will puff out its spines when it is frightened or threatened. So let's just say that just offscreen there's something really scary that shows up every so often."},
                                  {"name":"Live Mine","desc":"Basic nautical weaponry, drop it off and watch it go!","flav":""},
                                  {"name":"Cthulhu","desc":"The Deep One. Walks slowly across the screen, but decimates everything in its path.","flav":"Did you know you could buy Cthulhus? Seriously. You can just go to the store and be like \"Hey do you have any Cthulhus for sale?\" and they'd be all \"Oh yeah of course we can't get rid of the damn (ha ha) things!\""}]
        self.index = 0
        def go_back(someone, mpos):
            self.main.change_screen("game")
        self.clickbox.append((1100,750,180,50), go_back)
        
    def display(self, scr):
        Screen.display(self, scr)
        scr.fill(COLORS["shopbg"])
        pygame.draw.rect(scr, COLORS["sand"], (0,0,1280,320))
        pygame.draw.rect(scr, COLORS["water"], (0,320,560,480))
        for x in xrange(-1,321,160):
            pygame.draw.line(scr, COLORS["black"], (0,x),(1280,x),2)
        for x in xrange(-1,1281,160):
            pygame.draw.line(scr, COLORS["black"], (x,0),(x,320),2)
        pygame.draw.line(scr, COLORS["black"], (560,320),(560,800),2)
        
        font = pygame.font.Font(None, 72)
        text = font.render(self.prices_and_values[self.index]["name"], True, COLORS["black"])
        scr.blit(text, (616,345))
        
        font2 = pygame.font.Font(None, 50)
        text = font2.render("Cost: ",True,COLORS["black"])
        scr.blit(text, (626,386))
        text = font2.render("Next upgrade: ", True, COLORS["black"])
        
        font3 = pygame.font.Font(None, 40)
        
        textwidth = 664
        textlist = [""]
        for x in self.prices_and_values[self.index]["desc"].split(" "):
            if font3.size(textlist[-1]+" "+x)[0] > textwidth:
                textlist.append("")
            textlist[-1] += x+" "
            
        textlist.append("")
        textlist.append("")
        for x in self.prices_and_values[self.index]["flav"].split(" "):
            if font3.size(textlist[-1]+" "+x)[0] > textwidth:
                textlist.append("")
            textlist[-1] += x+" "
        
        for i,x in enumerate(textlist):
            text = font3.render(x, True, COLORS["black"])
            scr.blit(text, (616, 420+i*30))
