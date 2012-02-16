from constants import COLORS
from screens.screen import Screen
import pygame
class LobbyScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.players_panel = pygame.Surface((496,578), pygame.SRCALPHA)
        self.players_panel.fill((0, 0, 0, 128))
        self.chat_panel = pygame.Surface((696, 578), pygame.SRCALPHA)
        self.chat_panel.fill((0,0,0,128))
        textbox = pygame.Surface((582,30), pygame.SRCALPHA)
        textbox.fill((0,0,0,128))
        self.chat_panel.blit(textbox, (20,539))
        chatbox = pygame.Surface((652, 509), pygame.SRCALPHA)
        chatbox.fill((0,0,0,128))
        self.chat_panel.blit(chatbox, (20,23))
        self.base_panel = pygame.Surface((1215, 96), pygame.SRCALPHA)
        self.base_panel.fill((0,0,0,128))
        self.startable = False
    
    def display(self, screen):
        Screen.display(self, screen)
        screen.fill(COLORS["water"])
        screen.blit(self.players_panel, (26,38))
        screen.blit(self.chat_panel, (545, 38))
        screen.blit(self.base_panel, (26, 681))
        
