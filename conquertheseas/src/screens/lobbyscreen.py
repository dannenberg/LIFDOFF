import time
from string import lowercase
import threading
import urllib, urllib2
from constants import COLORS
from screens.screen import Screen
from message_panel import MessagePanel
from bg_waves import Waves
import pygame
import socket
import networking
from dummy import Dummy

CLOSED = 1
OPEN = 2
AI = 3

class LobbyScreen(Screen):
    def __init__(self, main, host=True):
        Screen.__init__(self, main)
        
        self.my_index = 0
        
        self.player_colors = [(0xFF,0,0), (0,0xFF,0), (0xFF,0,0xFF), (0xFF,0xFF,0),
                              (0,0xFF,0xFF), (0xFF, 180, 0), (180,0,0xFF),
                              (0, 0xFF, 100), (0xFF,0xCC,0xCC), (0xCC,0xCC,0xFF)]
        self.color_pick = 0
        self.largefont = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 30)
        
        self.waves = Waves()
        
        self.player_menu = pygame.Surface((415, 120), pygame.SRCALPHA)
        self.player_menu_pos = (0, 0)
        
        self.players_panel = pygame.Surface((496,578), pygame.SRCALPHA)
        self.players_panel.fill((0, 0, 0, 128))
        self.players = []

        self.start_timeout = time.time()
        
        self.players.append(["Host",pygame.Surface((474,48), pygame.SRCALPHA), False])
        for _ in xrange(1,10):
            self.players.append([CLOSED, pygame.Surface((474,48), pygame.SRCALPHA), False])
        self.redraw_players()
        self.chat_panel = pygame.Surface((696, 578), pygame.SRCALPHA)
        self.chat_panel.fill((0,0,0,128))
        send_button = pygame.Surface((67,30), pygame.SRCALPHA)
        send_button.fill((0,0,0,64))
        txt = self.font.render("Send", True, (0xCC,)*3)    # TODO: nope
        send_button.blit(txt, (10,7))
        self.chat_panel.blit(send_button, (20+582+5,577-38))
        self.textbox = pygame.Surface((1820,30), pygame.SRCALPHA)
        self.textbox.fill((0,0,0,64))
        self.base_panel = pygame.Surface((1215, 96), pygame.SRCALPHA)
        self.base_panel.fill((0,0,0,128))
        txt_leave_lobby = self.largefont.render("Leave Lobby", True, COLORS["white"])
        self.button_leave_lobby = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_leave_lobby.fill((0,0,0,64))
        self.button_leave_lobby.blit(txt_leave_lobby, (15,15))
        self.base_panel.blit(self.button_leave_lobby, (10,10))
        
        if host:
            def get_ip():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(('google.com', 80))
                    ip = s.getsockname()[0]
                    s.close()

                    txt_ip = self.largefont.render(ip, True, COLORS["white"])
                    self.base_panel.blit(txt_ip, (450, 25))
                    def copy_ip(mpos):
                        try:
                            pygame.scrap.init()
                            pygame.scrap.put(pygame.SCRAP_TEXT, ip)
                        except:
                            pass # fixes!
                    self.clickbox.append((476,706,txt_ip.get_width(), txt_ip.get_height()), copy_ip)
                except (urllib2.URLError, urllib2.HTTPError, IOError):
                    print "Error fetching IP"
            threading.Thread(target=get_ip).start()
        
        self.button_start = pygame.Surface((331,76), pygame.SRCALPHA)
        self.button_start.fill((0,0,0,64))
        txt_start_game = self.largefont.render("Start Game", True, COLORS["white"])
        self.button_start.blit(txt_start_game, (30,15))
        self.base_panel.blit(self.button_start, (870,10))
        def start_game(mpos):
            if time.time() - self.start_timeout > 3:
                self.main.client.start_game()
                self.start_timeout = time.time()
        self.clickbox.append((900, 690, 331, 76), start_game)
        
        self.text_input = ""
        self.msgpanel = MessagePanel((652,509), 23, self.font)
        self.startable = False
        def to_main(mpos):
            self.main.change_screen("main")
        self.clickbox.append((37,692,329,74), to_main)
        def ready_button_click(i):
            def anon(mpos):
                if i == self.my_index:
                    self.main.client.set_ready(int(not self.players[i][2]))
                else:
                    print "ready button clicked!!"
            return anon
        for x in xrange(10):
            self.clickbox.append((37, 75+54*x, 48, 48), ready_button_click(x))
        def player_panel_click(i):
            def anon(mpos):
                if self.my_index == 0:      # only the host can kick
                    if i == self.my_index:
                        pass
                    elif isinstance(self.players[i][0], int):
                        self.player_menu_pos = (95, 75+54*i+48)
                        options = ["Closed", "Open", "AI"]
                        self.player_menu.fill((0,0,0,128))
                        def clearworking(mpos):
                            self.player_menu_pos = (0,0)
                            for k in xrange(3):
                                self.clickbox.remove((95, 75+54*i+48+k*40+5))
                            self.clickbox.remove((0,0))
                        self.clickbox.append((0, 0, 1280, 800), clearworking, z=2)
                        for j,option in enumerate(options):
                            def wrapper(toWhat):
                                def changeto(mpos):
                                    self.main.client.set_slot(i, toWhat+1)
                                    self.player_menu_pos = (0,0)
                                    for k in xrange(3):
                                        self.clickbox.remove((95, 75+54*i+48+k*40+5))
                                    self.clickbox.remove((0,0))
                                return changeto
                            self.clickbox.append((95, 75+54*i+48+j*40+5, 415, 40), wrapper(j), z=3)
                            text = self.font.render(option, True, COLORS["white"])
                            self.player_menu.blit(text, (5, 5+j*40))
                    else:   # it's a person
                        self.player_menu_pos = (95, 75+54*i+48)
                        self.player_menu.fill((0,0,0,0))
                        pygame.draw.rect(self.player_menu, (0,0,0,128), (0,0,415,30))
                        def clearworking(mpos):
                            self.player_menu_pos = (0,0)
                            self.clickbox.remove((95, 75+54*i+48+5))
                            self.clickbox.remove((0,0))
                        self.clickbox.append((0, 0, 1280, 800), clearworking, z=2)
                        def kickhim(mpos):
                            self.main.client.kick_player(str(i))
                            self.player_menu_pos = (0,0)
                            self.clickbox.remove((95, 75+54*i+48+5))
                            self.clickbox.remove((0,0))
                        self.clickbox.append((95, 75+54*i+48, 415, 40), kickhim, z=3)
                        text = self.font.render("Kick", True, COLORS["white"])
                        self.player_menu.blit(text, (5, 5))
            return anon
        for x in xrange(10):
            self.clickbox.append((95, 75+54*x, 415, 48), player_panel_click(x))
        
        def wrapper(mpos):
            self.message()
            self.textbox.fill((0,0,0,64))
            txt = self.font.render(self.text_input, True, COLORS["white"])
            self.textbox.blit(txt, (5,5))
        self.clickbox.append((1154, 580, 64, 25), wrapper)
        
    def redraw_players(self):
        self.players_panel.fill((0, 0, 0, 128))
        for i,(name, surf, ready) in enumerate(self.players):
            surf.fill((0,0,0,64))
            if ready:
                pygame.draw.rect(surf, (135,221,68,128), (0,0,48,48))
            pygame.draw.rect(surf, (0,0,0,0), (48,0,12,48)) # clear
            color = self.player_colors[i]
            if isinstance(name, int):
                color = (0x80, 0x80, 0x80)
                if name == CLOSED:
                    name = "Closed"
                elif name == OPEN:
                    name = "Open"
                elif name == AI:
                    name = "AI Player"
            surf.blit(self.font.render(name, True, color), (65,15))
            self.players_panel.blit(surf, (10,37+i*54))
    
    def display(self, screen):
        Screen.display(self, screen)
        # I feel like the following code is flipping me off...
        self.waves.display(screen, False)
        screen.blit(self.players_panel, (26,38))
        screen.blit(self.chat_panel, (545, 38))
        screen.blit(self.textbox, (565,577), (min(self.textbox.get_width()-582, max(0,(self.font.size(self.text_input)[0])-582+10)),0,582,30))
        screen.blit(self.base_panel, (26, 681))
        screen.blit(self.msgpanel.view, (566,63))
        
        if self.player_menu_pos != (0,0):
            screen.blit(self.player_menu, (self.player_menu_pos[0], self.player_menu_pos[1]))
        
    def message(self, data=None):
        index = self.my_index
        msg = self.text_input
        if not (data is None):  # gotta parse the data
            data = data.split(" ")
            index, msg = int(data[0]), ' '.join(data[1:])
        if msg: # needs to like... say something.
            if isinstance(self.players[index][0], int):
                print "Why is",self.players[index][0],"trying to talk?"
                return
            if index == self.my_index:
                self.text_input = ""
                if msg[:6] == "/nick ":
                    newnick = msg[6:]
                    if self.main.valid_nick(newnick):
                        self.send_nick_change(newnick)
                    return
                if msg[:6] == "/kick ":
                    newkick = msg[6:].lower()
                    for i, (name, _, _) in enumerate(self.players):
                        if not isinstance(name, int):
                            if name.lower() == newkick:
                                self.main.client.kick_player(str(i))
                                self.recv_kick_player(str(i))
                    return
                self.main.client.send_message(msg)
            self.msgpanel.message(self.players[index][0], msg, self.player_colors[index])
        
    def reload_server_data(self, data):
        """ loading player data after joining a lobby """
        self.main.race_cond = True
        self.my_index = int(data[0])    # what slot should you get
        data = data.split("\n")[1:]     # split on newlines (ignore the first slot)
        print data
        for i,d in enumerate(data):     # 
            num = int(d[0])             # are you a player or a certain value
            if num:                     # if not a human
                self.players[i][0] = num    # make my "name" that value
                self.players[i][2] = False  # also i'm 'unready'
            else:                           # 0 c Name (c is 0 if unready, 1 if ready)
                self.players[i][0] = d[4:]  # the rest of the string after the first two characters and spaces is the name
                self.players[i][2] = bool(int(d[2]))    # char space _char_ is readiness
        if self.main.player_name is None:
            self.main.player_name = self.players[self.my_index][0]
        self.redraw_players()           # redraw that board
    
    def ready_up(self, data):
        print data
        index, ready  = int(data[0]), bool(int(data[2]))
        self.players[index][2] = ready
        self.redraw_players()
    
    def send_nick_change(self, nick):
        self.main.player_name = nick
        self.main.client.change_name(nick)
        
    def recv_nick_change(self, data=None):
        data = data.split(" ")
        i, name = int(data[0]), ' '.join(data[1:])
        if i == self.my_index:
            self.main.player_name = name
        try:
            name = int(name)
        except ValueError:
            pass
        if not (isinstance(self.players[i][0], int) == isinstance(name, int) == False):
            self.ready_up(str(i)+" 0")
        self.players[i][0] = name
        self.redraw_players()
        
    def recv_kick_player(self, data=None):
        kickme = int(data[0])
        if kickme == self.my_index: # D:
            self.main.client = None
            self.main.change_screen("main")
            return
        self.players[kickme][0] = OPEN
        self.players[kickme][2] = False
        self.redraw_players()
        
    def recv_start_game(self, players):
        print "game starting!!"
        seed, _, players = players.partition(" ")
        self.main.rand.seed(int(seed))
        players = players.split("\t")
        self.main.reset_screen("game", players, False)
        self.main.reset_screen("shop")
        self.main.change_screen("game")
        
    def notify_key(self, inkey):
        if inkey.key == pygame.K_BACKSPACE:
            self.text_input = self.text_input[:-1]
        elif inkey.key == pygame.K_TAB:
            try:    # tab complete
                mname = self.text_input.split(' ')[-1].lower()
                if mname == "": # don't tab complete on nothing
                    return
                matches = []    # people whose names we've matched
                for i,(name, _, _) in enumerate(self.players):
                    if not isinstance(name, int):   # don't check slots that aren't players
                        if mname == name[:len(mname)].lower():  # if the first part of their name is what you've typed
                            matches += [name]       # they're a match
                if len(matches) == 1:
                    self.text_input = self.text_input[:-len(mname)]+matches[0]
                elif len(matches) > 1:
                    def get_most_letters():
                        text = ""
                        for x in xrange(len(mname), 22):
                            letter = None
                            for i in matches:
                                if letter is None:
                                    letter = i[x:x+1]
                                    if letter == "":
                                        return text
                                    continue
                                if i[x:x+1] != letter:
                                    return text
                            text += letter
                    self.text_input += get_most_letters()
            except IndexError:
                pass
        elif inkey.key == pygame.K_RETURN or inkey.key == pygame.K_KP_ENTER:
            self.message()  # send my current message
        elif inkey.unicode and self.font.size(self.text_input+inkey.unicode)[0] <= self.textbox.get_width()-10 and len(self.text_input)<250:
            self.text_input += inkey.unicode    # send the unicode character you pressed
        else:
            return  # if none of these things happened, no need to redraw
        self.textbox.fill((0,0,0,64))
        txt = self.font.render(self.text_input, True, COLORS["white"])
        self.textbox.blit(txt, (5,5))
