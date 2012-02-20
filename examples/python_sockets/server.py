import socket
import threading
import Queue

HOST = socket.gethostname()
PORT = 11151

print HOST
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # this is just standard, don't touch
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # ???
s.bind((HOST, PORT))
s.listen(5) # n people may connect. does not appear to work?

players = []
instream = Queue.Queue()    # Threadsafe queue

def accept_connections(players,stream):
    while 1:
        conn, addr = s.accept()    # blocking, waits for new connection
        print "Connecting "+str(addr)
        players.append((conn,addr)) # add to playerlist
        threading.Thread(target=handler,args=(conn,addr,stream)).start()    # start a thread for them to speak

def handler(conn,addr,stream):
    done = False
    while not done:
        data = conn.recv(1024)  # see what the player says
        if data:
            toR = str(addr)+":"+data    # compile the message
            stream.put(toR)             # post to the queue, for propogation later.
        else:
            conn.shutdown(1)
            conn.close()
            players.remove((conn,addr))
            done = True

# allow people to connect
threading.Thread(target=accept_connections,args=(players,instream)).start()

while 1:
    if not instream.empty():    # if new messages
        dat = instream.get()    # get a message
        print dat               # post it to server
        for x in players:       # send it to all players
            x[0].send(dat)      # Burma Shave
