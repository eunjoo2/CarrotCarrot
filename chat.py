# ✅ 채팅
import socket
import pymysql
import time # 채팅시간 저장
import threading

send_time, recv_time = "",""

# 상수 처리
HOST = '192.168.0.69'
PORT = 8080

# 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# 커서 생성
conn = pymysql.connect(user='root', password='0000', db='carrot', charset='utf8')
cur = conn.cursor()


# ✅ 채팅방 클래스
class Chat:
    def __init__(self, id, buyer, seller, product, date, read_check, content):
        self.id = id # 🍪 00001 ... int
        self.buyer = buyer # 카테고리(구매) 구분을 위함 # 🍪 "포립 님" ... str
        self.seller = seller # 카테고리(판매) 구분을 위함 # 🍪 "수리 님" ... str
        self.product = product # 상품 # 🍪 '한화 이글스 유니폼' ... str
        self.date = date # 🍪 '년 / 월 / 일' ... str
        self.read_check = read_check # 카테고리(안 읽은 채팅방) 구분을 위함 # 🍪 False(안읽음) ... bool
        self.content = content  # 🍪 메시지 보관

    # ☑️ 보낸 메시지
    def sendmessage(self):
        global send_time
        while True:
            # "사용자 채팅 입력"
            send_ms = input("보낼 메세지 입력 : ")

            # "채팅방 나가기" 연결
            if send_ms == 'exit':
                print("채팅 종료")
                break

            # "보내기" 연결
            sock.send(send_ms.encode("utf-8"))

            # 보낸 시간
            t = time.localtime()
            if t.tm_hour < 12:
                send_time = "오전"
            else:
                send_time = "오후"
            check_time = time.strftime("%I시 %M분", t) # I시(01 ~ 12)
            send_time += check_time

            # SQL 수정
            try:
                chat_content = "INSERT INTO CHAT (content, date) VALUES (%s, %s)"
                cur.execute(chat_content, (send_ms,send_time))
                conn.commit() # DB 반영
            except Exception as e:
                print("오류! 오류 원인 : ",e)

            # 메시지 리스트 저장
            self.content.append([send_ms, send_time]) # 2중 리스트

    # ☑️ 받은 메시지
    def receiveMessage(self):
        global recv_time
        while True:
            recv_ms = sock.recv(8192).decode("utf-8")

            # 받은 시간
            t = time.localtime()
            if t.tm_hour < 12:
                recv_time = "오전"
            else:
                recv_time = "오후"
            check_time = time.strftime("%I시 %M분", t)  # I시(01 ~ 12)
            recv_time += check_time

            # 메시지 리스트 저장
            self.content.append([recv_ms, recv_time])  # 2중 리스트

    # 스레드 연결 / 채팅 시작
    def start_chat(self):
        sender = threading.Thread(target=self.sendmessage)
        receiver = threading.Thread(target=self.receiveMessage)
        sender.start()
        receiver.start()

    def promise(self):
        pass







"""
chat_num
sell_id
user_id

채팅방 ID 에
sll_ID 와 각 유저의 ID 필요
"""