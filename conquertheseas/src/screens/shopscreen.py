import pygame
from unit import UnitFactory
from screen import Screen
from constants import *
from mousehitbox import MouseHitboxes

class ShopScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.prices_and_values = [{"name":"Mine","desc":"Basic nautical weaponry, drop it off and hope for the best. These ones have seen better days.","flav":"During the American Civil War, hundreds of these mines were laid along various rivers. After the war, they were collected by legitimate businesses and put on the market, although almost no one has been crazy enough to buy them.", "highres":pygame.image.load("../img/mine_highres.png"), "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.MINE},
                                  {"name":"Angry Fish","desc":"This angry fish will start moving slowly, but will charge forward when it sees an enemy ship.","flav":"Angry Fish were created by mad scientists, in order to stop those who would oppose them. Unfortunately, mad scientists do not have any allies, so Angry Fish have been conditioned to attack all ships.", "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.ANGRYFISH, "highres":pygame.image.load("../img/angryfish_highres.png")},
                                  {"name":"Mermaid","desc":"Mermaids are smarter than the average bear, and clearly more intelligent than the fish and mines you've been hiring thusfar. They'll actively seek out their prey!","flav":"In the past mermaids have not been seen as intimidating, but these ones have knives!", "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.MERMAID, "highres":pygame.image.load("../img/mermaid_highres.png")},
                                  {"name":"Squiddle","desc":"Beware of this tanglebuddy's entangling tentacles!","flav":"Squiddles are the My Little Pony of the sea. They spread their joy and love to all that they see, whether they like it or not.","highres":pygame.image.load("../img/squiddle_highres.png"), "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.SQUIDDLE},
                                  {"name":"Crab","desc":"Even if everyone had the same towel at the beach, this wouldn't be a rock OR a lobster: it's a crab!","flav":"Crabs move along the sea floor and pinch anyone who gets too close.","highres":pygame.image.load("../img/crab_highres.png"), "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.CRAB},
                                 #{"name":"Pufferfish","desc":"The pufferfish will expand and contract its pointy quills. Timing is key!","flav":"Under normal circumstances, the puffer fish will puff out its spines when it is frightened or threatened. So let's just say that just offscreen there's something really scary that shows up every so often.", "rank":0, "prices":[(0,""),(10,"")], "token":UnitFactory.MINE},
                                  {"name":"Cthulhu","desc":"The Deep One. Walks slowly across the screen, but decimates everything in its path.","flav":"Did you know you could buy Cthulhus? Seriously. You can just go to the store and be like \"Hey do you have any Cthulhus for sale?\" and they'd be all \"Oh yeah of course we can't get rid of the damn (ha ha) things!\"", "highres":pygame.image.load("../img/cthulhu_highres.png"), "rank":0, "prices":[(666,""),(10,"")], "token":UnitFactory.MINE}]
        self.index = None
        self.icons = pygame.image.load("../img/shop_imgs.png")
        def go_back(mpos):
            self.main.change_screen("game")
        self.clickbox.append((SHOP_BACK_X,SHOP_BACK_Y,SHOP_BACK_W,SHOP_BACK_H), go_back)
        def which(ik):
            def select(mpos):
                try:
                    self.prices_and_values[ik]
                except IndexError:
                    return
                self.index = ik
                self.draw_words()
            return select
        for y in xrange(SHOP_PANEL_Y):
            for i in xrange(SHOP_PANEL_X):
                self.clickbox.append((i*SHOP_GRID_SIZE, y*SHOP_GRID_SIZE, SHOP_GRID_SIZE, SHOP_GRID_SIZE), which(y*SHOP_PANEL_X+i))
                
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.words = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        def purchase(mpos):
            try:
                if self.index is None:
                    return
                x = self.prices_and_values[self.index]
                print len(x["prices"]), x["rank"]
                if len(x["prices"]) <= x["rank"]:
                    return
            except ValueError:
                return
            if self.main.screens["game"].my_board.gold >= x["prices"][x["rank"]][0]:  # TODO: MONEY
                self.main.screens["game"].my_board.gold -= x["prices"][x["rank"]][0]
                self.main.screens["game"].to_server.append("BUY " + str(self.index))
                if not x["rank"]:
                    self.main.screens["game"].offense_panel.add_unit(x["token"])
                x["rank"] += 1
                self.draw_words()
                # TODO: apply upgrades?
                
        self.clickbox.append((SHOP_PURCH_X, SHOP_PURCH_Y, SHOP_PURCH_W, SHOP_PURCH_H), purchase)
        
        self.background.fill(COLORS["shopbg"])
        pygame.draw.rect(self.background, COLORS["sand"], (0,0,SCREEN_WIDTH,SHOP_PANEL_H))
        for y in xrange(SHOP_PANEL_Y):
            for i in xrange(SHOP_PANEL_X):
                self.background.blit(self.icons, (i*SHOP_GRID_SIZE, y*SHOP_GRID_SIZE), (i*SHOP_GRID_SIZE+y*SCREEN_WIDTH, 0, SHOP_GRID_SIZE, SHOP_GRID_SIZE))
        pygame.draw.rect(self.background, COLORS["water"], (0,SHOP_PANEL_H,SHOP_IMG_BORDER,SCREEN_HEIGHT-SHOP_PANEL_H))
        for x in xrange(-1,SHOP_GRID_SIZE*SHOP_PANEL_Y+1,SHOP_GRID_SIZE):
            pygame.draw.line(self.background, COLORS["black"], (0,x),(SCREEN_WIDTH,x),2)
        for x in xrange(-1,SCREEN_WIDTH+1,SHOP_GRID_SIZE):
            pygame.draw.line(self.background, COLORS["black"], (x,0),(x,SHOP_PANEL_H),2)
        pygame.draw.line(self.background, COLORS["black"], (SHOP_IMG_BORDER,SHOP_PANEL_H),(SHOP_IMG_BORDER,SCREEN_HEIGHT),2)
        
        pygame.draw.rect(self.background, (0xC0, 0xC0, 0xC0), (SHOP_BACK_X, SHOP_BACK_Y, SHOP_BACK_W, SHOP_BACK_H))
        pygame.draw.rect(self.background, COLORS["black"], (SHOP_BACK_X, SHOP_BACK_Y, SHOP_BACK_W, SHOP_BACK_H), 2)
        
        font = pygame.font.Font(None, 60)
        text = font.render("Back", True, COLORS["black"])
        self.background.blit(text, (SHOP_BACK_X+45,SHOP_BACK_Y+7))
    
    def draw_words(self):
        self.words.fill((0,0,0,0))
        font = pygame.font.Font(None, 72)
        text = font.render(self.prices_and_values[self.index]["name"], True, COLORS["black"])
        self.words.blit(text, (SHOP_TITLE_X,SHOP_TITLE_Y))
        
        font2 = pygame.font.Font(None, 50)
        font3 = pygame.font.Font(None, 40)
        
        if len(self.prices_and_values[self.index]["prices"]) > self.prices_and_values[self.index]["rank"]:
            text = font2.render("Cost: "+str(self.prices_and_values[self.index]["prices"][self.prices_and_values[self.index]["rank"]][0]),True,COLORS["black"])
            self.words.blit(text, (SHOP_COST_X,SHOP_COST_Y))
            pygame.draw.rect(self.words, (0xC0,0xC0,0xC0), (SHOP_PURCH_X,SHOP_PURCH_Y,SHOP_PURCH_W,SHOP_PURCH_H))
            pygame.draw.rect(self.words, COLORS["black"], (SHOP_PURCH_X,SHOP_PURCH_Y,SHOP_PURCH_W,SHOP_PURCH_H), 2)
            
            if self.main.screens["game"].my_board.gold >= self.prices_and_values[self.index]["prices"][self.prices_and_values[self.index]["rank"]][0]: 
                text = font3.render("Purchase",True,COLORS["black"])
            else:
                text = font3.render("Purchase",True,COLORS["gray"])
            self.words.blit(text, (SHOP_PURCH_X+7,SHOP_PURCH_Y+5))
        
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
            self.words.blit(text, (SHOP_TITLE_X, SHOP_TEXT_Y+i*SHOP_TEXT_SPACING))
            
        if "highres" in self.prices_and_values[self.index]:
            self.words.blit(self.prices_and_values[self.index]["highres"], (0,SHOP_GRID_SIZE*SHOP_PANEL_Y))
        
    def display(self, screen):
        Screen.display(self, screen)
        
        screen.blit(self.background, (0,0))
        screen.blit(self.words, (0,0))
