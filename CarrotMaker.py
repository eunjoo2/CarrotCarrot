import tkinter as tk
from header import Header
from bottom import bottom
from opening import Opening

class CarrotMaker:

    def go_to_next_stage(self):
        self.logo_view.destroy()
        self.show_page("홈")  # 시작은 '홈'으로

    def show_page(self, name):
        # Body 제거 및 새로 생성
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        # 헤더 제목 바꾸기
        self.header.update_title(name)

        # Body 내부 페이지 출력
        content = {
            "홈": "홈 페이지.",
            "동네생활": "동네생활 페이지.",
            "동네지도": "동네지도 페이지.",
            "채팅": "채팅 페이지.",
            "나의당근": "나의 당근 페이지.",
        }
        msg = content.get(name, "페이지 없음")
        tk.Label(self.body_frame, text=msg, font=("Arial", 12), bg="white").pack(pady=20)

    def __init__(self, root):
        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")
        self.stage = 0

        # Header
        self.header = Header(self.root)

        # Body
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        # Opening
        if self.stage == 0:
            self.logo_view = Opening(self.body_frame)
            self.root.after(3000, self.go_to_next_stage)
        else:
            self.show_page("홈")

        # Bottom
        self.bottom = bottom(self.root, self.show_page)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker(root)
    root.mainloop()
