class CarrotMaker:
    def __init__(self):
        self.database = "carot"



# client.py (수정된 버전)
import socket

# 서버 IP 및 포트
HOST = "192.168.0.56"
PORT = 8080

# 소켓 생성 및 서버 연결
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# 보낼 문자열 (예: 명령어 또는 메시지)
message = "hello"

# 문자열 전송
client.sendall(message.encode())

# 서버 응답 받기
response = client.recv(1024)
print("[서버 응답]", response.decode())

# 소켓 종료
client.close()
