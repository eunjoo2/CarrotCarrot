from tkinter.constants import BOTTOM

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
#🍪🍪🍪
from tkcalendar import Calendar
    # pip install tkcalendar
    # 약속잡기 캘린더

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

    # ------------------------------------------------------------todo 채팅 관련 all
    # ☑️ 채팅방 진입 시 액자 변경
    def chat_content(self, room_info):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title(room_info["nickname"])
        self.header.back_button(self.back_chat)

        # 채팅 페이지 진입
        Chat_page(self.body_frame, self.user, room_info)

    # ☑️ 뒤로가기 버튼 생성
    def back_chat(self):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.header.update_title("채팅 목록")
        self.header.back_button(None)

        Chat_list(self.body_frame, self.user, self.chat_content)

CHATTING = {} # 채팅메시지

# class Chat:
#     def __init__(self, id, buyer, seller, product, date, content):
#         self.id = id # 🍪 00001 ... int
#         self.buyer = buyer # 카테고리(구매) 구분을 위함 # 🍪 "포립 님" ... str
#         self.seller = seller # 카테고리(판매) 구분을 위함 # 🍪 "수리 님" ... str
#         self.product = product # 상품 # 🍪 '한화 이글스 유니폼' ... str
#         self.date = date # 🍪 '년 / 월 / 일' ... str
#         self.content = content  # 🍪 메시지 보관
#
#         self.read_check = False  # 카테고리(안 읽은 채팅방) 구분을 위함 # 🍪 False(안읽음) ... bool




