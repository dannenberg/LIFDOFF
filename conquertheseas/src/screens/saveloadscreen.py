import pygame
import os
from constants import *
from bg_waves import Waves
from screens.screen import Screen

MAX_FILE_NAME = 18
LINE_HEIGHT = 40
class SaveLoadScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.waves = Waves()
        self.files = None
        self.font = pygame.font.Font(None, LINE_HEIGHT)
        self.disp_area = pygame.Surface((600, 520), pygame.SRCALPHA)
        self.text_area = pygame.Surface((500, LINE_HEIGHT), pygame.SRCALPHA)
        self.save_load_button = pygame.Surface((90,LINE_HEIGHT), pygame.SRCALPHA)
        self.highlight_over_box = pygame.Surface((600, LINE_HEIGHT), pygame.SRCALPHA)
        self.highlight_over_box.fill((0,0,0,64))
        self.highlight_over_loc = None
        self.highlight_click_box = pygame.Surface((600, LINE_HEIGHT), pygame.SRCALPHA)
        self.highlight_click_box.fill((0,0,0,64))
        self.highlight_click_loc = None
        self.redraw_save_load()
        self.return_to = None
        self.text_area.fill((0,0,0,64))
        self.text_input = ""
        self.back_button = pygame.Surface((110,50), pygame.SRCALPHA)
        self.back_button.fill((0,0,0,128))
        txt = pygame.font.Font(None, 60).render("Back", True, COLORS["white"])
        self.back_button.blit(txt, (5,5))
        def go_back(mpos):
            if self.return_to is not None:
                self.main.change_screen(self.return_to)
            else:
                print "I got nowhere to go to."
        self.clickbox.append((40, 740, 110, 50), go_back)
        self.redraw_files()
        
        def m_click(mpos):
            index = mpos[1]//LINE_HEIGHT
            if index < len(self.files):
                self.highlight_click_loc = (40, index*LINE_HEIGHT + 160)
                self.text_input = self.files[index]
                self.redraw_text()
        def m_over(mpos):
            index = mpos[1]//LINE_HEIGHT
            if index < len(self.files):
                self.highlight_over_loc = (40, index*LINE_HEIGHT + 160)
            else:
                self.highlight_over_loc = None
        def m_out():
            self.highlight_over_loc = None
        self.overbox.append((40,160,600,520), m_over, off=m_out)
        self.clickbox.append((40,160,600,520), m_click)
        self.clickbox.append((550,690,90,LINE_HEIGHT), self.save_load)
        
    def redraw_save_load(self, save=True):
        self.save_notload = save
        self.save_load_button.fill((0,0,0,64))
        txt = self.font.render("Save" if save else "Load", True, COLORS["white"])
        self.save_load_button.blit(txt, (12,8))
        
    def redraw_files(self):
        d = os.path.dirname("../saves/")
        if not os.path.exists(d):
            os.makedirs(d)
        self.files = ['.'.join(f.split(".")[:-1]) for f in os.listdir("../saves/") if "sav"==f.split(".")[-1]]
        self.disp_area.fill((0,0,0,64))
        for i,f in enumerate(self.files):
            txt = self.font.render(f, True, COLORS["white"])
            self.disp_area.blit(txt, (10,i*LINE_HEIGHT+10))
        
    def redraw_text(self):
        self.text_area.fill((0,0,0,64))
        txt = self.font.render(self.text_input, True, COLORS["white"])
        self.text_area.blit(txt, (5,5))
        
    def on_switch_in(self):
        self.main.reset_screen("saveload")
        
    def display(self, screen):
        Screen.display(self, screen)
        self.waves.display(screen)
        if self.highlight_over_loc is not None:
            screen.blit(self.highlight_over_box, self.highlight_over_loc)
        if self.highlight_click_loc is not None:
            screen.blit(self.highlight_click_box, self.highlight_click_loc)
        screen.blit(self.disp_area, (40,160))
        screen.blit(self.text_area, (40,690))
        screen.blit(self.save_load_button, (550,690))
        screen.blit(self.back_button, (40,740))
        
    def save_load(self, mpos=None):
        if not self.text_input:
            #print "Invalid filename"
            return False
        f = self.text_input+".sav"
        if self.save_notload:
            if self.text_input in self.files:
                #print "Hot damn are you sure you want to overwrite that file?"
                return False
            if self.return_to is not None:
                self.main.change_screen(self.return_to)
            self.main.save("../saves/"+f)
            self.main.change_screen("saveload")
        else:   # load
            if self.text_input not in self.files:
                #print "File does not exist"
                return False
            self.main.load("../saves/"+f)
        
    def notify_key(self, inkey):
        if inkey.key == pygame.K_BACKSPACE:
            self.text_input = self.text_input[:-1]
        elif inkey.key == pygame.K_TAB:
            try:    # tab complete
                mname = self.text_input.lower()
                if mname == "": # don't tab complete on nothing
                    return
                matches = []    # files whose names we've matched
                for i,name in enumerate(self.files):
                    if mname == name[:len(mname)].lower():  # if the first part of their name is what you've typed
                        matches += [name]       # they're a match
                if len(matches) == 1:
                    self.text_input = matches[0]
                elif len(matches) > 1:
                    def get_most_letters():
                        text = ""
                        for x in xrange(len(mname), MAX_FILE_NAME):
                            letter = None
                            for i in matches:
                                if letter is None:
                                    letter = i[x:x+1]
                                    if letter == "":
                                        return text
                                elif i[x:x+1] != letter:
                                    return text
                            text += letter
                    self.text_input += get_most_letters()
            except IndexError:
                pass
        elif inkey.key == pygame.K_RETURN or inkey.key == pygame.K_KP_ENTER:
            self.save_load()
        elif inkey.unicode and len(self.text_input)<MAX_FILE_NAME and inkey.unicode not in "\\/:*?\"<>|":
            self.text_input += inkey.unicode    # send the unicode character you pressed
        else:
            return  # if none of these things happened, no need to redraw
        self.redraw_text()
