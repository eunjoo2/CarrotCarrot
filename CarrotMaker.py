from header import Header
from bottom import bottom
from opening import Opening
from arealife_page import AreaLifePage
from arealife import AreaLifeBoard
from User import User
from HomeArray import HomeArray
from detailPage import DetailPage
from AreaMap import AreaMap
from MyCarrotPage import MyCarrotPage


import tkinter as tk

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
        # self.body_frame = tk.Frame(self.root)
        self.body_frame = tk.Frame(self.root, bg="white") # get_page_color 함수 지우면 이거 활성화
        self.body_frame.pack(expand=True, fill="both")

        # 헤더 타이틀 변경
        self.header.update_title(name)

        # "동네지도" 외에는 헤더 다시 표시
        if name != "동네지도":
            self.header.pack(fill="x")
            self.header.update_title(name)
        else:
            self.header.pack_forget()  # 헤더 숨기기

        # 페이지 조건별 분기
        if name == "홈":
            self.body_frame.destroy()
            self.body_frame = HomeArray(self.root)


        elif name == "동네생활":
            self.body_frame.destroy()
            AreaLifePage(self.body_frame, self.board, self.user)  # 따로 pack 필요 없음 (내부에서 구현됨)

        elif name == "동네지도":
            self.header.pack_forget()  # ← 헤더 숨기기
            self.body_frame.destroy()
            self.body_frame = AreaMap(self.root)
            self.body_frame.pack(expand=True, fill="both")

            #tk.Label(self.body_frame, text="동네지도 페이지", font=("Arial", 12), bg=self.get_page_color(name)).pack(pady=20)

        elif name == "채팅":
            tk.Label(self.body_frame, text="채팅 페이지", font=("Arial", 12),bg="#E0F0FF").pack(pady=20)
            self.body_frame.destroy()

        elif name == "나의당근":
            self.body_frame.destroy()
            user_info = {
                "name": "돌맹구",
                "temp": "36.7"
            }
            # self.body_frame = MyCarrotPage(self.root, user_info=user_info)
            self.body_frame = MyCarrotPage(self.root, show_page_callback=self.show_page, user_info=user_info)

            self.body_frame.pack(fill="both", expand=True)
            self.header.update_title("나의 당근")

        else:
            tk.Label(self.body_frame, text="[오류] 페이지를 찾을 수 없습니다.", font=("Arial", 12), bg="#FFCCCC").pack(pady=20)

    def show_detail_page(self, item_id):
        self.header.update_title("상세")
        #self.home.pack_forget()  # 홈 화면 숨기기
        self.detail = DetailPage(self.root, item_id)  # item_id 전달
        self.detail.pack()

    # def get_page_color(self, name):
    #     colors = {
    #         "홈": "#FFFFFF",
    #         "동네생활": "#FFFACD",
    #         "동네지도": "#E0FFE0",
    #         "채팅": "#E0F0FF",
    #         "나의당근": "#8041D9"
    #     }
    #     return colors.get(name, "#FFFFFF")




if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker(root)
    root.mainloop()
