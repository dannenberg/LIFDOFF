import socket
import select
import threading

ADDR = ('localhost', 2424)

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.connections = []

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
                    print "it's a new connection!"
                    conn, _ = c.accept()
                    # sends welcome banner
                    conn.send('sup')
                    self.connections.append(conn)
                else:
                    print "you've got mail!"
                    # blocks on c (but select has told us that there's a
                    # message waiting, so there's no real blocking)
                    message = c.recv(255)
                    print "received message: '%s'" % (message,)
                    if not message:
                        # an empty string indicates that the client has
                        # closed their connection
                        c.close()
                        del(self.connections[self.connections.index(c)])
                    else:
                        # echoes actual message
                        c.send(message)

    def stop(self):
        self.server.close()
        del(self.connections)

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.connect(ADDR)
        # receives welcome banner
        banner = self.sock.recv(255)
        print "got banner: '%s'" % (banner,)

    def send(self, message):
        self.sock.send(message[:255])
        reply = self.sock.recv(255)
        print "got reply: '%s'" % (reply,)

    def stop(self):
        self.sock.close()
