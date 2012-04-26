from screens.screen import Screen
from string import count
from constants import *
from bg_waves import Waves
import networking
import pygame
class JoinScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.waves = Waves()
        self.inputblock = pygame.Surface((JOIN_BOX_W, JOIN_BOX_H), pygame.SRCALPHA)
        self.inputblock.fill((0,0,0,128))
        self.textbox = pygame.Surface((JOIN_TEXT_W, JOIN_TEXT_H), pygame.SRCALPHA)
        self.textbox.fill((0,0,0,64))
        self.font = pygame.font.Font(None, 40)
        okbutton = pygame.Surface((JOIN_BUTT_W,JOIN_BUTT_H), pygame.SRCALPHA)
        okbutton.fill((0,0,0,64))
        oktxt = self.font.render("Join", True, COLORS["white"])
        okbutton.blit(oktxt, (10,8))
        backbutton = pygame.Surface((JOIN_BUTT_W,JOIN_BUTT_H), pygame.SRCALPHA)
        backbutton.fill((0,0,0,64))
        backtxt = self.font.render("Back", True, COLORS["white"])
        backbutton.blit(backtxt, (5,8))
        self.inputblock.blit(backbutton, (JOIN_BUTT_BUF_X,JOIN_BUTT_BUF_Y))
        self.inputblock.blit(okbutton, (self.inputblock.get_width()-JOIN_BUTT_BUF_X-okbutton.get_width(),JOIN_BUTT_BUF_Y))
        instruction = self.font.render("Server Address", True, COLORS["white"])
        self.inputblock.blit(instruction, (int(((self.inputblock.get_width()-instruction.get_width())/2.0)),10))
        self.ip = ""
        self.countdown = 0
        
        def go_back(mpos):
            self.main.change_screen("main")
        self.clickbox.append((JOIN_BACK_X,JOIN_BUTT_Y, JOIN_BUTT_W,JOIN_BUTT_H), go_back)
        self.clickbox.append((JOIN_OK_X,JOIN_BUTT_Y, JOIN_BUTT_W,JOIN_BUTT_H), self.connect_ip)
        
    def display(self, screen):
        Screen.display(self, screen)
        self.waves.display(screen)
        screen.blit(self.inputblock, (JOIN_BOX_X,JOIN_BOX_Y))
        screen.blit(self.textbox, (JOIN_TEXT_X,JOIN_TEXT_Y))
        if self.countdown > 0:
            self.countdown -= 1
            if not self.countdown:
                self.redraw_textbox(False)
        
    def connect_ip(self, mpos=None):
        try:
            if count(self.ip, ".") == 3:
                int(self.ip[-1:])   # what we're "try"ing
                if self.main.join_server(self.ip):
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
        elif pygame.key.get_mods()&pygame.KMOD_CTRL:
            if inkey.key == pygame.K_v:
                pygame.scrap.init()
                word = str(pygame.scrap.get(pygame.SCRAP_TEXT)).rstrip(u"\x00")
                try:
                    test = map(int, word.split("."))
                    if len(test) != 4 or filter(lambda x:not (0<=x<256), test):
                        self.redraw_textbox(True)
                        return
                except ValueError:
                    self.redraw_textbox(True)
                    return
                self.ip = word
            else:
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
