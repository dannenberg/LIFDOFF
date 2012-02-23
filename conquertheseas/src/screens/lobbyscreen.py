from string import lowercase
import threading
import urllib, urllib2
from constants import COLORS
from screens.screen import Screen
from message_panel import MessagePanel
from bg_waves import Waves
import pygame
class LobbyScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.player_colors = [(0xFF,0,0), (0,0xFF,0), (0xFF,0,0xFF), (0xFF,0xFF,0), (0,0xFF,0xFF), (0xFF, 180, 0), (180,0,0xFF), (0, 0xFF, 100), (0xFF,0xCC,0xCC), (0xCC,0xCC,0xFF)]
        self.color_pick = 0
        self.largefont = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 30)
        
        self.waves = Waves()
        
        self.players_panel = pygame.Surface((496,578), pygame.SRCALPHA)
        self.players_panel.fill((0, 0, 0, 128))
        self.player_surfs = []
        for _ in xrange(10):
            self.player_surfs.append(pygame.Surface((474,48), pygame.SRCALPHA))
        self.redraw_players()
        self.chat_panel = pygame.Surface((696, 578), pygame.SRCALPHA)
        self.chat_panel.fill((0,0,0,128))
        #pygame.draw.rect(self.chat_panel
        self.textbox = pygame.Surface((1820,30), pygame.SRCALPHA)
        self.textbox.fill((0,0,0,64))
        self.base_panel = pygame.Surface((1215, 96), pygame.SRCALPHA)
        self.base_panel.fill((0,0,0,128))
        txt_leave_lobby = self.largefont.render("Leave Lobby", True, COLORS["white"])
        self.button_leave_lobby = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_leave_lobby.fill((0,0,0,64))
        self.button_leave_lobby.blit(txt_leave_lobby, (15,15))
        self.base_panel.blit(self.button_leave_lobby, (10,10))
        
        def get_ip():
            try:
                ip = urllib.urlopen('http://whatismyip.org').read()    # yes, this is actually the accepted way to do this
                txt_ip = self.largefont.render(ip, True, COLORS["white"])
                self.base_panel.blit(txt_ip, (450, 25))
                def copy_ip(scr, mpos):
                    pygame.scrap.init()
                    pygame.scrap.put(pygame.SCRAP_TEXT, ip)
                self.clickbox.append((476,706,txt_ip.get_width(), txt_ip.get_height()), copy_ip)
            except (urllib2.URLError, urllib2.HTTPError):
                print "Error fetching IP"
        threading.Thread(target=get_ip).start()
        
        self.button_start = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_start.fill((0,0,0,64))
        txt_start_game = self.largefont.render("Start Game", True, COLORS["white"])
        self.button_start.blit(txt_start_game, (30,15))
        self.base_panel.blit(self.button_start, (870,10))
        
        self.text_input = ""
        self.msgpanel = MessagePanel((652,509), 23, self.font)
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
        self.waves.display(screen, False)
        screen.blit(self.players_panel, (26,38))
        screen.blit(self.chat_panel, (545, 38))
        screen.blit(self.textbox, (565,577), (min(self.textbox.get_width()-582, max(0,(self.font.size(self.text_input)[0])-582+10)),0,582,30))
        screen.blit(self.base_panel, (26, 681))
        screen.blit(self.msgpanel.view, (566,63))
        
    def message(self):
        if self.text_input:
            self.msgpanel.message("Orez", self.text_input, self.player_colors[self.color_pick])
            self.text_input = ""
        
    def notify_key(self, inkey):
        if inkey.key == pygame.K_BACKSPACE:
            self.text_input = self.text_input[:-1]
        elif inkey.key == pygame.K_RETURN or inkey.key == pygame.K_KP_ENTER:
            self.message()
        elif inkey.unicode and self.font.size(self.text_input+inkey.unicode)[0] <= self.textbox.get_width()-10:
            self.text_input += inkey.unicode
        else:
            return  # if none of these things happened, no need to redraw
        self.textbox.fill((0,0,0,64))
        txt = self.font.render(self.text_input, True, COLORS["white"])
        self.textbox.blit(txt, (5,5))
