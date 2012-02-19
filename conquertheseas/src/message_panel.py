import pygame
from constants import COLORS

TRANSPARENT = (0xFF,0,0xFF)
class MessagePanel:
    def __init__(self, (widthpx, heightpx), heightln, font=None):
        """ Takes the width and height in pixels, the height in number of lines,
        and a font to render all the fonts in """
        if font is None:
            self.font = pygame.font.Font(None, 40)
        else:
            self.font = font
        self.height = self.font.get_linesize()
        print self.height*heightln
        self.surface = pygame.Surface((widthpx, (self.height*heightln)))
        self.surface.set_colorkey(TRANSPARENT)
        self.surface.fill(TRANSPARENT)
        self._juggler = pygame.Surface((widthpx, (self.height*heightln)))
        self._juggler.set_colorkey(TRANSPARENT)
        self._juggler.fill(TRANSPARENT)
        self.view = pygame.Surface((widthpx, heightpx))
        self.view.set_colorkey(TRANSPARENT)
        self.view.fill(TRANSPARENT)
        
    def message(self, by, msg):
        self._juggler.fill(TRANSPARENT)
        height = self.height    # TODO: make it based on message length
        self._juggler.blit(self.surface, (0,-height))
        self.surface.fill(TRANSPARENT)
        self.surface.blit(self._juggler, (0,0))
        text = self.font.render(msg, True, COLORS["white"])
        self.surface.blit(text, (0,self.surface.get_height()-self.height))
        self.view.fill(TRANSPARENT)
        self.view.blit(self.surface, (0, self.view.get_height()-self.surface.get_height()))    # TODO: maybe make it keep track of scroll (instead of scrolling to the bottom)
