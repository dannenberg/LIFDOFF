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
        
        
        
        for x in (self.tree_one, self.tree_two, self.tree_three):
            x.fill((0xCC,0xCC,0xFF))
        self.info_sfc.fill((0x99,0xCC,0xCC))
        
        self.setup()
        
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
        
        font = pygame.font.Font(None, 50)
        font2 = pygame.font.Font(None, 40)        
        
        shopButton = font.render("Shop", True, COLORS["black"])
        self.info_sfc.blit(shopButton, (0+33, SCREEN_HEIGHT*5/6+20))    # TODO: fix these magic nums
        backButton = font.render("Back", True, COLORS["black"])
        self.info_sfc.blit(backButton, (SCREEN_WIDTH/8 + 33, SCREEN_HEIGHT*5/6+20))
        
        def click_back(someone, mpos):
            self.main.change_screen("game")
        
        self.clickbox.append((SCREEN_WIDTH*7/8, SCREEN_HEIGHT*5/6, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), click_back)