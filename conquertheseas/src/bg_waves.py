from constants import COLORS
import math
import pygame

class Waves(object):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Waves, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.water_level = 0 #defines the height of the water in the background
        self.water_range = 16 #how much the water level fluctuates
        
        self.font = pygame.font.Font(None, 170) #title text defined and two colored versions created
        self.text = self.font.render("CONQUER THE SEAS", True, COLORS["black"])
        self.whitetext = self.font.render("CONQUER THE SEAS", True, COLORS["submergedt"])
        
    def display(self, screen, display_text=True):
        self.water_level = (self.water_level + (math.pi / 180)) % (math.pi * 2) #movement in rads for waterlevel (since it is based on sin)
        modifier = int(math.sin(self.water_level) * self.water_range) #actual change
        
        #draws the sky, water, and text
        screen.fill(COLORS["sky"])
        water = pygame.Surface((1280, 700 - modifier))
        water.fill(COLORS["water"])
        if display_text:
            screen.blit(self.text, (20, 50))
            water.blit(self.whitetext, (20,  -50 - modifier))
        screen.blit(water, (0, modifier + 100))
