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

def send_message(addr, message):
    print message
    players_lock.acquire()
    for player in players:
        if str(player["socket"][1]) != addr:
            player["socket"][0].send(message)
    players_lock.release()

def change_name(addr, message):
    players_lock.acquire()
    for player in players:
        if str(player["socket"][1]) == addr:
            player["name"] = message
            print player["name"]
            player["socket"][0].send("your name is now " + str(player["name"]))
    players_lock.release()

def toggle_readiness(addr, message):
    players_lock.acquire()
    for player in players:
        if str(player["socket"][1]) == addr:
            player["ready"] = not player["ready"]
            if player["ready"]:
                player["socket"][0].send("you're ready")
            else:
                player["socket"][0].send("you're not ready")
    players_lock.release()

commands = { 
            "MSG" : send_message,
            "NAME" : change_name,
            "READY" : toggle_readiness
            }

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
        else:                           # player gone, so close the connection and remove em from the list
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
            colonloc = dat.find(':')               # this parsing is pretty ugly feel free to pretty it up 
            cmdend = colonloc+1+dat[colonloc:].find(' ')
            addr = dat[0:colonloc]
            cmd = dat[colonloc+1:cmdend-1]
            args = dat[cmdend:]
            #print addr+"\ncmd: "+cmd+"\nargs: "+args+"\n"
            commands[cmd](addr, args)
    except KeyboardInterrupt:
        connect_thread._Thread__stop() # kill the thread allowing connections so this will actually quit
        done = True                    # given all the _ this may be dangerous...
        s.close()
        players_lock.acquire()         # close all the player connections
        for player in players:
            player["thread"]._Thread__stop()
            player["socket"][0].shutdown(1)
            player["socket"][0].close()
        players_lock.release()
