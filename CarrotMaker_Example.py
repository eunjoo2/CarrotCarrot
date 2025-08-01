import tkinter as tk
from header import Header
from login1 import Login1
from login2 import Login2
from opening import Opening
import threading
import socket


class CarrotMaker_Example:
    def __init__(self, root):

        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")
        self.stage = 0

        # 헤더 불러오기
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.logo_view = Opening(self.body_frame)

        self.root.after(500, lambda: self.set_stage(9))

    def set_stage(self, stage):
        print(f"기존 스테이지: {self.stage} → 변경될 스테이지: {stage}")
        self.stage = stage

        if self.stage != 0:
            # 인트로 화면 제거
            self.logo_view.destroy()

            # Header 생성 (인트로 화면에는 없었음)
            self.header = Header(self.root)


        if self.stage == 1:
            # 본문 영역 갱신
            self.show_register_page()

        if self.stage == 9:
            self.show_login_page()

    def show_register_page(self):
        # 이전 body_frame 제거 -> 기존화면에 그려지고있던 틀인 body_frame을 일단 제거시킴
        self.body_frame.destroy()

        # 새로운 body_frame 생성 -> 새롭게 그릴 화면의 틀을 다시 만들어냄.
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.register_view = Login1(self.body_frame, controller=self)

    def show_login_page(self):
        # 이전 body_frame 제거 -> 기존화면에 그려지고있던 틀인 body_frame을 일단 제거시킴
        self.body_frame.destroy()

        # 휴대전화번호 인증 페이지에서는 헤더가 없음. 숨겨둘거임.
        self.header.destroy()

        # 새로운 body_frame 생성 -> 새롭게 그릴 화면의 틀을 다시 만들어냄.
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.login_view = Login2(self.body_frame)



if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker_Example(root)

    root.mainloop()
