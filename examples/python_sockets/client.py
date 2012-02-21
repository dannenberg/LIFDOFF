import socket
import threading

HOST = socket.gethostname()
PORT = 11151

s=socket.socket( )
s.connect((HOST, PORT))

done = False

def handler(s):
    while not done:
        readbuffer=s.recv(1024) # get new data
        if readbuffer:
            print readbuffer

text = ""
threading.Thread(target=handler,args=(s,)).start()  # create a new thread to handle input from server

while not done:    # input TO server
    try:
        text = raw_input(">")   # blocking
        if text == "/quit":
            done = True
        else:
            s.send("MSG "+text+"\r\n")
    except KeyboardInterrupt:
        done = True

s.shutdown(1)
s.close()
