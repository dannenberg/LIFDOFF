import pygame
from screen import Screen
from constants import COLORS
from mousehitbox import MouseHitboxes

class IntroMovie(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.introtheme = pygame.mixer.music.load("../sound/lifdoff.ogg")
        self.logo = pygame.image.load("../img/lifdofflogo.png")
        self.overlay = pygame.Surface((1280, 800), pygame.SRCALPHA)
        self.overlay.fill((0xFF, 0xFF, 0xFF, 192))
        self.yloc = 500-62
        self.playing = 0

    def display(self, scr):
        Screen.display(self, scr)
        if self.playing == 0:
            self.playing = 1
            pygame.mixer.music.play()
        scr.fill(COLORS["white"])

        self.overlay.fill((0xFF, 0xFF, 0xFF, int(2.55*abs((self.yloc+62-400)))))

        scr.blit(self.logo, (300, self.yloc))
        scr.blit(self.overlay, (0, 0))
        self.yloc -= .75
        if self.yloc < 300-62:
            pygame.mixer.music.stop()
            self.main.change_screen("main")
