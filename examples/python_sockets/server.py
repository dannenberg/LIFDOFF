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
players_lock = threading.Lock()
instream = Queue.Queue()    # Threadsafe queue

def accept_connections(stream):
    while 1:
        conn, addr = s.accept()    # blocking, waits for new connection
        print "Connecting "+str(addr)
        player_thread = threading.Thread(target=handler,args=(conn,addr,stream,)) 
        players_lock.acquire()
        players.append({"socket":(conn,addr), "thread":player_thread, "name":"player " + str(len(players)), "ready":False}) # add to playerlist
        players_lock.release()
        player_thread.start()   # start a thread for them to speak

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
            players_lock.acquire()
            players[:] = [player for player in players if player["socket"] != (conn,addr)]
            players_lock.release()
            done = True

# allow people to connect
connect_thread = threading.Thread(target=accept_connections,args=(instream,))
connect_thread.start()

done = False

while not done:
    try:
        if not instream.empty():    # if new messages
            dat = instream.get()    # get a message
            print dat               # post it to server
            players_lock.acquire()
            for player in players:       # send it to all players
                player["socket"][0].send(dat)      # Burma Shave
            players_lock.release()
    except KeyboardInterrupt:
        connect_thread._Thread__stop() # kill the thread allowing connections so thi will actually quit
        done = True                    # given all the _ this may be dangerous...
        s.close()
        players_lock.acquire()
        for player in players:
            player["thread"]._Thread__stop()
            player["socket"][0].shutdown(1)
            player["socket"][0].close()
        players_lock.release()
