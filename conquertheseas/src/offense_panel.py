from unit import UnitFactory
from screens.screen import Screen
import pygame

class Offense_Panel:
    def __init__(self, w, h):
        self.surface = pygame.Surface((w*67, h*67)) # TODO make a const for cell size
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # no units at start
        self.selected = None
        self.tileset = pygame.image.load("../img/enemy_tileset.png")
        self.image_dict = {UnitFactory.TADPOLE:0}
    
    def on_click(self, (x, y)):
        if self.cells[x][y] != None:
            if self.selected == (x,y):
                self.selected = None
                return None
            else:
                self.selected = (x, y)
                return self.cells[x][y]

    def add_unit(self, unitid):
        for y in xrange(self._h):
            for x in xrange(self._w):
                if self.cells[y][x] == None:
                    self.cells[y][x] = unitid
                    return

    def draw_panel(self):
        pygame.draw.rect(self.surface, Screen.color["attackbut"], (0, 0, 201, 335))
        for x in xrange(0, 201, 67):  # vert lines
            pygame.draw.line(self.surface, Screen.color["lines"], (x, 0), (x, 395), 2)
        for x in xrange(0, 400, 67):  # hori lines
            pygame.draw.line(self.surface, Screen.color["lines"], (0, x), (201, x), 2)
        for i,x in enumerate(self.cells):
            for j,y in enumerate(x):
                if y != None:
                    self.surface.blit(self.tileset, (i*67, j*67), ((self.image_dict[y]*67, 0), (67, 67)))

