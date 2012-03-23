import pygame
import networking
import random
import math
import re
import threading
import os
import pickle
from constants import SCREEN_WIDTH,SCREEN_HEIGHT
from screens.screen import *
from screens.gamescreen import *
from screens.introscreen import *
from screens.mainscreen import *
from screens.creditsscreen import *
from screens.shopscreen import *
from screens.upgradescreen import *
from screens.lobbyscreen import *
from screens.joinscreen import *
from screens.saveloadscreen import *

class Main():
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.server = None
        self.client = None
        self.stdsize=(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.size=self.stdsize
        self.scale = 1
        self.screen=pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.screens = {"intro": IntroMovie(self),
                        "game": GameScreen(self),
                        "main": MainScreen(self),
                        "credits":CreditsScreen(self),
                        "upgrade":UpgradeScreen(self),
                        "shop":ShopScreen(self),
                        "lobby":LobbyScreen(self),
                        "join":JoinScreen(self),
                        "saveload":SaveLoadScreen(self)}

        pygame.display.set_caption("FRIENDS OF THE SEA")
        self.done=False
        clock = pygame.time.Clock()
        self.player_name = None
        self.mainscreen = self.screens["main"]

        pygame.key.set_repeat(500,20)   # half second delay, 20 second interval
        self.keys = set()
        preblit = pygame.Surface((self.stdsize))
        preblit2 = None
        
        font = pygame.font.Font(None, 16)
        
        while not self.done:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done=True
                elif event.type == pygame.MOUSEMOTION:
                    self.mainscreen.over(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.mainscreen.click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.keys.add(event.key)
                    self.mainscreen.notify_key(event)
                elif event.type == pygame.KEYUP:
                    self.keys.discard(event.key)
                elif event.type == pygame.VIDEORESIZE:
                    self.size,self.scale = self.resize(event.w, event.h)
                    self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
                    self.mainscreen.abs_scale(self.scale)
            
            self.mainscreen.display(preblit)
            preblit.blit(font.render(str(clock.get_fps()), True, (0xFF,0,0)), (0,0))
            preblit2 = pygame.transform.scale(preblit, self.size)
            self.screen.blit(preblit2, (0,0))
            pygame.display.flip()
        pygame.quit()
        if self.server != None:
            self.server.stop()
            self.server = None
        if self.client != None:
            self.client.stop()
            self.client = None
    
    def join_server(self, ip=None):
        self.client = networking.Client(ip)
        self.reset_screen("lobby")
        self.client.start()
        self.race_cond = False
        def get_server_msg():
            while not self.done and self.client is not None:
                while not self.done and self.client is not None and self.client.msgs.empty():
                    pass
                if self.client is not None and not self.client.msgs.empty():
                    msg = self.client.msgs.get(block = False)
                    if "DIE!" in msg:
                        self.client = None
                        self.race_cond = 2
                        return
                    self.parse_server_output(msg)
        threading.Thread(target=get_server_msg).start()
        while not self.race_cond:
            pass
        if self.race_cond == 2:
            return False
        if self.client is not None and self.player_name is not None and self.race_cond:
            self.client.change_name(self.player_name)
        return True
    
    def parse_server_output(self, msg):
        actions = {"MSG":self.screens["lobby"].message, "NICK":self.screens["lobby"].recv_nick_change,
                   "JOIN":self.screens["lobby"].recv_nick_change, "DATA":self.screens["lobby"].reload_server_data,
                   "READY":self.screens["lobby"].ready_up, "KICK":self.screens["lobby"].recv_kick_player,
                   "START":self.screens["lobby"].recv_start_game, "ERROR":lambda x:None}
        msg = msg.split(" ")
        cmd,msg = msg[0],' '.join(msg[1:])  # first word of the message is the action
        if cmd not in actions:
            print "Unknown action",cmd,msg
            return
        actions[cmd](msg)
    
    def change_screen(self, screen):
        self.screens[screen].on_switch_in()
        self.mainscreen = self.screens[screen]
        self.mainscreen.abs_scale(self.scale)
    
    def save(self, floc):
        f = open(floc, "w+")
        pickle.dump((VERSION, self.screens["game"].enemy_boards), f)
        
    def load(self, floc):
        f = open(floc, "r")
        v, boards = pickle.load(f)
        self.reset_screen("game", boards)
        self.change_screen("game")
    
    def exit(self):
        self.done = True
        
    def reset_screen(self, screen, *args):
        self.screens[screen] = self.screens[screen].__class__(self, *args)
        
    def resize(self, w, h):
        if w==self.size[0]:  # width was constant
            scale = float(h)/self.stdsize[1]
            return ((int(scale*self.stdsize[0]),h),scale)
        scale = float(w)/self.stdsize[0]
        return ((w,int(scale*self.stdsize[1])),scale)
    
    def valid_nick(self, newnick):
        return re.match(r"^[A-Z][A-Z0-9 ]{0,20}[A-Z0-9]$", newnick, re.I)

if __name__ == "__main__":
    Main()
