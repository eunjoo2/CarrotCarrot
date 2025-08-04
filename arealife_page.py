import tkinter as tk
import tkinter as tk
from tkinter import messagebox

class AreaLifePage:
    def __init__(self, parent, board, user):
        self.parent = parent  # 부모 Frame 혹은 root
        self.board = board
        self.user = user

        # body_frame 새로 만들기 (혹은 외부에서 주입 가능)
        self.body_frame = tk.Frame(self.parent, bg="white")
        self.body_frame.pack(expand=True, fill="both")

        self.create_widgets()

class AreaLifePage:
    def __init__(self, parent, board, user):
        self.board = board
        self.user = user
        self.form_visible = False

        self.body_frame = tk.Frame(parent, bg="#FAFAF6")
        self.body_frame.pack(expand=True, fill="both")

        # 글쓰기 입력 폼 (초기에는 숨김)
        self.form_frame = tk.Frame(self.body_frame, bg="#FAFAF6")
        tk.Label(self.form_frame, text="제목", font=("맑은 고딕", 10), bg="#FAFAF6").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.form_frame, width=32, font=("맑은 고딕", 11))
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(7,0))
        tk.Label(self.form_frame, text="내용", font=("맑은 고딕", 10), bg="#FAFAF6").grid(row=1, column=0, sticky="nw")
        self.content_entry = tk.Text(self.form_frame, width=32, height=3, font=("맑은 고딕",10))
        self.content_entry.grid(row=1, column=1, padx=(7,0), pady=3)
        self.submit_btn = tk.Button(
            self.form_frame, text="등록", bg="#FF6F0F", fg="white", font=("맑은 고딕", 10, "bold"),
            width=8, command=self.submit_post, bd=0)
        self.submit_btn.grid(row=2, column=1, sticky="e", pady=(4,0))
        self.form_frame.columnconfigure(1, weight=1)

        # 글 목록 스크롤 영역
        list_frame = tk.Frame(self.body_frame, bg="#FAFAF6")
        list_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(list_frame, bg="#FAFAF6", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(list_frame, command=self.canvas.yview)
        scroll.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FAFAF6")
        self.canvas_window = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def resize_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind('<Configure>', resize_canvas)

        def frame_configure(event):
            self.canvas.configure(scrollregion=(self.canvas.bbox("all")))
        self.scrollable_frame.bind("<Configure>", frame_configure)

        # 글쓰기 버튼
        self.write_btn = tk.Button(
            self.body_frame, text="+ 글쓰기", bg="#FF6F0F", fg="white",
            font=("맑은 고딕", 11, "bold"), command=self.toggle_form,
            bd=0, padx=12, pady=5
        )
        self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        # 게시글 불러오기
        self.load_posts()

    def toggle_form(self):
        if self.form_visible:
            self.form_frame.pack_forget()
            self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")  # 글쓰기 버튼 다시 표시
        else:
            self.form_frame.pack(fill="x", padx=16, pady=(10,8))
            self.write_btn.place_forget()  # 글쓰기 버튼 숨기기
        self.form_visible = not self.form_visible

    def load_posts(self):
        for post in reversed(self.board.posts):
            self.add_post_card(post)

    def submit_post(self):
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not title or not content:
            messagebox.showwarning("입력 오류", "제목과 내용을 입력해 주세요.")
            return
        post = self.board.create_post(self.user, title, content, "일반")
        if post:
            self.add_post_card(post)
            self.title_entry.delete(0, "end")
            self.content_entry.delete("1.0", "end")
            self.toggle_form()  # 폼 닫고 버튼 다시 보이게
        else:
            messagebox.showerror("글쓰기 실패", "로그인 후 이용 가능합니다.")

    def add_post_card(self, post):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="ridge", padx=12, pady=7)
        card.pack(fill="x", pady=0, padx=7)

        tk.Label(card, text=post.title, font=("맑은 고딕", 12, "bold"), bg="white", anchor="w").pack(fill="x")
        tk.Label(card, text=f"{post.user.nick_name} · {post.timestamp.strftime('%m월%d일 %H:%M')}",
                 font=("맑은 고딕",8), fg="#888", bg="white", anchor="w").pack(fill="x")
        tk.Label(card, text=post.content, bg="white", font=("맑은 고딕", 10),
                 wraplength=320, justify="left", anchor="w").pack(fill="x", pady=(6,0))

        footer = tk.Frame(card, bg="white")
        tk.Label(footer, text=f"👁 {post.views}", font=("맑은 고딕", 9), bg="white", fg="#666").pack(side="left", padx=(0,15))
        tk.Label(footer, text=f"❤️ {len(post.likes)}", font=("맑은 고딕", 9), bg="white", fg="#FF6F0F").pack(side="left", padx=(0,8))
        tk.Label(footer, text=f"💬 {len(post.comments)}", font=("맑은 고딕", 9), bg="white", fg="#22A6EF").pack(side="left")
        footer.pack(fill="x", pady=(7,0))

    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.body_frame.destroy()


    def create_widgets(self):
        # 글쓰기 폼
        form_frame = tk.Frame(self.body_frame, bd=2, relief="ridge", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="제목").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(form_frame, width=35)
        self.title_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="내용").grid(row=1, column=0, sticky="nw")
        self.content_text = tk.Text(form_frame, height=4, width=30)
        self.content_text.grid(row=1, column=1)

        tk.Button(form_frame, text="글쓰기", command=self.submit_post).grid(row=2, column=1, sticky="e", pady=5)

        # 게시글 목록 스크롤 영역
        list_frame = tk.Frame(self.body_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(list_frame)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def submit_post(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", "end").strip()
        if not title or not content:
            print("[알림] 제목과 내용을 입력하세요.")
            return

        post = self.board.create_post(self.user, title, content, "일반")
        if post:
            self.add_post_card(post)
            self.title_entry.delete(0, "end")


class AreaLifePage:
    def __init__(self, parent, board, user):
        self.board = board
        self.user = user
        self.form_visible = False

        self.body_frame = tk.Frame(parent, bg="#FAFAF6")
        self.body_frame.pack(expand=True, fill="both")

        # 글쓰기 입력 폼 (초기에는 숨김)
        self.form_frame = tk.Frame(self.body_frame, bg="#FAFAF6")
        tk.Label(self.form_frame, text="제목", font=("맑은 고딕", 10), bg="#FAFAF6").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.form_frame, width=32, font=("맑은 고딕", 11))
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=(7,0))
        tk.Label(self.form_frame, text="내용", font=("맑은 고딕", 10), bg="#FAFAF6").grid(row=1, column=0, sticky="nw")
        self.content_entry = tk.Text(self.form_frame, width=32, height=3, font=("맑은 고딕",10))
        self.content_entry.grid(row=1, column=1, padx=(7,0), pady=3)
        self.submit_btn = tk.Button(
            self.form_frame, text="등록", bg="#FF6F0F", fg="white", font=("맑은 고딕", 10, "bold"),
            width=8, command=self.submit_post, bd=0)
        self.submit_btn.grid(row=2, column=1, sticky="e", pady=(4,0))
        self.form_frame.columnconfigure(1, weight=1)

        # 글 목록 스크롤 영역
        list_frame = tk.Frame(self.body_frame, bg="#FAFAF6")
        list_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(list_frame, bg="#FAFAF6", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(list_frame, command=self.canvas.yview)
        scroll.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FAFAF6")
        self.canvas_window = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def resize_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind('<Configure>', resize_canvas)

        def frame_configure(event):
            self.canvas.configure(scrollregion=(self.canvas.bbox("all")))
        self.scrollable_frame.bind("<Configure>", frame_configure)

        # 글쓰기 버튼
        self.write_btn = tk.Button(
            self.body_frame, text="+ 글쓰기", bg="#FF6F0F", fg="white",
            font=("맑은 고딕", 11, "bold"), command=self.toggle_form,
            bd=0, padx=12, pady=5
        )
        self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        # 게시글 불러오기
        self.load_posts()

    def toggle_form(self):
        if self.form_visible:
            self.form_frame.pack_forget()
            self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")  # 글쓰기 버튼 다시 표시
        else:
            self.form_frame.pack(fill="x", padx=16, pady=(10,8))
            self.write_btn.place_forget()  # 글쓰기 버튼 숨기기
        self.form_visible = not self.form_visible

    def load_posts(self):
        for post in reversed(self.board.posts):
            self.add_post_card(post)

    def submit_post(self):
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not title or not content:
            messagebox.showwarning("입력 오류", "제목과 내용을 입력해 주세요.")
            return
        post = self.board.create_post(self.user, title, content, "일반")
        if post:
            self.add_post_card(post)
            self.title_entry.delete(0, "end")
            self.content_entry.delete("1.0", "end")
            self.toggle_form()  # 폼 닫고 버튼 다시 보이게
        else:
            messagebox.showerror("글쓰기 실패", "로그인 후 이용 가능합니다.")

    def add_post_card(self, post):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="ridge", padx=12, pady=7)
        card.pack(fill="x", pady=0, padx=7)

        tk.Label(card, text=post.title, font=("맑은 고딕", 12, "bold"), bg="white", anchor="w").pack(fill="x")
        tk.Label(card, text=f"{post.user.nick_name} · {post.timestamp.strftime('%m월%d일 %H:%M')}",
                 font=("맑은 고딕",8), fg="#888", bg="white", anchor="w").pack(fill="x")
        tk.Label(card, text=post.content, bg="white", font=("맑은 고딕", 10),
                 wraplength=320, justify="left", anchor="w").pack(fill="x", pady=(6,0))

        footer = tk.Frame(card, bg="white")
        tk.Label(footer, text=f"👁 {post.views}", font=("맑은 고딕", 9), bg="white", fg="#666").pack(side="left", padx=(0,15))
        tk.Label(footer, text=f"❤️ {len(post.likes)}", font=("맑은 고딕", 9), bg="white", fg="#FF6F0F").pack(side="left", padx=(0,8))
        tk.Label(footer, text=f"💬 {len(post.comments)}", font=("맑은 고딕", 9), bg="white", fg="#22A6EF").pack(side="left")
        footer.pack(fill="x", pady=(7,0))

    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.body_frame.destroy()

        self.content_text.delete("1.0", "end")

    def add_post_card(self, post):
        card = tk.Frame(self.scrollable_frame, bd=1, relief="solid", padx=10, pady=5)
        tk.Label(card, text=post.title, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(card, text=f"{post.user.name} · {post.timestamp.strftime('%m월%d일 %H:%M')}").pack(anchor="w")
        tk.Label(card, text=post.content, wraplength=350, justify="left").pack(anchor="w")

        footer = tk.Frame(card)
        tk.Label(footer, text=f"👁 조회수: {post.views}").pack(side="left")
        tk.Label(footer, text=f"❤️ 좋아요: {len(post.likes)}").pack(side="right")
        footer.pack(fill="x", pady=5)

        card.pack(fill="x", pady=5)

    def destroy(self):
        self.body_frame.destroy()
