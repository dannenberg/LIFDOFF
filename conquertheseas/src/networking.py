import socket
import select
import threading
import random
from Queue import Queue
from board import Board
from constants import *

HOST = socket.gethostname()
PORT = 11173
ADDR = (HOST,PORT)

class Server(threading.Thread):
    PLAYER = 0
    CLOSED = 1
    OPEN = 2
    AI = 3

    def __init__(self):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(ADDR)
        self.slots = [{"type":Server.CLOSED} for _ in xrange(10)]
        self.host = None
        self.done = False
        self.game_slots = []
        self.commands = {
            "MSG"    : self.send_message,
            "NICK"   : self.change_name,
            "SLOT"   : self.set_slot,
            "READY"  : self.set_ready,
            "START"  : self.start_game,
            "KICK"   : self.kick_player,
            "MOVE"   : self.act_generic("MOVE"),
            "SENT"   : self.act_sent,
            "SHOOT"  : self.act_generic("SHOOT"),
            "SPECIAL": self.act_generic("SPECIAL"),
            "BUY"    : self.act_generic("BUY"),
            "UPGRADE": self.act_generic("UPGRADE"),
            "TURN"   : self.act_turn,
            "END"    : self.act_end
            }
        
    def act_generic(self, action):
        def anon(c, msg):
            board = self.get_sender(c)
            self.add_action(board, action+" "+msg)
        return anon
        
    # TODO: make all these act_ functions actually like... queue some actions
    def act_move(self, c, msg):
        x,y,dude = msg.split(" ")
        print "server says: Def Unit",dude,"moved to",x,",",y
        
    def act_sent(self, c, msg):
        """ Deployed a unit on an enemy board """
        bnum, uftoken, x, y = msg.split(" ")
        # TODO: x will tell us the turn to come in. Queue it to the correct board, then later sort it onto the correct turn
        print "server says: Deployed unit",uftoken,"at (",x,",",y,"), on board ",bnum
        self.add_action(int(bnum), "SENT "+uftoken+" "+x+" "+y, OFFENSIVE_PLACEMENT_DEPTH - (BOARD_SQUARES_X - int(x)))
        
    def act_shoot(self, c, msg):
        print "server says: Def Unit",msg,"has shot!"
        
    def act_buy(self, c, msg):
        print "simon says: bought",msg,"!"
        
    def act_special(self, c, msg):
        """ But only if you feel special """
        x,y,dude = msg.split(" ")
        print "server says: Def Unit",dude,"has SPECIALED at",x,",",y
        
    def act_turn(self, c, msg):
        return  # TODO: stop
        print "server says: New Turn!"
        self.slots[self.get_sender(c)]["index"] += 1
        
    def act_upgrade(self, c, msg):
        print "masuda says: upgrade",msg,"purchased!"
        
    def act_end(self, c, msg):
        """ End transmission of moves """
        sender = self.get_sender(c)
        print self.slots[sender]["name"],"has sent all their moves"
        self.set_sent(sender)
    
    def add_action(self, board, msg, index=None):
        """ Format msg nicely please. """
        if index is None:
            index = self.slots[board]["index"]
        actions = self.slots[board]["actions"]
        if index not in actions:
            actions[index] = []
        actions[index].append(msg)
    
    def set_sent(self, sender):
        print "networking.set_sent: Player",sender,"set sent"
        self.slots[sender]["sent"] = True
        if not filter(lambda x:not x["sent"] and x["type"]==Server.PLAYER, self.slots):  # if all humans has sent TODO: someday might want to drop the x["type"]==Player part
            print "networking.set_sent: Generate the AI's turn"
            for i,x in enumerate(self.slots):
                if x["type"] == Server.AI:
                    self.generate_ai_turns(i)
            self.do_turns()
    
    def do_turns(self):
        toR = []
        for x in self.slots:
            # TODO: Actually resolve these friggin turns
            #toR += ["TURN "]
            i=0
            while x["actions"]:
                if i in x["actions"]:
                    for j in x["actions"][i]:
                        toR += [j]
                        #if j.split(" ")[0] == "MOVE":
                        #    _,x,y,dude = j.split(" ")
                        #    x["board"].units[int(dude)].queue_movements([(int(x),int(y))])
                        #if j.split(" ")[0] == "SHOOT":
                        #    _,dude = j.split(" ")
                        #    x["board"].units[int(dude)].queue_shoot()
                    del x["actions"][i]
                i += 1
            toR += ["END "]
            #x["board"].take_turn_server()
            
            #i = 0
            #to_send = []
            #while x["actions"]:
            #    if i in x["actions"]:
            #        to_send.append(x["actions"][i])
            #        del x["actions"][i]
            #    else:
            #        to_send.append("TURN")
            #    i += 1
            # x["actions"] = {}   # clear the actions
        for t in toR:
            print "networking.do_turns: Gimme a",t
            self.send_to_all(t) # TODO: Actually send the actions to everyone
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # work out all the turns and stuff
        for x in self.slots:    # next turns
            x["sent"] = False
    
    def generate_ai_turns(self, s):
        # TODO: AI players should make turns: DIS BENSON'S DOMAIN
        # Toggle the comments on the next two lines
        self.slots[s]["actions"][0] = []
        self.slots[s]["sent"] = True
        #self.set_sent(s)   # over and over and over and over
    
    def run(self):
        print "listening"
        self.server.listen(10)
        while not self.done:
            # list of socket objects from clients, plus the server socket
            inputs = [x["conn"] for x in self.slots if x.has_key("conn")] + [self.server]
            # blocks until someone connects or a client sends a message
            ready, _, _ = select.select(inputs, [], [], 0.5)
            if ready:
                print "ready: %s" % (ready,)
            for c in ready:
                print "processing message"
                if c == self.server:
                    if self.host == None:
                        conn, _ = c.accept()
                        self.host = conn
                        self.slots[0] = {"type":Server.PLAYER, "name":"Host", "ready":False, "conn":conn, "buffer":''}
                        conn.send(self.get_server_data(0) + RS)
                        print "it's a new connection!"
                    else:
                    # check slots
                        x = self.find_free_slot()
                        if x:
                            conn, _ = c.accept()
                            self.slots[x] = {"type":Server.PLAYER, "name":"Player " + str(x), "ready":False, "conn":conn, "buffer":''}
                            conn.send(self.get_server_data(x) + RS)
                            print "it's a new connection!"
                            self.send_to_all("JOIN " + str(x) + " Player " + str(x))
                        else:
                            conn, _ = c.accept()
                            conn.send("DIE There were no available slots in the game you attempted to join!" + RS)  # little harsh but alright
                            print "a player couldn't join due to lack of slots"
                            conn.close()
                else:
                    print "Message from a client"
                    # blocks on c (but select has told us that there's a
                    # message waiting, so there's no real blocking)
                    sender = self.get_sender(c)
                    go = True
                    while go:
                        while "buffer" in self.slots[sender] and self.slots[sender]["buffer"].find(RS) == -1:
                            message = self.slots[sender]["conn"].recv(MAX_PACKET_LENGTH)
                            if not message:
                                # an empty string indicates that the client has
                                # closed their connection
                                print "closed connection"
                                for i,x in enumerate(self.slots):
                                    if x.has_key("conn"):
                                        if x["conn"] == c:
                                            self.slots[i] = {"type":Server.OPEN}
                                            self.send_to_all("KICK " + str(i))
                                c.close()
                            else:
                                self.slots[sender]["buffer"] += message
                        if "buffer" not in self.slots[sender]:
                            continue
                        message, _, self.slots[sender]["buffer"] = self.slots[sender]["buffer"].partition(RS)
                        # echoes actual message to all players
                        cmdend = message.find(' ')
                        cmd = message[:cmdend]
                        args = message[cmdend+1:]
                        #print "\ncmd: "+cmd+"\nargs: "+args+"\n"
                        if cmd in self.commands:
                            self.commands[cmd](c, args)
                        else:
                            print cmd,"is not a command i'm aware of"
                        
                        
                        go = bool(self.slots[sender]["buffer"].find(RS)+1)  # loop if there's more messages :D :D :D
                        #print "go",go,", buffer is",self.slots[sender]["buffer"]
                        #message = str(self.connections.index(c)) + ": " + message
                        #for p in self.connections:
                        #    p.send(message)
        self.server.close()
        self.send_to_all("HOSTDEAD ")
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                x["conn"].close()
                self.slots[i] = {"type" : Server.CLOSED}

    def stop(self):
        self.done = True
    
    def find_free_slot(self):
        for x in xrange(10):
            if self.slots[x]["type"] == Server.OPEN:
                return x
        return False
    
    def get_server_data(self, slot):
        toR = "DATA " + str(slot)
        for x in self.slots:
            toR += "\n"
            toR += str(x["type"])
            if x["type"] == Server.PLAYER:
                toR += " " + str(int(x["ready"])) + " " + x["name"]
        return toR
    
    def get_sender(self, c):
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                if x["conn"] == c:
                    return i
    
    def send_to_all(self, message, exempt = None):
        buf = message + RS
        while buf:
            for x in self.slots:
                if x.has_key("conn"):
                    if x["conn"] != exempt:
                        x["conn"].send(buf[:MAX_PACKET_LENGTH])
            buf = buf[MAX_PACKET_LENGTH:]
    
    def send_message(self, c, message):
        self.send_to_all("MSG " + str(self.get_sender(c)) + " " + message, c)
    
    # TODO: DON'T USE ON PEOPLE. KICK EM FIRST
    def set_slot(self, c, message):
        if self.slots[0]["conn"] == c:
            slot, setting = int(message[0]), int(message[2])
            self.slots[slot]["type"] = setting
            self.send_to_all("NICK "+str(slot)+" "+str(setting))
    
    def change_name(self, c, message):
        sender = self.get_sender(c)
        for x in self.slots:
            if x["type"] == Server.PLAYER:
                if x["name"] == message:
                    self.slots[sender]["conn"].send("NICK " + str(sender) + " " + self.slots[sender]["name"] + RS)
                    return
        self.slots[sender]["name"] = message
        self.send_to_all("NICK " + str(sender) + " " + message)
    
    def set_ready(self, c, message):
        sender = self.get_sender(c)
        self.slots[sender]["ready"] = int(message)
        self.send_to_all("READY " + str(sender) + " " + message)
    
    def recv_actions(self, c, message):
        sender = self.get_sender(c)
        actions = pickle.loads(message)
        
        # TODO: this goes in another method, right now we're just unpickling, but we need everyone's data before we can go
        """b = self.slots[sender]["board"]
        cmds = {"BUY":b.buy_item, "UPGRADE":b.buy_upgrade, "SENT":b.send_offensive, "MOVE":b.move_peon, "SHOOT":b.shoot_unit, "SPECIAL":b.special_unit}
        for x in actions:
            splitter = x.find(" ")
            cmd,args = x[:splitter], x[splitters:]
            cmds[cmd](args)
        self.slots[sender]["return_actions"] = """
        
    def start_game(self, c, message):
        if self.slots[0]["conn"] == c:
            for x in self.slots:
                if x.has_key("ready"):
                    if not x["ready"]:
                        return
            ai_num = 1
            for x in self.slots:
                if x["type"] in [Server.PLAYER, Server.AI]: # "give them a board i guess" -- Dannenberg
                    self.game_slots.append({"type":x["type"], "buffer":'', "actions":{}, "sent":False, "index":0})
                    if x["type"] == Server.PLAYER:
                        self.game_slots[-1]["conn"] = x["conn"]
                        self.game_slots[-1]["name"] = x["name"]
                    else:
                        self.game_slots[-1]["name"] = AI_NAME+" "+str(ai_num)
                        ai_num += 1
                    self.game_slots[-1]["data"] = self.generate_board_data(self.game_slots[-1]["name"])
            self.slots = self.game_slots
            print "number of slots", len(self.slots)
            self.send_to_all("START "+str(random.randint(0,2**32-1))+" "+('\t'.join([x["name"] for x in self.slots])))
                    
    def generate_board_data(self, name):
        return {"board":Board(BOARD_SQUARES_X,BOARD_SQUARES_Y, name)}
    
    def kick_player(self, c, message):
        if self.slots[0]["conn"] == c:
            if self.slots[int(message)]["type"] == Server.PLAYER:
                self.send_to_all("KICK " + message)
                self.slots[int(message)]["conn"].close()
                self.slots[int(message)] = {"type":Server.OPEN}
            elif self.slots[int(message)]["type"] == Server.AI:
                self.send_to_all("KICK " + message)

