import pygame
from screen import Screen

class UpgradeScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.tree_one = pygame.Surface((320, 800))
        self.tree_two = pygame.Surface((320, 800))
        self.tree_three = pygame.Surface((320, 800))
        self.info_sfc = pygame.Surface((320, 800))
        
        for x in (self.tree_one, self.tree_two, self.tree_three):
            x.fill((0xCC,0xCC,0xFF))
        self.info_sfc.fill((0x99,0xCC,0xCC))
        
    def display(self, screen):
        Screen.display(self, screen)
        for i,x in enumerate((self.tree_one, self.tree_two, self.tree_three, self.info_sfc)):
            screen.blit(x, (320*i, 0))
            pygame.draw.line(screen, (0,0,0), (i*320,0), (i*320, 800), 2)
