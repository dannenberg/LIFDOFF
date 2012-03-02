import socket
import select
import threading

HOST = socket.gethostname()
PORT = 11170
ADDR = (HOST,PORT)

class Server(threading.Thread):
    PLAYER = 0
    CLOSED = 1
    OPEN = 2
    AI = 3

    def __init__(self):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.connections = []
        self.slots = [{"type":Server.OPEN} for _ in xrange(10)] # TODO: CHANGE THIS TO CLOSED
        self.host = None
        self.commands = {
            "MSG" : self.send_message,
            "NICK" : self.change_name,
            "READY" : self.toggle_readiness,
            "START" : self.start_game,
            "KICK" : self.kick_player
            }
            
 
        
    def run(self):
        print "listening"
        self.server.listen(5)
        while 1:
            # list of socket objects from clients, plus the server socket
            inputs = self.connections + [self.server]
            # blocks until someone connects or a client sends a message
            ready, _, _ = select.select(inputs, [], [])
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
                        self.connections.append(conn)
                    else:
                    # check slots
                        for x in xrange(10):
                            if self.slots[x]["type"] == Server.OPEN:
                                conn, _ = c.accept()
                                self.slots[x] = {"type":Server.PLAYER, "name":"Player " + str(x), "ready":False, "conn":conn}
                                conn.send(self.get_server_data(x))
                                print "it's a new connection!"
                                self.connections.append(conn)
                                for i in self.slots:
                                    if i.has_key("conn"):
                                        i["conn"].send("JOIN " + str(x) + " Player " + str(x))
                                break
                            if x == 9:
                                conn, _ = c.accept()
                                conn.send("Sorry, server is full!")
                                print "it's a new connection!"
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
                        c.close()
                        del(self.connections[self.connections.index(c)])
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

    def stop(self):
        self.server.close()
        del(self.connections)
        
    def get_server_data(self, slot):
        toR = "DATA " + str(slot) + "\n"
        for x in self.slots:
            toR += str(x["type"])
            if x["type"] == Server.PLAYER:
                toR += " " + str(int(x["ready"])) + " " + x["name"]
            toR += "\n"
        return toR  
        
    def send_message(self, c, message):
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                if x["conn"] == c:
                    sender = i
        message = "MSG " + str(sender) + " " + message
        for x in self.slots:
            if x.has_key("conn"):
                if x["conn"] == c:
                    pass
                else:
                    x["conn"].send(message)
                    
    def change_name(self, c, message):
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                if x["conn"] == c:
                    sender = i
                    x["name"] = message
        message = "NICK " + str(sender) + " " + message
        for x in self.slots:
            if x.has_key("conn"):
                if x["conn"] == c:
                    pass
                else:
                    x["conn"].send(message)
                    
    def toggle_readiness(self, c, message):
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                if x["conn"] == c:
                    sender = i
                    x["ready"] = not x["ready"]
        message = "READY " + str(sender) + " " + str(int(self.slots[sender]["ready"]))
        for x in self.slots:
            if x.has_key("conn"):
                if x["conn"] == c:
                    pass
                else:
                    x["conn"].send(message)
                    
    def start_game(self, c, message):
        if self.slots[0]["conn"] == c:
            for x in self.slots:
                if x.has_key("ready"):
                    if not x["ready"]:
                        return
        for x in self.slots:
            if x.has_key("conn"):
                x["conn"].send("START")
                    
    def kick_player(self, c, message):
        if self.slots[0]["conn"] == c:
            if self.slots[int(message)]["type"] == Server.PLAYER:
                self.slots[int(message)]["conn"].close()
                for x in self.slots:
                    if x.has_key("conn"):
                        x["conn"].send("KICK " + message)
            elif self.slots[int(message)]["type"] == Server.AI:
                for x in self.slots:
                    if x.has_key("conn"):
                        x["conn"].send("KICK " + message)
                

class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def run(self):
        #print "nigga made a pizza"
        self.sock.connect(ADDR)
        while 1:
            #print "nigga made aWHIEL LOOP pizza"
            self.process_message(self.sock.recv(255))
        
    def process_message(self, message):
        # dannenberg loves cocks in his body
        if message == '':
            self.sock.close()
        print message
        

    def send(self, message):
        self.sock.send(message[:255])
        
    def send_message(self, message):
        message = "MSG " + message
        self.send(message)
        
    def kick_player(self, message):
        message = "KICK " + message
        self.send(message)
    
    def start_game(self, message):
        message = "START " + message
        self.send(message)
    
    def toggle_readiness(self, message):
        message = "READY " + message
        self.send(message)
        
    def change_name(self, message):
        message = "NICK " + message
        self.send(message)
        
    def stop(self):
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