class Chat_page:
    def __init__(self, parent, user, room_id):
        self.parent = parent
        self.user = user
        self.room_id = room_id
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(expand=True, fill="both")

        self.room_key = str(room_id["room_id"])
        if self.room_key not in CHATTING:
            CHATTING[self.room_key] = []
        self.msgs = CHATTING[self.room_key]

        # 채팅방 진입 시 "게시물이름 채팅방"
        tk.Label(self.frame, text=f"[{room_id['title']}] 채팅방", font=("맑은 고딕", 13)).pack(pady=5)
        tk.Button(self.frame, text="약속 잡기", command = lambda : self.promise(room_id)).pack()

        self.top_frame = tk.Frame(self.frame, bg="white")
        self.top_frame.pack(fill="both", expand=True)
        self.bottom_frame = tk.Frame(self.frame, bg="white")
        self.bottom_frame.pack(fill="x")

        self.canvas = tk.Canvas(self.top_frame, bg="white", highlightthickness=0)
            # highlightthickness = 외곽선 두께

        # ☑️ 마우스 휠 함수
        def mouse_wheel(event):
            self.canvas.yview_scroll((-1 * event.delta), "units")
            # -1 없으면 스크롤이 반대로 작동
            # 현재
        self.canvas.bind_all("<MouseWheel>", mouse_wheel) # 마우스 휠 바인딩
            # bind_all() = 전체 앱에서 마우스 휠 감지할 수 있도록

        # ☑️ 스크롤바, 메시지 프레임
        self.scrollbar = ttk.Scrollbar(self.top_frame, orient="vertical", command=self.canvas.yview)
            # yview() = 세로 스크롤 연결

        self.msg_frame = tk.Frame(self.canvas, bg="white")
        self.msg_frame.bind("<Configure>",
                            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            # 캔버스는 자동으로 스크롤 범위를 계산하지 않음
            # 메시지가 늘어나면 scrollregion(스크롤가능 영역)도 수동으로 해야함
            # bind("이벤트", 함수) ... "<Configure>"은 이벤트 크기or위치 변경 시 발생
            # self.canvas.bbox("all") 의 return = (x1, y1, x2, y2)

        # ☑️ 캔버스_메시지프레임 크기 맞추기 // 보낸사람, 받은사람 좌우 배열을 위함
        def canvas_sizing(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.msg_window, width=canvas_width)

        self.canvas.bind("<Configure>", canvas_sizing)
        self.msg_window = self.canvas.create_window((0, 0), window=self.msg_frame, anchor="nw")
            # creat_window(x, y)
            # 캔버스 안에 메시지 프레임 삽입 (캔버스 스크롤 가능 영역(좌표)을 새로 설정)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
            # yscrollcommand = 스크롤될 때마다 스크롤 위치 알려줌
            # scrollbar.set = 스크롤바의 손잡이 위치와 크기를 설정 매서드

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 하단 입력창
        entry_frame = tk.Frame(self.bottom_frame, bg="white")
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
                "sender": self.user.nick_name,
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


    # 약속잡기☀️☀️☀️☀️☀️
    def promise(self, room_info):
        promise_window = tk.Toplevel(self.frame)
        promise_window.title("약속잡기")
        promise_window.geometry("300x500")

        body_frame = tk.Frame(promise_window, bg="white")
        body_frame.pack(expand=True, fill="both")

        top_frame = tk.Frame(body_frame, bg="white")
        top_frame.pack(fill="x")

        # 날짜, 시간, 장소 // 약속 전 나에게 알림(x)
        nick_name = str(room_info["nickname"])
        label = tk.Label(top_frame, text=f"{nick_name}님과 약속", font=("맑은 고딕", 13, "bold"))
        label.pack(anchor="nw",padx=10, pady=10)

        date_frame = tk.Frame(body_frame, bg="white", height=60)
        time_frame = tk.Frame(body_frame, bg="white", height=60)
        location_frame = tk.Frame(body_frame, bg="white", height=60)
        calendar_frame = tk.Frame(body_frame, bg="white", height=170)
        date_frame.pack(fill="x", pady=10)
        time_frame.pack(fill="x", pady=10)
        location_frame.pack(fill="x", pady=10)
        calendar_frame.pack(fill="x",padx=10, pady=10, expand=True)



        date1 = tk.Label(date_frame, bg="white", text="날짜", font=("맑은 고딕", 11, "bold"))
        time1 = tk.Label(time_frame, bg="white", text="시간", font=("맑은 고딕", 11, "bold"))
        location1 = tk.Label(location_frame, bg="white", text="장소", font=("맑은 고딕", 11, "bold"))
        date1.pack(side="left", padx=10, pady=10)
        time1.pack(side="left", padx=10, pady=10)
        location1.pack(side="left", padx=10, pady=10)


        promise_btn = tk.Button(body_frame, bg="#FF6F0F",text="완료",font=("맑은 고딕", 12, "bold"),
                                fg="#FFFFFF", highlightthickness=0, borderwidth=0,height=2)
        promise_btn.pack(side="bottom",fill="x", pady=5)

        # 캘린더 그림 확인 변수
        calendar_view = None

        # ☑️ 캘린더 버튼
        def calendar():
            nonlocal calendar_view
            if calendar_view is None:
                calendar_view = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
                calendar_view.pack()
            else:
                calendar_view.destroy()
                calendar_view = None

        def date_time():
            now = datetime.datetime.now().strftime("%m월 %d일 %a")
            if now[0] == 0:
                now = now[1:]

            if now[-3:] == "Mon":
                week = "월요일"
            elif now[-3:] == "Tue":
                week = "화요일"
            elif now[-3:] == "Wed":
                week = "수요일"
            elif now[-3:] == "Thu":
                week = "목요일"
            elif now[-3:] == "Fri":
                week = "금요일"
            elif now[-3:] == "Sat":
                week = "토요일"
            elif now[-3:] == "Sun":
                week = "일요일"
            return now[:-3] + week

        date2 = tk.Button(date_frame, bg="white", text=f"{date_time()}", font=("맑은 고딕", 11, "bold")
                          , highlightthickness=0, activebackground="white", borderwidth=0, command=calendar)
        date2.pack(side="right", padx=10, pady=10)



    def display_single_message(self, msg):
        is_me = (msg["sender"] == self.user.nick_name)
        bubble_frame = tk.Frame(self.msg_frame, bg="white", pady=2)

        # 말풍선 라벨
        bubble = tk.Label(
            bubble_frame,
            text=msg["text"],
            bg="#FF6F0F" if is_me else "#D9D9D9",
            fg="black",
            font=("맑은 고딕", 10),
            bd=1,
            relief="solid",
            wraplength=250,
            justify="left",
            padx=10,
            pady=5
        )

        # 시간 표시 (작게)
        time_label = tk.Label(
            bubble_frame,
            text=msg["time"],
            font=("맑은 고딕", 8),
            fg="gray",
            bg="white"
        )

        # 좌우 배열 조건문
        if is_me:
            bubble_frame.pack(anchor="e", padx=10, pady=2)
            bubble.pack(anchor="e")
            time_label.pack(anchor="e", pady=(0, 5))
        else:
            bubble_frame.pack(anchor="w", padx=10, pady=2)
            bubble.pack(anchor="w")
            time_label.pack(anchor="w", pady=(0, 5))

        # ☑️ 최신채팅 스크롤 따라가기
        self.canvas.update_idletasks()
            # 지금 즉시 레이아웃 처리! 명령코드
            # 이유 : pack(), grid(), place() 같은 레이아웃 작업은 Tkinter가 비교적 느리게 처리함
        self.canvas.yview_moveto(1.0)

"""
완, 뒤로가기 버튼, 메시지 저장, 채팅내용 자동 시간 연결, 채팅페이지 좌우배열, 스크롤바
 
약속잡기, 사진 보내기(자동 사진 사이즈 조절), 이모지 

상단고정, 읽음/안읽음, 채팅방 나가기 //// 커멘드 함수 엮어야함
메시지 저장 / 삭제
채팅방이 없을 때 "채팅방이 없어요."

DB 연결 후>
채팅방 생성, 채팅방 옆 동네 붙이기
카테고리 연결,  사용자 이미지 연결,
"""


class Chat_list:
    def __init__(self, parent, user, chat_content):
        self.parent = parent
        self.user = user
        self.chat_content = chat_content

        # 버튼 카테고리
        self.btn_frame = tk.Frame(self.parent, bg="white")
        self.btn_frame.pack(fill="x", pady=(0,5))
        tk.Button(self.btn_frame, text="전체", font=("맑은고딕", 12)).pack(side="left") #command=lambda: chatroom_filter(user,count)
        tk.Button(self.btn_frame, text="판매", font=("맑은고딕", 12)).pack(side="left")
        tk.Button(self.btn_frame, text="구매", font=("맑은고딕", 12)).pack(side="left")
        tk.Button(self.btn_frame, text="안 읽은 채팅방", font=("맑은고딕", 12)).pack(side="left")

        # # ☑️ 카테고리 구분 함수(전체 / 판매 / 구매 / 안 읽은 채팅방)
        # def chatroom_filter(user_id, count): # 유저, 안 읽은 메시지 개수
        #     # 전체는 그냥 다가지고 오고
        #     # user_id 로 seller, buyer 로 구분해서 판매/구매 글 구분
        #     # 안읽음 생각해보고
        #     if user_id == seller:
        #         pass # 판매
        #     elif user_id == buyer:
        #         pass # 구매
        #     elif count != 0:
        #         pass



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
             "last_time": datetime.datetime.now() - datetime.timedelta(days=1),
             "read_count": 0,
             },
            {"room_id": "room2",
             "title": "강아지 집",
             "nickname": "철수",
             "area": "대전 서구",
             "last_msg": "내일 볼 수 있을까요?",
             "last_time": datetime.datetime.now() - datetime.timedelta(days=1),
             "read_count": 2
             },
            {"room_id": "room3",
             "title": "바디필로우",
             "nickname": "유리",
             "area": "부산 해운대구",
             "last_msg": "감사합니다!",
             "last_time": datetime.datetime.now() - datetime.timedelta(days=3),
             "read_count": 1
             }
        ]

        for room in self.chat_rooms:
            self.Chat_list_view(room)

    # ☑️ 채팅 리스트 GUI
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
        self.chatlist_click_left(box, lambda e, r=room: self.chat_content(r))
            # e에 이벤트 r에 룸을 담아서 r을 넘겨주고
            # e는 bind()를 사용할 때 전달됨.
        self.chatlist_click_right(box, lambda e, r=room: self.chatlist_clickmenu(e, r))

    # ☑️ 채팅방 진입(마우스 왼)
    def chatlist_click_left(self, widget, callback):
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            self.chatlist_click_left(child, callback)
        # box 프레임의 모든 자식들을 묶어서
        # 재귀는 for문 돌듯이 돎, 자식이 없다면 빈리스트 반환... 종료
        # 결국 모든 자식들을 묶어묶음 (바인딩)

    # ☑️ 채팅방 설정(마우스 오)
    def chatlist_click_right(self, widget, callback):
        widget.bind("<Button-3>", callback)
        for child in widget.winfo_children():
            self.chatlist_click_right(child, callback)

    # ☑️ 채팅방 설정메뉴 (읽음표시 / 상단고정 / 채팅방나가기)
    def chatlist_clickmenu(self, event, room): # + , room
        menu = tk.Menu(self.parent, tearoff=0)  # 부모는 frame이든 canvas든 상관없음
        menu.add_command(label="읽음으로 표시")  # command=lambda: self.mark_as_read(room)
        menu.add_command(label="상단 고정") # command=lambda: self.pin_room(room)
        menu.add_command(label="채팅방 나가기") # command=lambda: self.leave_chatroom(room)
        menu.tk_popup(event.x_root, event.y_root)
        menu.grab_release() # 다른곳 누르면 메뉴 꺼짐


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