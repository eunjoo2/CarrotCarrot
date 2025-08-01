import tkinter as tk

class Login1(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master, width=300, height=300, bg="white")
        self.controller = controller  # CarrotMaker를 참조로 저장
        # self.place(relx=0.5, rely=0.5, anchor="center")
        self.pack(expand=True, fill="both")

        self.create_widgets()


    def create_widgets(self):
        # ─────────────── 1. 로고 ───────────────
        frame_logo = tk.Frame(self, bg="white")
        frame_logo.pack(pady=30)
        image = tk.PhotoImage(file="./img/Daangn_icon_RGB.png").subsample(8, 8)
        logo = tk.Label(frame_logo, image=image, bg="white")
        logo.image = image  # 이미지 참조 유지
        logo.pack()

        # ─────────────── 2. 메인 문구 ───────────────
        frame_title = tk.Frame(self, bg="white")
        frame_title.pack()
        title = tk.Label(frame_title, text="당신 근처의 당근", font=("Arial", 16, "bold"), fg="black", bg="white")
        title.pack()

        # ─────────────── 3. 설명 + 위치 ───────────────
        frame_desc = tk.Frame(self, bg="white")
        frame_desc.pack(pady=10)
        subtitle = tk.Label(frame_desc, text="동네라서 가능한 모든 것\n지금 내 동네를 선택하고 시작해보세요!", font=("Arial", 10), fg="black", bg="white", justify="center")
        subtitle.pack()


        # ─────────────── 4. 시작하기 버튼 ───────────────
        frame_button = tk.Frame(self, bg="white")
        frame_button.pack(pady=20)
        start_btn = tk.Button(frame_button, text="시작하기", bg="#FF6F0F", fg="white", font=("Arial", 12, "bold"), width=30, height=2, bd=0, relief="flat")
        start_btn.pack()




