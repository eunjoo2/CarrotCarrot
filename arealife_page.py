import tkinter as tk
from tkinter import messagebox

class AreaLifePage:
    def __init__(self, parent, board, user):
        self.board = board # 게시판
        self.user = user # 로그인된 사용자
        self.form_visible = False

        # 전체 화면의 메인 프레임 생성
        self.body_frame = tk.Frame(parent, bg="#FAFAF6")
        self.body_frame.pack(expand=True, fill="both")

        # 글쓰기 입력 폼 프레임 (초기에는 숨김)
        self.form_frame = tk.Frame(self.body_frame, bg="#FAFAF6")

        # 제목 Entry
        # tk.Label(self.form_frame, text="제목", font=("맑은 고딕", 10), bg="#FAFAF6").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.form_frame, width=40, font=("맑은 고딕", 10))
        self.title_entry.grid(row=0, column=1, sticky="w", padx=(7,0))
        self.title_placeholder = "제목을 입력하세요."
        self.title_entry.insert(0, self.title_placeholder)
        self.title_entry.config(fg="gray")
        self.title_entry.bind("<FocusIn>", self.clear_title_placeholder)
        self.title_entry.bind("<FocusOut>", self.restore_title_placeholder)

        # 내용 Text
        # tk.Label(self.form_frame, text="내용", font=("맑은 고딕", 10), bg= "#FAFAF6").grid(row=1, column=0, sticky="nw")
        self.content_entry = tk.Text(self.form_frame, width=40, height=3, font=("맑은 고딕",10))
        self.content_entry.grid(row=1, column=1, sticky="w", padx=(7,0), pady=3)
        self.content_placeholder = "둔산동 이웃과 이야기를 나눠보세요."
        self.content_entry.insert("1.0", self.content_placeholder)
        self.content_entry.config(fg="gray")
        self.content_entry.bind("<FocusIn>", self.clear_content_placeholder)
        self.content_entry.bind("<FocusOut>", self.restore_content_placeholder)

        # 등록 버튼
        self.submit_btn = tk.Button(self.form_frame, text="등록", bg="#FF6F0F", fg="white", font=("맑은 고딕", 10, "bold"),width=8, command=self.submit_post, bd=0)
        self.submit_btn.grid(row=2, column=1, sticky="e", pady=(4,0))
        self.form_frame.columnconfigure(1, weight=1)

        # 글 목록 스크롤 영역
        list_frame = tk.Frame(self.body_frame, bg="#FAFAF6")
        list_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(list_frame, bg="#FAFAF6", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(list_frame, command=self.canvas.yview)
        scroll.pack(side="right", fill="y")

        # 글 카드들이 들어갈 내부 프레임
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FAFAF6")
        self.canvas_window = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)

        # # 마우스 휠 스크롤 기능
        # self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # 마우스 휠 스크롤 기능
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # canvas 크기 조절될때 내부 프레임 크기 동기화
        def resize_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind('<Configure>', resize_canvas)

        # 내부 프레임 크기 바뀌면 스크롤 영역 재조정
        def frame_configure(event):
            self.canvas.configure(scrollregion=(self.canvas.bbox("all")))
        self.scrollable_frame.bind("<Configure>", frame_configure)

        # 글쓰기 버튼
        self.write_btn = tk.Button(self.body_frame, text="+ 글쓰기", bg="#FF6F0F", fg="white", font=("맑은 고딕", 11, "bold"), command=self.toggle_form, bd=0, padx=12, pady=5)
        self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        # 게시글 불러오기
        self.load_posts()

    # 제목 Entry에 포커스가 생기면 placeholder 제거
    def clear_title_placeholder(self, event=None):
        current = self.title_entry.get()
        if current == self.title_placeholder:
            self.title_entry.delete(0, "end")
            self.title_entry.config(fg="black")

    # 제목 Entry에 포커스가 사라지면 placeholder 복원
    def restore_title_placeholder(self, event=None):
        current = self.title_entry.get().strip()
        if not current:
            self.title_entry.insert(0, self.title_placeholder)
            self.title_entry.config(fg="gray")

    # 내용 Text에 포커스가 생기면 placeholder 제거
    def clear_content_placeholder(self, event=None):
        current = self.content_entry.get("1.0", "end").strip()
        if current == self.content_placeholder:
            self.content_entry.delete("1.0", "end")
            self.content_entry.config(fg="black")

    # 내용 Text에 포커스가 사라지면 placeholder 복원
    def restore_content_placeholder(self, event=None):
        current = self.content_entry.get("1.0", "end").strip()
        if not current:
            self.content_entry.insert("1.0", self.content_placeholder)
            self.content_entry.config(fg="gray")

    # 마우스 휠 스크롤 처리 함수
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # 글쓰기 입력 폼을 보여주거나 숨기는 함수
    def toggle_form(self):
        if self.form_visible:
            self.form_frame.pack_forget() # 폼 숨김
            self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")  # 글쓰기 버튼 다시 표시
        else:
            self.form_frame.pack(fill="x", padx=16, pady=(4,4), side="top", anchor="n") # 폼 표시
            self.write_btn.place_forget()  # 글쓰기 버튼 숨기기
        self.form_visible = not self.form_visible

    # 게시판에 저장된 기존 게시글들을 UI에 표시
    def load_posts(self):
        for post in reversed(self.board.posts): # 최신글이 위로 올라오게
            self.add_post_card(post)

    # 글 등록 처리 함수
    def submit_post(self):
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not title or not content:
            messagebox.showwarning("입력 오류", "제목과 내용을 입력해 주세요.")
            return
        post = self.board.create_post(self.user, title, content, "일반")
        if post: # 글 생성 성공시
            self.add_post_card(post) # UI에 추가
            self.title_entry.delete(0, "end") # 입력창 초기화
            self.content_entry.delete("1.0", "end")
            self.restore_title_placeholder()
            self.restore_content_placeholder()
            self.toggle_form()  # 폼 닫고 버튼 다시 보이게
        else:
            messagebox.showerror("글쓰기 실패", "로그인 후 이용 가능합니다.")


    # 하나의 게시글을 카드 형식으로 UI에 표시
    def add_post_card(self, post):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="ridge", padx=12, pady=7)
        card.pack(fill="x", pady=0, padx=7)

        # 게시글 제목
        tk.Label(card, text=post.title, font=("맑은 고딕", 12, "bold"), bg="white", anchor="w").pack(fill="x")

        # 작성자 닉네임과 작성시간
        tk.Label(card, text=f"{post.user.nick_name} · {post.timestamp.strftime('%m월%d일 %H:%M')}", font=("맑은 고딕",8), fg="#888", bg="white", anchor="w").pack(fill="x")

        # 게시글 내용(줄바꿈 허용, 왼쪽 정렬)
        tk.Label(card, text=post.content, bg="white", font=("맑은 고딕", 10), wraplength=320, justify="left", anchor="w").pack(fill="x", pady=(6,0))

        # 하단 정보(조회수, 좋아요, 댓글 수)
        footer = tk.Frame(card, bg="white")
        tk.Label(footer, text=f"👁 {post.views}", font=("맑은 고딕", 9), bg="white", fg="#666").pack(side="left", padx=(0,15))
        tk.Label(footer, text=f"❤️ {len(post.likes)}", font=("맑은 고딕", 9), bg="white", fg="#FF6F0F").pack(side="left", padx=(0,8))
        tk.Label(footer, text=f"💬 {len(post.comments)}", font=("맑은 고딕", 9), bg="white", fg="#22A6EF").pack(side="left")
        footer.pack(fill="x", pady=(7,0))

    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.body_frame.destroy()