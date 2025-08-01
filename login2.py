import tkinter as tk

class Login2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self.pack(fill=tk.X)
        self.create_widgets()

    def create_widgets(self):
        # ─────────────── 1. 로고 ───────────────
        frame_logo = tk.Frame(self, bg="white")
        frame_logo.pack(fill=tk.X)
        image = tk.PhotoImage(file="./img/left_arrow.png").subsample(20, 20)
        logo = tk.Label(frame_logo, image=image, bg="white")
        logo.place(x=0, y=0, anchor="nw")
        logo.image = image  # 이미지 참조 유지
        logo.pack(side=tk.LEFT)

        # ─────────────── 2. 메인 문구 ───────────────
        frame_title = tk.Frame(self, bg="white")
        frame_title.pack()
        title = tk.Label(frame_title, text="휴대폰 번호를 입력해주세요", font=("Arial", 16, "bold"), fg="black", bg="white")
        title.pack()

        #  ─────────────── 3. 휴대폰 입력 창 ───────────────
        frame_entry = tk.Frame(self, bg="white")
        frame_entry.pack(side=tk.LEFT)
        entry = tk.Entry(frame_entry, bg="white", fg="black", width=20)
        entry.pack(side=tk.LEFT)

        # ─────────────── 4. 시작하기 버튼 ───────────────
        frame_button = tk.Frame(self, bg="white")
        frame_button.pack(pady=20)
        start_btn = tk.Button(frame_button, text="확인", bg="#FF6F0F", fg="white", font=("Arial", 12, "bold"), width=30,
                              height=2, bd=0, relief="flat")
        start_btn.pack()