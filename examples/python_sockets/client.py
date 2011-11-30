import socket
import threading

HOST = "127.0.0.1"
PORT = 11151

s=socket.socket( )
s.connect((HOST, PORT))

def handler(s):
    while 1:
        readbuffer=s.recv(1024) # get new data
        if readbuffer:
            print readbuffer

text = ""
threading.Thread(target=handler,args=(s,)).start()  # create a new thread to handle input from server
while text!="/quit":    # input TO server
    text = raw_input(">")   # blocking
    s.send(text+"\r\n")
