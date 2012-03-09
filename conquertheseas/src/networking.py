import socket
import select
import threading
from Queue import Queue

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
        self.commands = {
            "MSG" : self.send_message,
            "NICK" : self.change_name,
            "SLOT" : self.set_slot,
            "READY" : self.set_ready,
            "START" : self.start_game,
            "KICK" : self.kick_player
            }
        
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
                        self.slots[0] = {"type":Server.PLAYER, "name":"Host", "ready":False, "conn":conn}
                        conn.send("Welcome to the game, you're the host!")
                        print "it's a new connection!"
                    else:
                    # check slots
                        x = self.find_free_slot()
                        if x:
                            conn, _ = c.accept()
                            self.slots[x] = {"type":Server.PLAYER, "name":"Player " + str(x), "ready":False, "conn":conn}
                            conn.send(self.get_server_data(x))
                            print "it's a new connection!"
                            self.send_to_all("JOIN " + str(x) + " Player " + str(x))
                        else:
                            conn, _ = c.accept()
                            conn.send("Sorry, server is full!")
                            print "a player couldn't join due to lack of slots"
                            conn.close()
                                        
                else:
                    print "Message from a client"
                    # blocks on c (but select has told us that there's a
                    # message waiting, so there's no real blocking)
                    message = c.recv(255)
                    print "received message: '%s'" % (message,)
                    if not message:
                        # an empty string indicates that the client has
                        # closed their connection
                        print "closed connection"
                        for i,x in enumerate(self.slots):
                            if x.has_key("conn"):
                                if x["conn"] == c:
                                    self.slots[i] = {"type":Server.OPEN}
                        c.close()
                    else:
                        # echoes actual message to all players   
                        cmdend = message.find(' ')
                        cmd = message[:cmdend]
                        args = message[cmdend+1:]
                        #print addr+"\ncmd: "+cmd+"\nargs: "+args+"\n"
                        self.commands[cmd](c, args)
                        #message = str(self.connections.index(c)) + ": " + message
                        #for p in self.connections:
                        #    p.send(message)
        self.server.close()
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
        for x in self.slots:
            if x.has_key("conn"):
                if x["conn"] != exempt:
                    x["conn"].send(message)
        
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
                    self.slots[sender]["conn"].send("That name is already taken")
                    return
        self.slots[sender]["name"] = message
        self.send_to_all("NICK " + str(sender) + " " + message)
                    
    def set_ready(self, c, message):
        sender = self.get_sender(c)
        self.slots[sender]["ready"] = int(message)
        self.send_to_all("READY " + str(sender) + " " + message)
                    
    def start_game(self, c, message):
        if self.slots[0]["conn"] == c:
            for x in self.slots:
                if x.has_key("ready"):
                    if not x["ready"]:
                        return
        self.send_to_all("START")
                    
    def kick_player(self, c, message):
        if self.slots[0]["conn"] == c:
            if self.slots[int(message)]["type"] == Server.PLAYER:
                self.send_to_all("KICK" + message)
                self.slots[int(message)]["conn"].close()
                self.slots[int(message)] = {"type":Server.OPEN}
            elif self.slots[int(message)]["type"] == Server.AI:
                self.send_to_all("KICK" + message)

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
        
    def run(self):
        self.sock.connect(self.ADDR)
        self.sock.settimeout(0.5)
        while not self.done:
            try:
                message = self.sock.recv(255)
            except socket.timeout:
                continue
            if not message:
                # an empty string indicates that the client has
                # closed their connection
                print "closed connection"
                self.done = True
                self.sock.close()
            else:
                self.process_message(message)

    def process_message(self, message):
        if message == '':
            self.done = True
            self.sock.close()
        self.msgs.put(message)
        
    def send(self, message):
        self.sock.send(message[:255])
        
    def send_message(self, message):
        message = "MSG " + message
        self.send(message)
        
    def set_slot(self, slot, setting):
        message = "SLOT " + str(slot) + " " + str(setting)
        self.send(message)
        
    def kick_player(self, message):
        message = "KICK " + message
        self.send(message)
    
    def start_game(self, _):
        self.send("START")
    
    def set_ready(self, message):
        message = "READY " + str(message)
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
            print "You have fucked up."
