# ✅ 채팅
import socket
import pymysql
import time # 채팅시간 저장
import threading

t = time.localtime()
send_time = ""

# 상수 처리
HOST = '192.168.0.69'
PORT = 8080

# 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 커서 생성
conn = pymysql.connect(user='root', password='0000', db='carrot', charset='utf8')
cur = conn.cursor()



# ✅ 채팅방 클래스
class Chat:
    def __init__(self, id, buyer, seller, product, message):
        self.id = id
        self.buyer = buyer
        self.seller = seller
        self.product = product # 상품
        self.message = [] # 메시지

    # 메시지 보내기
    def sendmessage(self, id, message):
        global send_time
        while True:
            # "사용자 채팅 입력"
            msg = input("보낼 메세지 입력 : ")

            # "채팅방 나가기" 연결
            if msg == 'exit':
                print("채팅 종료")
                break

            # "보내기" 연결
            client_socket.send(msg.encode())

            # 보낸 시간
            if t.tm_hour < 12:
                send_time = "오전"
            else:
                send_time = "오후"
            check_time = time.strftime("%I시 %M분", t) # I시(01 ~ 12)
            send_time += check_time

            # SQL 수정
            chat_content = "INSERT INTO CHAT (content, date) VALUES (%s, %s)"

            cur.execute(chat_content, (msg,send_time)) # 보낸 내용 DB 저장

    def receiveMessage(self):
        global send_time
        while True:
            # "사용자 채팅 입력"
            msg = input("보낼 메세지 입력 : ")

            # "채팅방 나가기" 연결
            if msg == 'exit':
                break

# 스레드 연결
sender = threading.Thread(target=Chat.sendmessage, args=(client_socket,))
receiver = threading.Thread(target=Chat.receiveMessage, args=(client_socket,))



"""
chat_num
sell_id
user_id

채팅방 ID 에
sll_ID 와 각 유저의 ID 필요
"""