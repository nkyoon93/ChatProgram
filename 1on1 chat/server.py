import socket #클라이언트
HOST = 'localhost'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#TCP프로토콜 지정,socket.socket함수로 소켓 객체 생성

server_socket.bind((HOST, PORT))
#소켓을 포트번호와 연결해주는 bind함수
server_socket.listen(1)
print('대기')
#서버가 클라이언트의 접속을 허용시켜주는 함수
client_socket, addr = server_socket.accept()
#accept함수에서 대기하다가 client가run하면 새 소켓을 리턴
print('연결:', addr)

while True:
    data = client_socket.recv(1024)
    #클라이언트 수신위해 대기
    if not data:
        break

    print('수신:', addr, data.decode())

client_socker.close()
server_socket.close()