class Client(threading.Thread):
    def __init__(self, host=None):
        if host is None:
            self.ADDR=(HOST, PORT)
        else:
            self.ADDR=(host, PORT)
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msgs = Queue()
        self.done = False
        self.recv_buf = ''
        
    def run(self):
        try:
            self.sock.connect(self.ADDR)
        except IOError:
            self.msgs.put("DIE Network Error: Probably a bad IP address.")
            return
        self.sock.settimeout(0.5)
        while not self.done:
            while not self.done and self.recv_buf.find(RS) == -1:
                try:
                    message = self.sock.recv(MAX_PACKET_LENGTH)
                except socket.timeout:
                    continue
                if not message:
                    # an empty string indicates that the client has
                    # closed their connection
                    print "closed connection"
                    self.done = True
                    self.sock.close()
                    break
                else:
                    self.recv_buf += message
            term, _, self.recv_buf = self.recv_buf.partition(RS) 
            self.process_message(term)

    def process_message(self, message):
        if message == '':
            self.done = True
            self.sock.close()
        self.msgs.put(message)
        
    def send(self, message):
        buf = message + RS
        while buf:
            self.sock.send(buf[:MAX_PACKET_LENGTH])
            buf = buf[MAX_PACKET_LENGTH:]
        
    def send_message(self, message):
        message = "MSG " + message
        self.send(message)
        
    def set_slot(self, slot, setting):
        message = "SLOT " + str(slot) + " " + str(setting)
        self.send(message)
        
    def kick_player(self, message):
        message = "KICK " + message
        self.send(message)
    
    def start_game(self):
        self.send("START ")
    
    def set_ready(self, message):
        message = "READY " + str(message)
        self.send(message)
        
    def send_board(self, board):
        message = "BOARD " + board
        self.send(message)
        
    def change_name(self, message):
        message = "NICK " + message
        self.send(message)
        
    def stop(self):
        self.done = True
        self.sock.close()

if __name__ == "__main__":
    if int(raw_input("Server? ")):
        s = Server()
        s.start()
    else:
        c = Client()
        c.start()
    while 1:
        try:
            exec(raw_input(">"))
        except:
            print "Bad input."
