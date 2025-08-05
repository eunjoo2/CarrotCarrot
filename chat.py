

from header import Header
from bottom import bottom
from opening import Opening
from arealife_page import AreaLifePage
from arealife import AreaLifeBoard
from User import User

import tkinter as tk
#🍪🍪🍪
from tkinter import ttk
#🍪🍪🍪
import datetime


class CarrotMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")

        self.stage = 0  # 앱 실행 초기 화면 판단용 (예: 오프닝 로고)

        # 사용자 및 게시판 생성
        self.user = User(user_id="u001", nick_name="민기", area_name="서울", phone_num="010-1111-2222", temper=36.5, block_list=[], bad_count=0)
        self.board = AreaLifeBoard()

        # 상단 헤더 생성
        self.header = Header(self.root)

        # 바디 프레임 생성
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        # 오프닝 화면 처리
        if self.stage == 0:
            self.logo_view = Opening(self.body_frame)
            self.root.after(3000, self.go_to_next_stage)

        # 하단 네비게이션 바 생성
        self.bottom = bottom(self.root, self.show_page)

    def go_to_next_stage(self):
        self.logo_view.destroy()
        self.show_page("홈")

    def show_page(self, name):
        # 기존 body_frame 제거 후 새로 생성
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg=self.get_page_color(name))
        # self.body_frame = tk.Frame(self.root, bg=“white") # get_page_color 함수 지우면 이거 활성화
        self.body_frame.pack(expand=True, fill="both")

        # 헤더 타이틀 변경
        self.header.update_title(name)

        # 페이지 조건별 분기
        if name == "홈":
            tk.Label(self.body_frame, text="홈 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        elif name == "동네생활":
            AreaLifePage(self.body_frame, self.board, self.user)  # 따로 pack 필요 없음 (내부에서 구현됨)

        elif name == "동네지도":
            tk.Label(self.body_frame, text="동네지도 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        elif name == "채팅":
            Chat_list(self.body_frame, self.user, self.chat_content)

        elif name == "나의당근":
            tk.Label(self.body_frame, text="나의 당근 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        else:
            tk.Label(self.body_frame, text="[오류] 페이지를 찾을 수 없습니다.", font=("Arial", 12), bg="#FFCCCC").pack(pady=20)

    def get_page_color(self, name):
        colors = {
            "홈": "#FFFFFF",
            "동네생활": "#FFFACD",
            "동네지도": "#E0FFE0",
            "채팅": "#E0F0FF",
            "나의당근": "#000000"
        }
        return colors.get(name, "#FFFFFF")

    # 채팅방 진입 시
    def chat_content(self, room_info):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title(room_info["nickname"])
        self.header.back_button(self.back_chat)

        Chat_page(self.body_frame, self.user, room_info)

    def back_chat(self):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title("채팅 목록")
        self.header.back_button(None)

        Chat_list(self.body_frame, self.user, self.chat_content)

CHATTING = {} # 채팅메시지

class Chat:
    def __init__(self, id, buyer, seller, product, date, content):
        self.id = id # 🍪 00001 ... int
        self.buyer = buyer # 카테고리(구매) 구분을 위함 # 🍪 "포립 님" ... str
        self.seller = seller # 카테고리(판매) 구분을 위함 # 🍪 "수리 님" ... str
        self.product = product # 상품 # 🍪 '한화 이글스 유니폼' ... str
        self.date = date # 🍪 '년 / 월 / 일' ... str
        self.content = content  # 🍪 메시지 보관

        self.read_check = False  # 카테고리(안 읽은 채팅방) 구분을 위함 # 🍪 False(안읽음) ... bool




class Chat_page:
    def __init__(self, parent, user, room_id):
        self.parent = parent
        self.user = user
        self.room_id = room_id
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(expand=True, fill="both")
        # self.msgs = []

        self.room_key = str(room_id["room_id"])
        if self.room_key not in CHATTING:
            CHATTING[self.room_key] = []
        self.msgs = CHATTING[self.room_key]


        # 채팅방 진입 시 "게시물이름 채팅방"
        tk.Label(self.frame, text=f"[{room_id['title']}] 채팅방", font=("맑은 고딕", 13)).pack(pady=5)

        # # 텍스트 박스
        # self.text_area = tk.Text(self.frame, height=20, state="disabled", bg="#F5F5F5")
        # self.text_area.pack(padx=10, pady=10, fill="both", expand=True)
        #
        # self.entry = tk.Entry(self.frame)
        # self.entry.pack(side="left", padx=10, pady=5, fill="x", expand=True)
        # self.entry.bind("<Return>", self.send_message)
        #
        # self.send_button = tk.Button(self.frame, text="전송", command=self.send_message)
        # self.send_button.pack(side="right", padx=10, pady=5)
        #-------------------


        self.canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.msg_frame = tk.Frame(self.canvas, bg="white")

        self.msg_frame.bind("<Configure>",
                            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.msg_frame, anchor="nw")

        self.canvas.pack_propagate(False) # 캔버스 크기가 내용에 맞게 줄지 않도록
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 하단 입력창
        entry_frame = tk.Frame(self.frame, bg="white")
        entry_frame.pack(fill="x", pady=5)

        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side="left", padx=10, fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(entry_frame, text="전송", command=self.send_message)
        self.send_button.pack(side="right", padx=10)

        # 메시지 띄우기
        self.display_message()

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            now = datetime.datetime.now().strftime("%H:%M")
            formatted_msg = {
                "sender": self.user.nickname,
                "text": msg,
                "time": now,
            }
            # f"{self.user.nick_name}: {msg}"
            self.msgs.append(formatted_msg) # 메시지 저장🍪🍪🍪🍪
            self.display_single_message(formatted_msg)
            self.entry.delete(0, tk.END)

    # def append_text(self, msg):
    #     self.text_area.config(state="normal")
    #     self.text_area.insert(tk.END, msg + "\n")
    #     self.text_area.config(state="disabled")
    #     self.text_area.see(tk.END)

    def display_message(self):
        for msg in self.msgs:
            self.display_single_message(msg)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def display_single_message(self, msg):
        is_me = (msg["sender"] == self.user.nickname)
        bubble_frame = tk.Frame(self.msg_frame, bg="white", pady=2)


        anchor = "e" if is_me else "w"
        padx = (50, 10) if is_me else (10, 50)
        bubble_frame.pack(anchor=anchor, padx=padx, pady=2)

        # 말풍선 라벨
        bubble = tk.Label(
            bubble_frame,
            text=msg["text"],
            bg="#DCF8C6" if is_me else "#FFFFFF",
            fg="black",
            font=("맑은 고딕", 10),
            bd=1,
            relief="solid",
            wraplength=250,
            justify="left",
            padx=10,
            pady=5
        )
        bubble.pack(anchor=anchor)

        # 시간 표시 (작게)
        time_label = tk.Label(
            bubble_frame,
            text=msg["time"],
            font=("맑은 고딕", 8),
            fg="gray",
            bg="white"
        )
        time_label.pack(anchor=anchor, pady=(0, 5))

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


"""
완, 뒤로가기 버튼, 메시지 저장
카테고리 연결, 채팅방 자동 시간 연결, 사용자 이미지 연결, 채팅페이지 좌우배열

DB 연결 후>
채팅방 나가기, 채팅방 자동생성, 사진보내기, 이모지
약속잡기, 스크롤바
"""


class Chat_list:
    def __init__(self, parent, user, chat_content):
        self.parent = parent
        self.user = user
        self.chat_content = chat_content

        # 버튼 카테고리
        self.btn_frame = tk.Frame(self.parent, bg="white")
        self.btn_frame.pack(fill="x", pady=(0,5))
        tk.Button(self.btn_frame, text="전체", font=("맑은고딕", 12)).pack(side="left")
        tk.Button(self.btn_frame, text="판매", font=("맑은고딕", 12)).pack(side="left")
        tk.Button(self.btn_frame, text="구매", font=("맑은고딕", 12)).pack(side="left")
        tk.Button(self.btn_frame, text="안 읽은 채팅방", font=("맑은고딕", 12)).pack(side="left")

        # 채팅 목록 프레임
        self.chat_frame = tk.Frame(self.parent, bg="white")
        self.chat_frame.pack(expand=True, fill="both")

        # 이미지 불러오기
        self.profile_img = tk.PhotoImage(file="./img/chat_user.png")

        # 채팅방 예시
        self.chat_rooms = [
            {"room_id": "room1",
             "title": "고양이 캣타워",
             "nickname": "B님",
             "area": "서울시 강남구",
             "last_msg": "안녕하세요! 거래 가능할까요?",
             "last_time": datetime.datetime.now() - datetime.timedelta(days=1)},
            {"room_id": "room2",
             "title": "강아지 집",
             "nickname": "철수",
             "area": "대전 서구",
             "last_msg": "내일 볼 수 있을까요?",
             "last_time": datetime.datetime.now() - datetime.timedelta(days=1)},
            {"room_id": "room3",
             "title": "바디필로우",
             "nickname": "유리",
             "area": "부산 해운대구",
             "last_msg": "감사합니다!",
             "last_time": datetime.datetime.now() - datetime.timedelta(days=3)}]

        for room in self.chat_rooms:
            self.Chat_list_view(room)

    def Chat_list_view(self, room):
        box = tk.Frame(self.chat_frame, bg="white")
        box.pack(fill="x", padx=10, pady=5)

        # 왼쪽: 프로필 이미지
        img_label = tk.Label(box, image=self.profile_img, bg="white")
        img_label.image = self.profile_img  # 이미지 유지용 참조
        img_label.pack(side="left", padx=10, pady=10)

        # 오른쪽 전체 컨테이너
        right_frame = tk.Frame(box, bg="white")
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 위쪽 텍스트: 닉네임
        nickname = tk.Label(right_frame, text=room["nickname"],
                            font=("맑은고딕", 12, "bold"), bg="white", anchor="w")
        nickname.pack(anchor="w")

        # 중간: 동네 + 시간
        area_time = tk.Label(right_frame, text=self.get_days_ago_text((room["last_time"])),
                             font=("맑은고딕", 10), fg="gray",bg="white", anchor="w")
        area_time.pack(anchor="w")

        # 아래: 마지막 메시지 (오른쪽 아래 정렬)
        msg_frame = tk.Frame(right_frame, bg="white")
        msg_frame.pack(fill="both", expand=True)

        last_msg = tk.Label(msg_frame, text=room["last_msg"], font=("맑은고딕", 10), fg="black", bg="white", anchor="e")
        last_msg.pack(side="right", anchor="se")

        # 클릭 이벤트
        self.bind_all_widgets(box, lambda e, r=room: self.chat_content(r))

    def bind_all_widgets(self, widget, callback):
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            self.bind_all_widgets(child, callback)



    def get_days_ago_text(self, last_time):
        days = (datetime.datetime.now() - last_time).days
        if days == 0:
            return "오늘"
        elif days == 1:
            return "어제"
        else:
            return f"{days}일 전"













# todo 7월에 만든거

# # ✅ 채팅
# import socket
# import pymysql
# import time # 채팅시간 저장
# from datetime import datetime
# import threading

# # 상수 처리
# HOST = '192.168.0.55'
# PORT = 8080
#
# # 소켓 설정
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))
#
# # 커서 생성
# # conn = pymysql.connect(user='root', password='0000', db='carot', charset='utf8')
# # cur = conn.cursor()
#
#
# # ✅ 채팅방 클래스
# class Chat:
#     def __init__(self, id, buyer, seller, product, date, read_check, content):
#         self.id = id # 🍪 00001 ... int
#         self.buyer = buyer # 카테고리(구매) 구분을 위함 # 🍪 "포립 님" ... str
#         self.seller = seller # 카테고리(판매) 구분을 위함 # 🍪 "수리 님" ... str
#         self.product = product # 상품 # 🍪 '한화 이글스 유니폼' ... str
#         self.date = date # 🍪 '년 / 월 / 일' ... str
#         self.read_check = read_check # 카테고리(안 읽은 채팅방) 구분을 위함 # 🍪 False(안읽음) ... bool
#         self.content = content  # 🍪 메시지 보관
#
#     # ☑️ 시간 확인 함수(메시지 관련) ex)오전, 00시 00분
#     def time_check(self):
#         t = time.localtime()
#         tc = ""
#         if t.tm_hour < 12:
#             tc = "오전"
#         else:
#             tc = "오후"
#         check_time = time.strftime("%I시 %M분", t)  # I시(01 ~ 12)
#         tc += "," + check_time
#         return tc
#
#     # ☑️ 보낸 메시지
#     def sendmessage(self):
#         while True:
#             # "사용자 채팅 입력"
#             send_ms = input("보낼 메세지 입력 : ")
#
#             # "채팅방 나가기" 연결
#             if send_ms == 'exit':
#                 print("채팅 종료")
#                 sock.shutdown(socket.SHUT_RDWR) # RD(소켓통신차단), WR(소켓송신차단), RDWR(송수신차단)
#                 sock.close()
#                 break
#
#             # "보내기" 연결
#             send_total = send_ms
#             nowtime = self.time_check() # 시간저장
#             send_total += "," + nowtime
#             sock.send(send_total.encode("utf-8"))
#
#             # # SQL 수정
#             # try:
#             #     chat_content = "INSERT INTO CHAT (content, date) VALUES (%s, %s)"
#             #     cur.execute(chat_content, (send_ms,nowtime))
#             #     conn.commit() # DB 반영
#             # except Exception as e:
#             #     print("오류! 오류 원인 : ",e)
#
#             # 메시지 리스트 저장
#             self.content.append(["sender",send_ms, nowtime]) # 2중 리스트
#
#     # ☑️ 받은 메시지
#     def receiveMessage(self):
#         while True:
#             try:
#                 recv_ms = sock.recv(8192).decode("utf-8")
#                 nowtime = self.time_check()  # 시간저장
#                 # 메시지 리스트 저장
#                 self.content.append(["receiver", recv_ms, nowtime])  # 2중 리스트
#             except Exception: # 보내는 메시지가 exit 하면 종료
#                 print("채팅 종료")
#                 break
#
#     # ☑️ 스레드 연결 / 채팅 시작
#     def start_chat(self):
#         sender = threading.Thread(target=self.sendmessage)
#         receiver = threading.Thread(target=self.receiveMessage)
#         sender.start()
#         receiver.start()
#
#     # ☑️ 약속잡기 ()
#     def promise(self):
#         time = self.time_check()
#         week = datetime.today().weekday() # 오늘의 요일
#         loc = input("주소를 입력하세요 : ")
#         total = [time,week,loc]
#         return total
#
#
# import tkinter as tk
# from header import Header
#
# class CarrotMaker:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("CarrotCarrot")
#         self.root.geometry("400x600")
#
#         # 헤더 불러오기
#         self.header = Header(self.root)
#
#         # # 메인 영역
#         # self.body_frame = tk.Frame(self.root, bg="white")
#         # self.body_frame.pack(expand=True, fill="both")
#
#         # 예시 내용
#         # self.label = tk.Label(self.body_frame, text="메인 페이지입니다.", font=("Arial", 12))
#         # self.label.pack(pady=20)
#
#         # chat 프레임
#         self.chat_frame = tk.Frame(self.root, bg="black", height=490)
#         self.chat_frame.pack(expand=True, fill="x", anchor="n")
#
#         # 프레임 헤더1
#
#         # category 프레임
#         self.category_frame = tk.Frame(self.chat_frame, bg="red", height=40)
#         self.category_frame.pack(expand=True, fill="x", anchor="n")
#
#         # chat_content (채팅 1개씩 추가추가)
#         self.chat_content = tk.Frame(self.chat_frame, bg="blue", height=60)
#         self.chat_content.pack(expand=True, fill="x", anchor="n")
#
#         # self.btn_chat_total = tk.Button(self., text="전체", font=("Arial",12))
#         # self.btn_chat_total.pack(expand=True)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CarrotMaker(root)
#     root.mainloop()
#
#
#
# """
# chat_num
# sell_id
# user_id
#
# 채팅방 ID 에
# sll_ID 와 각 유저의 ID 필요
# """

if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker(root)
    root.mainloop()