import pygame
from constants import *
from screen import Screen

class UpgradeScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.tree_one = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.tree_two = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.tree_three = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.info_sfc = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        
        self.upgrades = [[{"First":{"row":0, "order":1, "next":["Second","Third"], "cost":5},
                           "Second":{"row":1, "order":1, "next":["Ultimate"], "cost":10},
                           "Third":{"row":1, "order":2, "next":["Ultimate"], "cost":15},
                           "Ultimate":{"row":2,"order":1, "next":[], "cost":30}},
                          {},{}],[{},{},{}],[{},{},{}]]
        self.init_upgrades()
        
        for x in (self.tree_one, self.tree_two, self.tree_three):
            x.fill((0xCC,0xCC,0xFF))
        self.info_sfc.fill((0x99,0xCC,0xCC))
        
        self.setup()
        
    def init_upgrades(self):
        rows = {}
        maxrow = 0
        for s,ship in enumerate(self.upgrades):
            for tree in ship:
                for upgrade in tree:    # find how many there are in each row
                    if tree[upgrade]["row"] not in rows:
                        rows[tree[upgrade]["row"]] = 1  # intentional
                    rows[tree[upgrade]["row"]] += 1
                    maxrow = max(maxrow, tree[upgrade]["row"]+2)
                for upgrade in tree:    # actually assign them to locations
                    tree[upgrade]["x"] = SCREEN_WIDTH*tree[upgrade]["order"]/4/rows[tree[upgrade]["row"]]
                    tree[upgrade]["y"] = SCREEN_HEIGHT*(tree[upgrade]["row"]+1)/maxrow
        
    def switch_ship(self, which):
        surfs = (self.tree_one, self.tree_two, self.tree_three)
        self.clickbox.clear(2)
        for t,tree in enumerate(self.upgrades[which]):
            for upgrade in tree:    # lines first
                for prereqs in tree[upgrade]["next"]:
                    pygame.draw.line(surfs[t], (0,0,0), (tree[upgrade]["x"],tree[upgrade]["y"]), (tree[prereqs]["x"],tree[prereqs]["y"]), 2)
            for upgrade in tree:
                rectloc = (tree[upgrade]["x"]-UPGRADE_ICON_SIZE/2, tree[upgrade]["y"]-UPGRADE_ICON_SIZE/2, UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE)
                pygame.draw.rect(surfs[t], (0xCC,0xCC,0xCC), rectloc)
                pygame.draw.rect(surfs[t], (0,0,0), rectloc, 2)
                def what(thef):
                    def onclick(scr, mpos):
                        print thef["cost"]
                    return onclick
                self.clickbox.append(rectloc, what(tree[upgrade]), z=2)
                
        
    def display(self, screen):
        Screen.display(self, screen)
        
        for i,x in enumerate((self.tree_one, self.tree_two, self.tree_three, self.info_sfc)):
            screen.blit(x, (SCREEN_WIDTH/4*i, 0))
            pygame.draw.line(screen, (0,0,0), (i*SCREEN_WIDTH/4,0), (i*SCREEN_WIDTH/4, SCREEN_HEIGHT), 2)
     
    def setup(self):
        # horizontal lines
        #pygame.draw.line(self.info_sfc, (0,0,0), (3*SCREEN_WIDTH/4, SCREEN_HEIGHT*2/3), (SCREEN_WIDTH, SCREEN_HEIGHT*2/3),2) # bottom third of right col
        pygame.draw.line(self.info_sfc, (0,0,0), (0, SCREEN_HEIGHT*2/3), (SCREEN_WIDTH, SCREEN_HEIGHT*2/3),2)
        pygame.draw.line(self.info_sfc, (0,0,0), (0, SCREEN_HEIGHT*5/6), (SCREEN_WIDTH, SCREEN_HEIGHT*5/6),2) # splits that bottom third in half
        pygame.draw.line(self.info_sfc, (0,0,0), (0, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH, SCREEN_HEIGHT*11/12),2) # splits the bottom 6th in half
        
        # vertical lines
        pygame.draw.line(self.info_sfc, (0,0,0), (SCREEN_WIDTH/8, SCREEN_HEIGHT*5/6), (SCREEN_WIDTH/8, SCREEN_HEIGHT*11/12),2) # splits shop/game in half
        pygame.draw.line(self.info_sfc, (0,0,0), (SCREEN_WIDTH/12, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH/12, SCREEN_HEIGHT),2)
        pygame.draw.line(self.info_sfc, (0,0,0), (SCREEN_WIDTH/6, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH/6, SCREEN_HEIGHT),2)
        
        
        # text 
        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 40)
        font3 = pygame.font.Font(None, 35)
        
        shopButton = font.render("Shop", True, COLORS["black"])
        self.info_sfc.blit(shopButton, (0+33, SCREEN_HEIGHT*5/6+15))    # TODO: fix these magic nums
        backButton = font.render("Back", True, COLORS["black"])
        self.info_sfc.blit(backButton, (SCREEN_WIDTH/8 + 33, SCREEN_HEIGHT*5/6+15))
        
        ship1Button = font2.render("Ship 1", True, COLORS["black"])
        ship2Button = font2.render("Ship 2", True, COLORS["black"])
        ship3Button = font2.render("Ship 3", True, COLORS["black"])
        self.info_sfc.blit(ship1Button, (0 + 10, SCREEN_HEIGHT*11/12 + 20))
        self.info_sfc.blit(ship2Button, (SCREEN_WIDTH/12 + 10, SCREEN_HEIGHT*11/12 + 20))
        self.info_sfc.blit(ship3Button, (SCREEN_WIDTH/6 + 10, SCREEN_HEIGHT*11/12 + 20))
        
        resourceOverview = font2.render("Resource Overview", True, COLORS["black"])
        self.info_sfc.blit(resourceOverview, (0 + 25, SCREEN_HEIGHT*2/3 + 5))
        dollars = font3.render("$$:", True, COLORS["black"])
        exp = font3.render("xp:", True, COLORS["black"])
        self.info_sfc.blit(dollars, (0 + 10, SCREEN_HEIGHT*2/3 + 45))
        self.info_sfc.blit(exp, (0 + 10, SCREEN_HEIGHT*2/3 + 85))
        # end of text
        
        def click_back(scr, mpos):
            self.main.change_screen("game")
        
        def click_shop(scr, mpos):
            self.main.change_screen("shop")
        
        def click_ship(which):
            def anon(scr, mpos):
                color = [0xCC, 0xCC, 0xCC]
                color[which] = 0xFF
                for x in (self.tree_one, self.tree_two, self.tree_three):
                    x.fill(color)
                self.switch_ship(which)
            return anon
        
        self.clickbox.append((SCREEN_WIDTH*6/8, SCREEN_HEIGHT*5/6, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), click_shop)
        self.clickbox.append((SCREEN_WIDTH*7/8, SCREEN_HEIGHT*5/6, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), click_back)
        
        self.clickbox.append((SCREEN_WIDTH*9/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(0))
        self.clickbox.append((SCREEN_WIDTH*10/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(1))
        self.clickbox.append((SCREEN_WIDTH*11/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(2))
        