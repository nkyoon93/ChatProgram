import socket
import threading
HOST = 'localhost'
PORT = 5001
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(1)
conn, addr = socket.accept()
print('연결', addr)
def sendingMsg():
    while True:
        data = input()
        data = data.encode("utf-8")
        conn.send(data)
    conn.close()
def gettingMsg():
    while True:
        data = conn.recv(1024)
        if not data:
                break
        else:
               data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
               print(data)
    conn.close()

threading._start_new_thread(sendingMsg,())
threading._start_new_thread(gettingMsg,())
while True:
    pass

