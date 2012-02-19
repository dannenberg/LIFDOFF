import pygame
from constants import COLORS

TRANSPARENT = (0xFF,0,0xFF,0)
class MessagePanel:
    def __init__(self, (widthpx, heightpx), heightln, font=None):
        """ Takes the width and height in pixels, the height in number of lines,
        and a font to render all the fonts in """
        if font is None:
            self.font = pygame.font.Font(None, 40)
        else:
            self.font = font
        self.height = self.font.get_linesize()
        self.surface = pygame.Surface((widthpx, (self.height*heightln)), pygame.SRCALPHA)
        self.surface.fill(TRANSPARENT)
        self._juggler = pygame.Surface((widthpx, (self.height*heightln)), pygame.SRCALPHA)
        self._juggler.fill(TRANSPARENT)
        self.view = pygame.Surface((widthpx, heightpx), pygame.SRCALPHA)
        self.view.fill(TRANSPARENT)
        
    def message(self, by, msg, color=(0xFF, 0xFF, 0xFF)):
        name = self.font.render(by+": ", True, color)
        lines = self.split_message(msg, name.get_width())
        bunp = -len(lines)*self.height
        self._juggler.fill(TRANSPARENT)
        self._juggler.blit(self.surface, (0, bunp))
        self.surface.fill(TRANSPARENT)
        self.surface.blit(self._juggler, (0,0))
        
        self._juggler.fill(TRANSPARENT)
        self._juggler.blit(name, (0,0))
        for i,x in enumerate(lines):
            text = self.font.render(x, True, COLORS["white"])
            self._juggler.blit(text, (0 if i else name.get_width(), i*self.height))
        self.surface.blit(self._juggler, (0, self.surface.get_height()+bunp))
        
        self.view.fill(TRANSPARENT)
        self.view.blit(self.surface, (0, self.view.get_height()-self.surface.get_height()))    # TODO: maybe make it keep track of scroll (instead of scrolling to the bottom)
        
    def split_message(self, msg, wid):
        toR = []
        screenwid = self.view.get_width()
        msg = msg.split(' ')
        line = ""
        while msg:
            if self.font.size(msg[0])[0]+wid > screenwid:  # nextline
                wid = 0
                toR += [line]
                line = ""
            wid += self.font.size(msg[0]+" ")[0]
            line += msg[0]+" "
            msg = msg[1:]
        toR += [line]
        return toR
