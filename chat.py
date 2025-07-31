# ✅ 채팅
import socket
import pymysql
import time # 채팅시간 저장
from datetime import datetime
import threading



# 상수 처리
HOST = '192.168.0.56'
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

    # ☑️ 시간 확인 함수(메시지 관련) ex)오전, 00시 00분
    def time_check(self):
        t = time.localtime()
        tc = ""
        if t.tm_hour < 12:
            tc = "오전"
        else:
            tc = "오후"
        check_time = time.strftime("%I시 %M분", t)  # I시(01 ~ 12)
        tc += "," + check_time
        return tc

    # ☑️ 보낸 메시지
    def sendmessage(self):
        while True:
            # "사용자 채팅 입력"
            send_ms = input("보낼 메세지 입력 : ")

            # "채팅방 나가기" 연결
            if send_ms == 'exit':
                print("채팅 종료")
                sock.shutdown(socket.SHUT_RDWR) # RD(소켓통신차단), WR(소켓송신차단), RDWR(송수신차단)
                sock.close()
                break

            # "보내기" 연결
            send_total = send_ms
            nowtime = self.time_check() # 시간저장
            send_total += "," + nowtime
            sock.send(send_total.encode("utf-8"))

            # SQL 수정
            try:
                chat_content = "INSERT INTO CHAT (content, date) VALUES (%s, %s)"
                cur.execute(chat_content, (send_ms,nowtime))
                conn.commit() # DB 반영
            except Exception as e:
                print("오류! 오류 원인 : ",e)

            # 메시지 리스트 저장
            self.content.append(["sender",send_ms, nowtime]) # 2중 리스트

    # ☑️ 받은 메시지
    def receiveMessage(self):
        while True:
            try:
                recv_ms = sock.recv(8192).decode("utf-8")
                nowtime = self.time_check()  # 시간저장
                # 메시지 리스트 저장
                self.content.append(["receiver", recv_ms, nowtime])  # 2중 리스트
            except Exception: # 보내는 메시지가 exit 하면 종료
                print("채팅 종료")
                break

    # ☑️ 스레드 연결 / 채팅 시작
    def start_chat(self):
        sender = threading.Thread(target=self.sendmessage)
        receiver = threading.Thread(target=self.receiveMessage)
        sender.start()
        receiver.start()

    # ☑️ 약속잡기 ()
    def promise(self):
        time = self.time_check()
        week = datetime.today().weekday() # 오늘의 요일
        loc = input("주소를 입력하세요 : ")
        total = [time,week,loc]
        return total







"""
chat_num
sell_id
user_id

채팅방 ID 에
sll_ID 와 각 유저의 ID 필요
"""