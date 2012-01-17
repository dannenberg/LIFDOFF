from unit import UnitFactory
from screens.screen import Screen
from constants import PANEL_SQUARE_SIZE, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT, COLORS
import pygame

class OffensePanel:
    def __init__(self, w, h):
        self.surface = pygame.Surface((w*PANEL_SQUARE_SIZE, h*PANEL_SQUARE_SIZE)) 
        self._w = w
        self._h = h
        self.cells = [[None for _ in xrange(h)] for _ in xrange(w)]    # no units at start
        self.selected = None
        self.tileset = pygame.image.load("../img/enemy_tileset.png")
        self.image_dict = {UnitFactory.TADPOLE:0, UnitFactory.YELLOW_SUB:3}
    
    def on_click(self, (x, y)):
        if self.cells[x][y] != None:
            if self.selected == (x,y):
                self.selected = None
                return None
            else:
                self.selected = (x, y)
                return self.cells[x][y]

    def add_unit(self, unitid):
        for x in xrange(self._w):
            for y in xrange(self._h):
                if self.cells[y][x] == None:
                    self.cells[y][x] = unitid
                    return

    def draw_panel(self):
        pygame.draw.rect(self.surface, COLORS["attackbut"], (0, 0, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT))
        for x in xrange(0, OFFENSIVE_PANEL_WIDTH, PANEL_SQUARE_SIZE):  # vert lines
            pygame.draw.line(self.surface, COLORS["lines"], (x, 0), (x, OFFENSIVE_PANEL_HEIGHT), 2)
        for y in xrange(0, OFFENSIVE_PANEL_HEIGHT, PANEL_SQUARE_SIZE):  # hori lines
            pygame.draw.line(self.surface, COLORS["lines"], (0, y), (OFFENSIVE_PANEL_WIDTH, y), 2)
        for i,x in enumerate(self.cells):
            for j,y in enumerate(x):
                if y != None:
                    self.surface.blit(self.tileset, (i*PANEL_SQUARE_SIZE, j*PANEL_SQUARE_SIZE), ((self.image_dict[y]*PANEL_SQUARE_SIZE, 0), (PANEL_SQUARE_SIZE, PANEL_SQUARE_SIZE)))

