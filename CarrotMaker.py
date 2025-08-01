import tkinter as tk
from header import Header
from opening import Opening

class CarrotMaker:

    def go_to_next_stage(self):
        self.logo_view.destroy()
        self.show_second_page()

    def show_second_page(self):
        self.body_frame.destroy()
        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        label = tk.Label(self.body_frame, text="두번째 페이지 입니다.", font=("Arial", 12))
        label.pack(pady=20)


    def __init__(self, root):
        self.root = root
        self.root.title("CarrotCarrot")
        self.root.geometry("400x600")
        self.stage = 0


        # 헤더 불러오기
        self.header = Header(self.root)

        self.body_frame = tk.Frame(self.root, bg="white")
        self.body_frame.pack(expand=True, fill="both")


        if self.stage == 0:
            self.logo_view = Opening(self.body_frame)

            # 3초 후 화면 전환
            self.root.after(3000, self.go_to_next_stage)


        elif self.stage == 1:
            self.body_frame = tk.Frame(self.root, bg="white")
            self.body_frame.pack(expand=True, fill="both")

            self.label = tk.Label(self.body_frame, text="두번째 페이지 입니다.", font=("Arial", 12))
            self.label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarrotMaker(root)
    root.mainloop()