import socket
from socket import SHUT_RDWR
import sys
import threading

HOST = socket.gethostname()
PORT = 11151

s=socket.socket( )
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.connect((HOST, PORT))

done = False

def handler(s):
    global done
    while not done:
        try:
            readbuffer=s.recv(1024) # get new data
            if readbuffer:
                print readbuffer
        except Exception:
            done = True
            s.close()

text = ""
threading.Thread(target=handler,args=(s,)).start()  # create a new thread to handle input from server

while not done:    # input TO server
    try:
        text = raw_input(">")   # blocking
        if text == "/quit":
            done = True
        elif text == "/ready":
            s.send("READY "+"\r\n")
        elif text.startswith("/kick"):
            s.send("KICK "+text[6:]+"\r\n")
        elif text.startswith("/name"):
            s.send("NAME "+text[6:]+"\r\n")
        else:
            s.send("MSG "+text+"\r\n")
    except Exception, KeyboardInterrupt:
        done = True
        s.shutdown(SHUT_RDWR)
        s.close()
        sys.exit(0)
