import tkinter as tk
from header import Header

class CarrotMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")

        # 헤더 불러오기
        self.header = Header(self.root)

        # 메인 영역
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        # 예시 내용
        self.label = tk.Label(self.body_frame, text="메인 페이지입니다.", font=("Arial", 12))
        self.label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker(root)
    root.mainloop()
