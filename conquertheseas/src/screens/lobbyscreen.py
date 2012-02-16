import urllib
from constants import COLORS
from screens.screen import Screen
import pygame
class LobbyScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.players_panel = pygame.Surface((496,578), pygame.SRCALPHA)
        self.players_panel.fill((0, 0, 0, 128))
        self.player_surfs = []
        for _ in xrange(10):
            self.player_surfs.append(pygame.Surface((474,48), pygame.SRCALPHA))
        self.redraw_players()
        self.chat_panel = pygame.Surface((696, 578), pygame.SRCALPHA)
        self.chat_panel.fill((0,0,0,128))
        textbox = pygame.Surface((582,30), pygame.SRCALPHA)
        textbox.fill((0,0,0,64))
        self.chat_panel.blit(textbox, (20,539))
        chatbox = pygame.Surface((652, 509), pygame.SRCALPHA)
        chatbox.fill((0,0,0,64))
        self.chat_panel.blit(chatbox, (20,23))
        self.base_panel = pygame.Surface((1215, 96), pygame.SRCALPHA)
        self.base_panel.fill((0,0,0,128))
        self.font = pygame.font.Font(None, 70)
        txt_leave_lobby = self.font.render("Leave Lobby", True, COLORS["white"])
        self.button_leave_lobby = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_leave_lobby.fill((0,0,0,64))
        self.button_leave_lobby.blit(txt_leave_lobby, (15,15))
        self.base_panel.blit(self.button_leave_lobby, (10,10))
        self.ip = urllib.urlopen('http://whatismyip.org').read()    # yes, this is actually the accepted way to do this
        txt_ip = self.font.render(self.ip, True, COLORS["white"])
        self.base_panel.blit(txt_ip, (450, 25))
        self.button_start = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_start.fill((0,0,0,64))
        txt_start_game = self.font.render("Start Game", True, COLORS["white"])
        self.button_start.blit(txt_start_game, (30,15))
        self.base_panel.blit(self.button_start, (870,10))
        
        self.startable = False
        def to_main(scr, mpos):
            self.main.change_screen("main")
        self.clickbox.append((37,692,329,74), to_main)
    
    def redraw_players(self):
        self.players_panel.fill((0, 0, 0, 128))
        for i,x in enumerate(self.player_surfs):
            x.fill((0,0,0,64))
            pygame.draw.rect(x, (0,0,0,0), (48,0,12,48))
            self.players_panel.blit(x, (10,37+i*54))
    
    def display(self, screen):
        Screen.display(self, screen)
        screen.fill(COLORS["water"])
        screen.blit(self.players_panel, (26,38))
        screen.blit(self.chat_panel, (545, 38))
        screen.blit(self.base_panel, (26, 681))
        
