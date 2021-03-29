import socket
import threading
HOST = "localhost"
PORT = 9999
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

def sendingMsg():
       while True:
           data = input()
           data = bytes(data, "utf-8")
           socket.send(data)
def gettingMsg():
    while True:
        data = socket.recv(1024)
        data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
        print(data)

threading._start_new_thread(sendingMsg,())
threading._start_new_thread(gettingMsg,())
while True: pass

