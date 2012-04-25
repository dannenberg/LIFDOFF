import pygame
from screen import Screen

ARROW_OFFSET = 400
class TutorialScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        arrows = pygame.image.load("../img/tut_arrows.png")
        self.arrows = pygame.Surface((arrows.get_width()*2, arrows.get_height()), pygame.SRCALPHA)
        paths = ["cthulhu_highres","crab_highres","mermaid_highres"]
        self.images = [pygame.image.load("../img/"+p+".png") for p in paths]
        self.basebar = pygame.Surface((1280,100))
        self.basebar.fill((0x44,)*3)
        self.basebar.fill((0x22,)*3, (1185,55,95,45))
        pygame.draw.rect(self.basebar, (0xFF,0,0), (0,0,1280,100), 3)
        pygame.draw.rect(self.basebar, (0xFF,0,0), (0,5,1280,95), 3)
        self.basebar.blit(pygame.font.Font(None,50).render("Back",True,(0xFF,)*3), (1190,60))
        self.basedisp = pygame.Surface((1280,100), pygame.SRCALPHA)
        self.arrows.blit(arrows, (0,0))
        self.arrows.blit(pygame.transform.flip(arrows, True, False), (arrows.get_width(),0))
        self.index = 0
        self.font = pygame.font.Font(None, 100)
        self.redraw_basedisp()
        
        def go(amt):
            def anon(mpos):
                if 0<=self.index+amt<len(self.images):
                    self.index += amt
                    self.redraw_basedisp()
            return anon
        
        def back(mpos):
            self.main.change_screen("main")
        
        self.clickbox.append((ARROW_OFFSET, 710, self.arrows.get_width()/4, self.arrows.get_height()), go(-1))
        self.clickbox.append((1280-ARROW_OFFSET-self.arrows.get_width()/4, 710, self.arrows.get_width()/4, self.arrows.get_height()), go(1))
        self.clickbox.append((1185,755,95,45), back)
        
    def redraw_basedisp(self):
        words = self.font.render(str(self.index+1), True, (0xFF,)*3)
        centered = (1280-words.get_width())/2
        self.basedisp.fill((0,0,0,0))
        self.basedisp.blit(words, (centered,20))
        off = 0
        if self.index:  # != 0
            off = 1
        self.basedisp.blit(self.arrows, (ARROW_OFFSET, 10), ((self.arrows.get_width()/4)*off,0, self.arrows.get_width()/4, self.arrows.get_height()))
        
        off = 2
        if self.index == len(self.images)-1:
            off = 3
        self.basedisp.blit(self.arrows, (1280-ARROW_OFFSET-self.arrows.get_width()/4, 10), ((self.arrows.get_width()/4)*off,0, self.arrows.get_width()/4, self.arrows.get_height()))
        
    def display(self, screen):
        Screen.display(self, screen)
        screen.blit(self.images[self.index], (0,0))
        screen.blit(self.basebar, (0,700))
        screen.blit(self.basedisp, (0,700))
