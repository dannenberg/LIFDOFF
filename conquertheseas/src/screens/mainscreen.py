import pygame
import math
from constants import COLORS
from mousehitbox import MouseHitboxes
from screen import Screen

class MainScreen(Screen):
    """ Main menu screen """
    def __init__(self, main):
        Screen.__init__(self, main)
        self.water_level = 0 #defines the height of the water in the background
        self.water_range = 16 #how much the water level fluctuates
        self.selectbox = [None, 15, 205, 50, True] #coords of the box (x, y, width, height) which highlights selected item
        self.gotobox = [12.5, 15, 205, 50] #coords of the desitination of the selectbox
        self.sel_accel = 3 #acceleration to new pos
        self.sel_speed = 0 #currents speed
        self.smallerfont = pygame.font.Font(None, 50) #font for menu items
        
        self.options = ["New Game", "Load Game", "Options", "Credits", "Exit"] # menu options
        self.submenuoptions = None
        self.submenu = 0
        self.maxwid = max([self.smallerfont.size(x)[0] for x in self.options])
        
        def over(setbit):
            def anon(scr, mpos): #picks new location for gotobox
                self.selectbox[4] = setbit
                self.selectbox[2] = (self.maxwid if setbit else self.submaxwid)+25
                wait = (mpos[1] - 13)//50
                if 0 <= wait < len(self.options):
                    self.gotobox = [12.5, (wait * 50) + 15]
                    if self.selectbox[0] == None:
                        self.selectbox[0:2] = self.gotobox[:]
            return anon

        def out(scr): #removes box since we have left menu
            self.selectbox[0] = None
        self.overbox.append((30, 200, self.maxwid+50, 280), over(True), out)

        def click_newgame(someone, mpos):
            if self.submenu == 1:
                return
            if self.submenu != 0:
                self.overbox.remove((90+self.maxwid, 200))
            self.submenu = 1
            self.submenuoptions = ["Single Player", "Join Multiplayer", "Host Multiplayer"]
            self.submaxwid = self.maxwidth(self.submenuoptions)
            self.overbox.append((90+self.maxwid, 200, self.submaxwid+50, 150), over(False), out)
            
            def click_singleplayer(x,mpos):
                self.main.change_screen("game")
            
            self.clickbox.append((90+self.maxwid, 200, self.submaxwid+50, 50), click_singleplayer)
            
        def click_options(someone, mpos):
            if self.submenu == 2:
                return
            if self.submenu != 0:
                self.overbox.remove((90+self.maxwid, 200))
                try:
                    self.clickbox.remove((90+self.maxwid, 200))
                except:
                    pass
            self.submenu = 2
            self.submenuoptions = ["Multiplayer name:","[_____________]","AI Level: 1 2 3","SFX:  "+("-"*9)+"|","Music:"+("-"*9)+"|"]
            self.submaxwid = self.maxwidth(self.submenuoptions)
            self.overbox.append((90+self.maxwid, 200, self.submaxwid+50, 150), over(False), out)
            
        def click_credits(someone, mpos):
            self.main.change_screen("credits")
            
        def click_exit(someone, mpos): #ideally this will close the game
            self.main.exit()
        
        for i,x in enumerate([click_newgame, lambda x,y:x, click_options, click_credits, click_exit]):
            self.clickbox.append((30, 215+50*i, self.maxwid, 45), x)
    
    def display(self, screen):
        Screen.display(self, screen) #calls super
        
        self.water_level = (self.water_level + (math.pi / 180)) % (math.pi * 2) #movement in rads for waterlevel (since it is based on sin)
        modifier = int(math.sin(self.water_level) * self.water_range) #actual change
        
        font = pygame.font.Font(None, 170) #title text defined and two colored versions created
        text = font.render("CONQUER THE SEAS", True, COLORS["black"])
        whitetext = font.render("CONQUER THE SEAS", True, COLORS["submergedt"])
        
        #draws the sky, water, and text
        screen.fill(COLORS["sky"])
        water = pygame.Surface((1280, 700 - modifier))
        water.fill(COLORS["water"])
        screen.blit(text, [20, 50])
        water.blit(whitetext, [20,  -50 - modifier])
        screen.blit(water, [0, modifier + 100])
        
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
        
        screen.blit(textbox, (30, 200))
        
    def maxwidth(self, optionlist):
        return max([self.smallerfont.size(x)[0] for x in optionlist])
