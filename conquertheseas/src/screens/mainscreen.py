import pygame
import math
from constants import COLORS
from mousehitbox import MouseHitboxes
from screen import Screen
from bg_waves import Waves
import networking

class MainScreen(Screen):
    """ Main menu screen """
    def __init__(self, main):
        Screen.__init__(self, main)
        self.selectbox = [None, 15, 205, 50, True] #coords of the box (x, y, width, height) which highlights selected item
        self.gotobox = [12.5, 15, 205, 50] #coords of the desitination of the selectbox
        self.sel_accel = 3 #acceleration to new pos
        self.sel_speed = 0 #current speed
        self.smallerfont = pygame.font.Font(None, 50) #font for menu items
        
        self.options = ["New Game", "Load Game", "Options", "Credits", "Exit"] # menu options
        self.submenuoptions = None
        self.submenu = 0    # submenu = 1 means one submenu is open
        self.maxwid = max([self.smallerfont.size(x)[0] for x in self.options])  # width of hitbox (highlighted area)
        # it's the 
        
        self.textbox = None
        self.text_input = ""
        self.entering_name = False
        
        self.waves = Waves()
        
        def over(setbit):
            def anon(mpos): # picks new location for gotobox
                self.selectbox[4] = setbit
                self.selectbox[2] = (self.maxwid if setbit else self.submaxwid)+25
                wait = (mpos[1] - 13)//50
                if 0 <= wait < len(self.options):
                    self.gotobox = [12.5, (wait * 50) + 15]
                    if self.selectbox[0] == None:
                        self.selectbox[0:2] = self.gotobox[:]
            return anon

        def out(): #removes box since we have left menu
            self.selectbox[0] = None
            
        self.overbox.append((30, 200, self.maxwid+50, 280), over(True), out)    # makes entire menu mouse-over-able

        def click_newgame(mpos):
            self.entering_name = False
            if self.submenu == 1:   # you've already clicked new game
                return  
            if self.submenu != 0:   # you've clicked on options (or load)
                self.overbox.remove((90+self.maxwid, 200))  # remove that submenu's overbox
                self.clickbox.remove((90+self.maxwid, 250))
            self.submenu = 1
            self.submenuoptions = ["Single Player", "Join Multiplayer", "Host Multiplayer"]
            self.submaxwid = self.maxwidth(self.submenuoptions)
            self.overbox.append((90+self.maxwid, 200, self.submaxwid+50, 150), over(False), out)
            
            def click_singleplayer(mpos):
                self.main.change_screen("game")
            def click_joingame(mpos):
                self.main.change_screen("join")
            def click_hostgame(mpos):
                self.main.server = networking.Server()
                self.main.server.start()
                self.main.join_server()
                self.main.change_screen("lobby")
            
            self.clickbox.append((90+self.maxwid, 215, self.submaxwid+50, 50), click_singleplayer)
            self.clickbox.append((90+self.maxwid, 265, self.submaxwid+50, 50), click_joingame)
            self.clickbox.append((90+self.maxwid, 315, self.submaxwid+50, 50), click_hostgame)
            
        def click_loadgame(mpos):
            self.entering_name = False
            self.main.change_screen("saveload")
            #self.main.screens["saveload"].redraw_save_load(False)
            
        def click_options(mpos):
            self.entering_name = False
            
            if self.submenu == 2:
                return
            if self.submenu == 1:   # new game submenu is open
                self.overbox.remove((90+self.maxwid, 200))
                #self.clickbox.remove((90+self.maxwid, 200))
                self.clickbox.remove((90+self.maxwid, 215))
                self.clickbox.remove((90+self.maxwid, 265))
                self.clickbox.remove((90+self.maxwid, 315))
            self.submenu = 2
            self.submenuoptions = ["Multiplayer name:","________________","AI Level: 1 2 3","SFX:  "+("-"*9)+"|","Music:"+("-"*9)+"|"]
            self.submaxwid = self.maxwidth(self.submenuoptions)
            self.overbox.append((90+self.maxwid, 200, self.submaxwid+50, 280), over(False), out)
            self.textbox = pygame.Surface((750,40), pygame.SRCALPHA)
            if self.main.player_name is not None:
                self.textbox.blit(self.smallerfont.render(self.main.player_name.strip(), True, COLORS["white"]),(5,5))
            
            def click_changename(mpos):
                self.entering_name = True
                if self.main.player_name is not None:
                    self.text_input = self.main.player_name
                #if self.main.valid_nick(self.text_input):
                #    self.main.player_name = self.text_input
                #else:
                #    self.main.player_name = None
                
            self.clickbox.append((90+self.maxwid, 250, self.submaxwid+50, 50), click_changename)

        def click_credits(mpos):
            self.entering_name = False
            if self.main.valid_nick(self.text_input.strip()):
                self.main.player_name = self.text_input.strip()
            else:
                self.main.player_name = None
            self.main.change_screen("credits")            
            
        def click_exit(mpos): #ideally this will close the game
            self.main.exit()
        
        for i,x in enumerate([click_newgame, click_loadgame, click_options, click_credits, click_exit]):
            self.clickbox.append((30, 215+50*i, self.maxwid, 45), x)
    
    def display(self, screen):
        """ main screen turn on """
        Screen.display(self, screen) #calls super
        
        self.waves.display(screen)
        ####################################
        
        textbox = pygame.Surface((self.maxwid + 50, len(self.options)*50+30), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 128))
        
        if self.submenuoptions != None:
            subtextbox = pygame.Surface((self.submaxwid + 50, len(self.submenuoptions)*50+30), pygame.SRCALPHA)
            subtextbox.fill((0, 0, 0, 128))
        
        #decide whether or not to move selectbox then do so
        if self.selectbox[0] != None:
            direction = math.copysign(1, self.gotobox[1] - self.selectbox[1])
            if self.selectbox[1] == self.gotobox[1]:
                self.sel_speed = 0
            else:
                self.sel_speed  += direction * self.sel_accel
                self.selectbox[1]  += self.sel_speed
                if direction < 0:
                    self.selectbox[1] = max(self.selectbox[1], self.gotobox[1])
                else:
                    self.selectbox[1] = min(self.selectbox[1], self.gotobox[1])
            if not (12.5<=self.selectbox[1]<=(len(self.options) - 1) * 50 + 12.5):
                self.selectbox[1] = max(min((len(self.options) - 1) * 50 + 12.5, self.selectbox[1]), 12.5)
                self.sel_speed = 0
            pygame.draw.rect((textbox if self.selectbox[4] else subtextbox), (0, 0, 0, 192), self.selectbox[:4])

        #draw all the menu items
        for i, x in enumerate(self.options):
            text = self.smallerfont.render(x, True, COLORS["white"])
            textbox.blit(text, (25, i * 50 + 25))
            
        if self.submenuoptions != None:
            for i, x in enumerate(self.submenuoptions):
                text = self.smallerfont.render(x, True, COLORS["white"])
                subtextbox.blit(text, (25, i * 50 + 25))
            screen.blit(subtextbox, (90 + self.maxwid, 200))

        if self.submenu == 2:
            #screen.blit(self.textbox, (300, 270))
            screen.blit(self.textbox, (300,270), (min(self.textbox.get_width()-self.submaxwid, max(0,(self.smallerfont.size(self.text_input)[0])-self.submaxwid+10)),0,self.submaxwid,40))
            
        
        screen.blit(textbox, (30, 200))
        
    def maxwidth(self, optionlist):
        return max([self.smallerfont.size(x)[0] for x in optionlist])
        
    def notify_key(self, inkey):
        if self.entering_name:
            if inkey.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif inkey.key == pygame.K_RETURN or inkey.key == pygame.K_KP_ENTER:
                return 
            elif inkey.unicode:#self.smallerfont.size(self.text_input+inkey.unicode)[0] <= self.textbox.get_width()-10 and 
                if len(self.text_input) < 2 or self.main.valid_nick((self.text_input+inkey.unicode).strip()):
                    self.text_input += inkey.unicode
            else:
                return  # if none of these things happened, no need to redraw
            self.textbox.fill((0,0,0,0))
            txt = self.smallerfont.render(self.text_input, True, COLORS["white"])
            self.textbox.blit(txt, (5,5))
            if self.main.valid_nick(self.text_input.strip()):
                self.main.player_name = self.text_input.strip()
            else:
                self.main.player_name = None
            
    def on_switch_in():
        if self.main.server != None:
            self.main.server.stop()
            self.main.server = None
        if self.main.client != None:
            self.main.client.stop()
            self.main.client = None
