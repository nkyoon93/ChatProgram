import socket
import select
import sys

addr = ('localhost', 5001)
PORT = 5001 # server_client port
ROOM_PORT = 9999 #my_room_port
HOST = 'localhost'
UDP_PORT = 5002 #kill_room port

nicknames = []
socket_list = []
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket_list = {}


udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsocket.bind(("localhost",5002))

def send():
    while True:
        data = input()
        data = bytes(data, "utf-8")
        client_socket.send(data)

def recv():
    while True:
        data = client_socket.recv(1024).decode() #서버->클라로데이터수신
        data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
        print(data)

def make_room(client_socket, msg):
    client_socket.sendall("1".encode())

    if client_socket.recv(1024).decode() == '0':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(4)
        socket_list.append(server_socket)
        room_name = msg[0:]
        client_socket.send(room_name.encode())
        print('room created')
        read_socket_list = [sys.stdin, server_socket,udpsocket]
        nick_list = {}

        while True:
            conn_read_socket_list, conn_write_socket_list, conn_except_socket_list = select.select(read_socket_list, [],[])
            for conn_read_socket in conn_read_socket_list:

                if conn_read_socket == server_socket:
                    print("connecting...")
                    client_socket, addr = server_socket.accept()
                    nickname = client_socket.recv(1024)
                    socket_list.append(client_socket)

                    print("%s connected!" %addr)
                    print("name: " + nickname.decode())

                    if not client_socket :
                        print('connect X')
                        return 0

                    server_client_socket, client_addr == server_socket.accept()
                    nickname = server_client_socket.recv(1024)

                    client_socket_ip, client_socket_port = str(client_addr[0]), str(client_addr[1])
                    print("{}:{} join".format(client_socket_ip, client_socket_port))
                    read_socket_list.append(server_client_socket)
                    client_socket_list[client_socket_ip + ":" + client_socket_port] = server_socket
                    nick_list[client_socket_ip + ":" + client_socket_port] = nickname.decode()

                elif conn_read_socket == udpsocket:
                    udpsocket.close()
                    for client_socket in client_socket_list.values():
                        client_socket.send("kill".encode())
                    print("kill room")
                    server_socket.close()
                    return 0

                elif conn_read_socket in list(client_socket_list.values()):
                    client_ip, client_port = conn_read_socket.nicknames()
                    data = conn_read_socket.recv(1024)

                    if (not data) or (data.decode() == "/exit"):
                        read_socket_list.remove(conn_read_socket)
                        del client_socket_list[client_ip + ":" + str(client_port)]
                        conn_read_socket.close()
                        print(client_ip + ":" + str(client_port) + " disconneted.")
                    break

                    nickname = client_socket_list[client_id + ":" + str(HOST + ":" + PORT)]
                    print(nickname + " : " + data.decode())
                    for client_socket in client_socket_list.keys():
                        if (client_id + ":" + str(client_port)) != client_socket:
                            msg = nickname + " : " + data.decode()
                    client_socket_list[client_socket].send(msg.encode())


    else:
        print("failed make room")

def show_list(client_socket):
    client_socket.send("2".encode())
    data = client_socket.recv(1024)
    print("####Room List###\n" + data.decode())

def join_room(client_socket, msg):
    client_socket.send("3".encode())
    if client_socket.recv(1024).decode() == "0":
        room_name = msg[6:]
        client_socket.send(room_name.encode())
        room_info = client_socket.recv(1024).decode()
    if room_info != "fail":
        room_info = room_info.split(":")[0]

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((room_info, PORT))
        q = 0
        while (q != "yes") and (q != "no"):
            q = input("nickname? yes or no\n==>")

        if q == "yes":
            nick = input("==> ")
            server_socket.send(nick.encode())
        else:
            server_socket.send("unknown".encode())

        room_socket_list = [sys.stdin, server_socket]
        while True:
            room_read_list, room_write_socket_list, room_except_socket_list = select.select(room_socket_list, [], [])
            for room_read_socket in room_read_list:
                if room_read_socket == sys.stdin:
                    msg = room_read_socket.readline()
                    server_socket.send(msg.encode())
                else:
                    data = server_socket.recv(1024).decode()
                    print(data)
    else:
        print("no room")




if __name__ == "__main__":

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    read_socket_list = [sys.stdin, client_socket] #read socket list
    command_dict = {"/create": 1, "/ls": 2}

    while True:
        if len(read_socket_list) != 1:
            conn_read_socket_list,conn_write_socket_list,conn_except_socket_list=select.select(read_socket_list,[],[])

            for conn_read_socket in conn_read_socket_list:
                if conn_read_socket == sys.stdin:
                      msg = conn_read_socket.readline()
                      if msg.split(" ")[0] == "/create":
                          make_room(client_socket, msg)

                      elif msg.split(" ")[0] == "/ls\n" or msg.split(" ")[0] == "/ls":
                           show_list(client_socket)

                      elif msg.split(" ")[0] == "/join":
                           join_room(client_socket, msg)

                      elif msg.split(" ")[0] == '/exit':
                           client_socket.send("/exit".encode())
                           read_socket_list.remove(client_socket)
                           client_socket.close()
                           break

