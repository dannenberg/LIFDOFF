from screens.screen import Screen
from string import count
from constants import COLORS
from bg_waves import Waves
import networking
import pygame
class JoinScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.waves = Waves()
        self.inputblock = pygame.Surface((245,130), pygame.SRCALPHA)
        self.inputblock.fill((0,0,0,128))
        self.textbox = pygame.Surface((225, 30), pygame.SRCALPHA)
        self.textbox.fill((0,0,0,64))
        self.font = pygame.font.Font(None, 40)
        okbutton = pygame.Surface((80,40), pygame.SRCALPHA)
        okbutton.fill((0,0,0,64))
        oktxt = self.font.render("Join", True, COLORS["white"])
        okbutton.blit(oktxt, (10,8))
        backbutton = pygame.Surface((80,40), pygame.SRCALPHA)
        backbutton.fill((0,0,0,64))
        backtxt = self.font.render("Back", True, COLORS["white"])
        backbutton.blit(backtxt, (5,8))
        self.inputblock.blit(backbutton, (10,80))
        self.inputblock.blit(okbutton, (self.inputblock.get_width()-10-okbutton.get_width(),80))
        instruction = self.font.render("Server Address", True, COLORS["white"])
        self.inputblock.blit(instruction, (int(((self.inputblock.get_width()-instruction.get_width())/2.0)),10))
        self.ip = ""
        self.countdown = 0
        
        def go_back(scr, mpos):
            self.main.change_screen("main")
        self.clickbox.append((525,415, 80,40), go_back)
        self.clickbox.append((675,415, 80,40), self.connect_ip)
        
    def display(self, screen):
        Screen.display(self, screen)
        self.waves.display(screen)
        screen.blit(self.inputblock, (517,335))
        screen.blit(self.textbox, (527,380))
        if self.countdown > 0:
            self.countdown -= 1
            if not self.countdown:
                self.redraw_textbox(False)
        
    def connect_ip(self, scr=None, mpos=None):
        try:
            if count(self.ip, ".") == 3:
                int(self.ip[-1:])   # what we're "try"ing
                self.main.client = networking.Client(self.ip)
                self.main.client.start()
                self.main.change_screen("lobby") # TODO: yeah connecting things
                return
        except ValueError:
            pass
        self.redraw_textbox(True)
        
    def redraw_textbox(self, bad_input=False):
        if bad_input:
            self.countdown = 3
            self.textbox.fill((0xFF,0,0,128))
        else:
            self.textbox.fill((0,0,0,64))
        txt = self.font.render(self.ip, True, COLORS["white"])
        self.textbox.blit(txt, (2,2))
        
    def notify_key(self, inkey):
        if inkey.key == pygame.K_BACKSPACE:
            self.ip = self.ip[:-1]
        elif inkey.key == pygame.K_RETURN or inkey.key == pygame.K_KP_ENTER:
            self.connect_ip(self)
            return
        elif inkey.unicode:
            try:
                if inkey.unicode != ".":
                    int(inkey.unicode)
            except ValueError:
                self.redraw_textbox(True)
                return
            if inkey.unicode!="." and len(self.ip)>=3 and "." not in self.ip[-3:]:  # needs a . seperator
                if count(self.ip, ".")>=3:
                    return
                self.ip+="."
            if inkey.unicode=="." and (self.ip[-1:] in (".","") or count(self.ip, ".")>=3):
                return
            self.ip += inkey.unicode
        else:
            return  # if none of these things happened, no need to redraw
        self.redraw_textbox()
