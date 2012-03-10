import pygame
from screen import Screen
from constants import COLORS
from mousehitbox import MouseHitboxes

class ShopScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.prices_and_values = [{"name":"Mine","desc":"Basic nautical weaponry, drop it off and hope for the best. These ones have seen better days.","flav":"During the American Civil War, hundreds of these mines were laid along various rivers. After the war, they were collected by legitimate businesses and put on the market, although almost no one has been crazy enough to buy them.", "highres":pygame.image.load("../img/mine_highres.png"), "rank":0, "prices":[(0,""),(10,"")]},
                                  {"name":"Angry Fish","desc":"This angry fish will start moving slowly, but will charge forward when it sees an enemy ship.","flav":"Angry Fish were created by mad scientists, in order to stop those who would oppose them. Unfortunately, mad scientists do not have any allies, so Angry Fish have been conditioned to attack all ships.", "rank":0, "prices":[(0,""),(10,"")]},
                                  {"name":"Mermaid","desc":"Mermaids are smarter than the average bear, and clearly more intelligent than the fish and mines you've been hiring thusfar. They'll actively seek out their prey!","flav":"In the past mermaids have not been seen as intimidating, but these ones have knives!", "rank":0, "prices":[(0,""),(10,"")]},
                                  {"name":"Squiddle","desc":"Beware of this tanglebuddy's entangling tentacles!","flav":"Squiddles are the My Little Pony of the sea. They spread their joy and love to all that they see, whether they like it or not.","highres":pygame.image.load("../img/squiddle_highres.png"), "rank":0, "prices":[(0,""),(10,"")]},
                                  {"name":"Pufferfish","desc":"The pufferfish will expand and contract its pointy quills. Timing is key!","flav":"Under normal circumstances, the puffer fish will puff out its spines when it is frightened or threatened. So let's just say that just offscreen there's something really scary that shows up every so often.", "rank":0, "prices":[(0,""),(10,"")]},
        {"name":"Cthulhu","desc":"The Deep One. Walks slowly across the screen, but decimates everything in its path.","flav":"Did you know you could buy Cthulhus? Seriously. You can just go to the store and be like \"Hey do you have any Cthulhus for sale?\" and they'd be all \"Oh yeah of course we can't get rid of the damn (ha ha) things!\"", "highres":pygame.image.load("../img/cthulhu_highres.png"), "rank":0, "prices":[(0,""),(10,"")]}]
        self.index = None
        self.icons = pygame.image.load("../img/shop_imgs.png")
        def go_back(scr, mpos):
            self.main.change_screen("game")
        self.clickbox.append((1100,750,180,50), go_back)
        def which(ik):
            def select(scr, mpos):
                try:
                    self.prices_and_values[ik]
                except IndexError:
                    return
                self.index = ik
                self.draw_words()
            return select
        for y in xrange(2):
            for i in xrange(8):
                self.clickbox.append((i*160, y*160, 160, 160), which(y*8+i))
                
        self.background = pygame.Surface((1280, 800), pygame.SRCALPHA)
        self.words = pygame.Surface((1280, 800), pygame.SRCALPHA)
        
        def purchase(scr, mpos):
            money = 6000000000000
            try:
                if self.index is None:
                    return
                x = self.prices_and_values[self.index]
                print len(x["prices"]), x["rank"]
                if len(x["prices"]) <= x["rank"]:
                    return
            except ValueError:
                return
            if money >= x["prices"][x["rank"]][0]:  # TODO: MONEY
                money -= x["prices"][x["rank"]][0]
                x["rank"] += 1
                self.draw_words()
                # TODO: apply upgrades?
                
        self.clickbox.append((1125,340,145,36), purchase)
        
        self.background.fill(COLORS["shopbg"])
        pygame.draw.rect(self.background, COLORS["sand"], (0,0,1280,320))
        for y in xrange(2):
            for i in xrange(8):
                self.background.blit(self.icons, (i*160, y*160), (i*160+y*1280, 0, 160, 160))
        pygame.draw.rect(self.background, COLORS["water"], (0,320,560,480))
        for x in xrange(-1,321,160):
            pygame.draw.line(self.background, COLORS["black"], (0,x),(1280,x),2)
        for x in xrange(-1,1281,160):
            pygame.draw.line(self.background, COLORS["black"], (x,0),(x,320),2)
        pygame.draw.line(self.background, COLORS["black"], (560,320),(560,800),2)
    
    def draw_words(self):
        self.words.fill((0,0,0,0))
        font = pygame.font.Font(None, 72)
        text = font.render(self.prices_and_values[self.index]["name"], True, COLORS["black"])
        self.words.blit(text, (616,345))
        
        font2 = pygame.font.Font(None, 50)
        font3 = pygame.font.Font(None, 40)
        
        if len(self.prices_and_values[self.index]["prices"]) > self.prices_and_values[self.index]["rank"]:
            text = font2.render("Cost: "+str(self.prices_and_values[self.index]["prices"][self.prices_and_values[self.index]["rank"]][0]),True,COLORS["black"])
            self.words.blit(text, (626,386))
            pygame.draw.rect(self.words, (0xC0,0xC0,0xC0), (1125,340,145,36))
            pygame.draw.rect(self.words, COLORS["black"], (1125,340,145,36), 3)
            
            text = font3.render("Purchase",True,COLORS["black"])
            self.words.blit(text, (1125+7,340+5))
        
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
            self.words.blit(text, (616, 420+i*30))
            
        if "highres" in self.prices_and_values[self.index]:
            self.words.blit(self.prices_and_values[self.index]["highres"], (0,320))
        
    def display(self, scr):
        Screen.display(self, scr)
        
        scr.blit(self.background, (0,0))
        scr.blit(self.words, (0,0))
