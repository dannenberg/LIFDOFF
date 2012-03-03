from string import lowercase
import threading
import urllib, urllib2
from constants import COLORS
from screens.screen import Screen
from message_panel import MessagePanel
from bg_waves import Waves
import pygame
import networking
from dummy import Dummy

CLOSED = 1
OPEN = 2
AI = 3

class LobbyScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        
        self.my_index = 0
        
        self.player_colors = [(0xFF,0,0), (0,0xFF,0), (0xFF,0,0xFF), (0xFF,0xFF,0),
                              (0,0xFF,0xFF), (0xFF, 180, 0), (180,0,0xFF),
                              (0, 0xFF, 100), (0xFF,0xCC,0xCC), (0xCC,0xCC,0xFF)]
        self.color_pick = 0
        self.largefont = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 30)
        
        self.waves = Waves()
        
        self.players_panel = pygame.Surface((496,578), pygame.SRCALPHA)
        self.players_panel.fill((0, 0, 0, 128))
        self.players = []
        
        self.players.append(["Orez",pygame.Surface((474,48), pygame.SRCALPHA), False]) # TODO: bad
        for _ in xrange(1,10):
            self.players.append([CLOSED, pygame.Surface((474,48), pygame.SRCALPHA), True])
        self.redraw_players()
        self.chat_panel = pygame.Surface((696, 578), pygame.SRCALPHA)
        self.chat_panel.fill((0,0,0,128))
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
        def ready_button_click(i):
            def anon(scr, mpos):
                if i == self.my_index:
                    self.main.client.set_ready(int(not self.players[i][2]))
                else:
                    print "ready button clicked!!"
            return anon
        for x in xrange(10):
            self.clickbox.append((37, 75+54*x, 48, 48), ready_button_click(x))
        
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
                    newkick = msg[6:]
                    for i, (name, _, _) in enumerate(self.players):
                        if name == newkick:
                            self.recv_kick_player(str(i))
                    return
                self.main.client.send_message(msg)
            self.msgpanel.message(self.players[index][0], msg, self.player_colors[index])
        
    def reload_server_data(self, data="4\n0 0 Dickbob\n0 0 ChildToucher\n0 0 Despicable Human\n0 0 MurderTorture\n0 0 Orez\n2\n3\n1\n1\n1"):
        # get that info somehow
        self.my_index = int(data[0])
        data = data.split("\n")[1:]
        print data
        for i,d in enumerate(data):
            num = int(d[0])
            if num:
                self.players[i][0] = num
                self.players[i][2] = False
            else:
                self.players[i][0] = d[4:]
                self.players[i][2] = bool(int(d[2]))
        self.redraw_players()
    
    def join_lobby(self):
        self.main.client = networking.Client()
        self.main.client.start()
        
        def get_server_msg():
            while not self.main.done:
                while self.main.client.msgs.empty():
                    pass
                self.parse_server_output(self.main.client.msgs.get())
        threading.Thread(target=get_server_msg).start()
    
    def ready_up(self, data):
        print data
        index, ready  = int(data[0]), bool(int(data[2]))
        self.players[index][2] = ready
        self.redraw_players()
    
    def send_nick_change(self, nick):
        self.main.client.change_name(nick)
        self.recv_nick_change(str(self.my_index)+" "+nick)
        
    def recv_nick_change(self, data=None):
        data = data.split(" ")
        i, name = int(data[0]), ' '.join(data[1:])
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
        
    def parse_server_output(self, msg):
        actions = {"MSG":self.message, "NICK":self.recv_nick_change, "JOIN":self.recv_nick_change,
                   "DATA":self.reload_server_data, "READY":self.ready_up, "KICK":self.recv_kick_player}
        msg = msg.split(" ")
        cmd,msg = msg[0],' '.join(msg[1:])
        if cmd not in actions:
            print "Unknown action",cmd
            return
        actions[cmd](msg)
        
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
