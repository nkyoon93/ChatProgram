import socket

HOST = 'localhost'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#소켓객체생성,AF_는asocket의 첫번쨰 인자에 사용되는 주소, SOCK는 socketkind-TCP
client_socket.connect((HOST, PORT))
#서버에connect로 접속
client_socket.sendall('helloworld'. encode())
#소켓에 데이터를보내는 sendall함수로 메세지를 보냄)
data = client_socket.recv(1024)
print('수신', repr(data.decode()))
#서버의 수신메세지 출력
client_socket.close()