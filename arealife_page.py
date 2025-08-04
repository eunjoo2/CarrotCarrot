import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AreaLifePage:
    def __init__(self, parent, board, user):
        self.board = board  # 게시판
        self.user = user  # 로그인된 사용자
        self.form_visible = False
        self.detail_frame = None
        self.is_editing = False

        # 글쓰기 화면의 메인 프레임 생성
        self.body_frame = tk.Frame(parent, bg="#FAFAF6")
        self.body_frame.pack(expand=True, fill="both")

        # 글쓰기 입력 폼 프레임 (초기에는 숨김)
        self.form_frame = tk.Frame(self.body_frame, bg="#FAFAF6")

        # 제목 Entry
        self.title_entry = tk.Entry(self.form_frame, width=40, font=("맑은 고딕", 10))
        self.title_entry.grid(row=0, column=1, sticky="w", padx=(7, 0))
        self.title_placeholder = "제목을 입력하세요."
        self.title_entry.insert(0, self.title_placeholder)
        self.title_entry.config(fg="gray")
        self.title_entry.bind("<FocusIn>", self.clear_title_placeholder)
        self.title_entry.bind("<FocusOut>", self.restore_title_placeholder)

        # 내용 Text
        self.content_entry = tk.Text(self.form_frame, width=40, height=3, font=("맑은 고딕", 10))
        self.content_entry.grid(row=1, column=1, sticky="w", padx=(7, 0), pady=3)
        self.content_placeholder = "둔산동 이웃과 이야기를 나눠보세요."
        self.content_entry.insert("1.0", self.content_placeholder)
        self.content_entry.config(fg="gray")
        self.content_entry.bind("<FocusIn>", self.clear_content_placeholder)
        self.content_entry.bind("<FocusOut>", self.restore_content_placeholder)

        # 등록 버튼
        self.submit_btn = tk.Button(self.form_frame, text="등록", bg="#FF6F0F", fg="white", font=("맑은 고딕", 10, "bold"),
                                    width=8, command=self.submit_post, bd=0)
        self.submit_btn.grid(row=2, column=1, sticky="e", pady=(4, 0))
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
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)

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
        self.write_btn = tk.Button(self.body_frame, text="+ 글쓰기", bg="#FF6F0F", fg="white", font=("맑은 고딕", 11, "bold"),
                                   command=self.toggle_form, bd=0, padx=12, pady=5)
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
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass

    # 글쓰기 입력 폼을 보여주거나 숨기는 함수
    def toggle_form(self):
        if self.form_visible:
            self.form_frame.pack_forget()  # 폼 숨김
            self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")  # 글쓰기 버튼 다시 표시
        else:
            self.form_frame.pack(fill="x", padx=16, pady=(4, 4), side="top", anchor="n")  # 폼 표시
            self.write_btn.place_forget()  # 글쓰기 버튼 숨기기
        self.form_visible = not self.form_visible

    # 게시판에 저장된 기존 게시글들을 UI에 표시
    def load_posts(self):
        for post in reversed(self.board.posts):  # 최신글이 위로 올라오게
            self.add_post_card(post)

    # 글 등록 처리 함수
    def submit_post(self):
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end").strip()
        if not title or not content:
            messagebox.showwarning("입력 오류", "제목과 내용을 입력해 주세요.")
            return
        post = self.board.create_post(self.user, title, content, "일반")
        if post:
            if self.is_editing: # 수정 중이면 목록 전체 갱신
                self.show_post_list()
                self.is_editing = False
            else: # 새 글쓰기 일때 UI 추가
                self.add_post_card(post)

            self.title_entry.delete(0, "end")  # 입력창 초기화
            self.content_entry.delete("1.0", "end")
            self.restore_title_placeholder()
            self.restore_content_placeholder()
            self.toggle_form()  # 폼 닫고 버튼 다시 보이게
        else:
            messagebox.showerror("글쓰기 실패", "로그인 후 이용 가능합니다.")

    # 하나의 게시글을 카드 형식으로 UI에 표시
    def add_post_card(self, post):
        card = tk.Frame(self.scrollable_frame, bg="white", padx=12, pady=7, cursor="hand2")
        card.pack(fill="x", pady=0, padx=7)

        # 작성자 닉네임과 작성시간
        info_text = f'{post.user.nick_name} · {post.timestamp.strftime('%m월 %d일 %H:%M')}'
        info_label = tk.Label(card, text=info_text, font=("맑은 고딕", 8), fg="#888", bg="white", anchor="w", justify="left")
        info_label.pack(fill="x", anchor="w")

        # 게시글 제목
        title_label = tk.Label(card, text=post.title, font=("맑은 고딕", 12, "bold"), bg="white", anchor="w")
        title_label.pack(fill="x")

        # 게시글 내용(줄바꿈 허용, 왼쪽 정렬)
        content_label = tk.Label(card, text=post.content, bg="white", font=("맑은 고딕", 10), wraplength=320, justify="left", anchor="w")
        content_label.pack(fill="x", pady=(6, 0))

        # 하단 정보(조회수, 좋아요, 댓글 수)
        footer = tk.Frame(card, bg="white")
        tk.Label(footer, text=f"👁 {post.views}", font=("맑은 고딕", 9), bg="white", fg="#666").pack(side="left", padx=(0, 15))
        tk.Label(footer, text=f"👍 {len(post.likes)}", font=("맑은 고딕", 9), bg="white", fg="#FF6F0F").pack(side="left", padx=(0, 8))
        tk.Label(footer, text=f"💬 {len(post.comments)}", font=("맑은 고딕", 9), bg="white", fg="#22A6EF").pack(side="left")
        footer.pack(fill="x", pady=(7, 0))

        # 하단 구분선 추가(Frame을 height=1로 얇은 선처럼 보이게 함)
        # sep = tk.Frame(self.scrollable_frame, bg="#DDDDDD", height=1)
        sep = tk.Frame(self.scrollable_frame, highlightbackground="#DDDDDD", highlightthickness=1)
        sep.pack(fill="x", padx=7, pady=(0, 7))

        # 게시글 클릭 함수
        def on_card_click(event):
            self.show_post_detail(post)

        # 내부 위젯 -> 클릭 이벤트를 카드에 넘기기
        def bind_all_widgets(widget):
            widget.bind("<Button-1>", on_card_click)
            for child in widget.winfo_children():
                bind_all_widgets(child)

        bind_all_widgets(card)

    def destroy(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.body_frame.destroy()

    # 상세보기 함수
    def show_post_detail(self, post):
        self.popup_post = post

        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # 상세 보기 프레임 생성
        self.detail_frame = tk.Frame(self.body_frame, bg="white")
        self.detail_frame.pack(fill="both", expand=True)

        # 상단 버튼 컨테이너
        top_btn_frame = tk.Frame(self.detail_frame, bg="white")
        top_btn_frame.pack(fill="both", anchor="n", pady=(5,0))

        try:
            img = Image.open("img/left_arrow.png").resize((25, 25))
            self.back_img = ImageTk.PhotoImage(img)
            back_btn = tk.Button(top_btn_frame, image=self.back_img, command=self.show_post_list, bd=0, bg="white", activebackground="white", cursor="hand2")
        except Exception:
            back_btn = tk.Button(top_btn_frame, text="←", command=self.show_post_list, bd=0, bg="white", font=("맑은 고딕", 12, "bold"))
        back_btn.pack(side="left", padx=(5,0))

        try:
            img = Image.open("img/menu.png").resize((25, 25))
            self.menu_img = ImageTk.PhotoImage(img)
            self.current_post = post
            menu_btn = tk.Button(top_btn_frame, image=self.menu_img, command=self.call_modify_post, bd=0, bg="white", activebackground="white", cursor="hand2")
        except Exception:
            menu_btn = tk.Button(top_btn_frame, text="=", command=self.modify_post, bd=0, bg="white", font=("맑은 고딕", 12, "bold"))
        menu_btn.pack(side="right", padx=(0,5))

        # 작성자/시간
        info_text = f'{post.user.nick_name} · {post.timestamp.strftime('%m월 %d일 %H:%M')}'
        info_label = tk.Label(self.detail_frame, text=info_text, font=("맑은 고딕", 8), fg="#888", bg="white", anchor="w",justify="left")
        info_label.pack(anchor="w")

        # 제목
        title_label = tk.Label(self.detail_frame, text=post.title, font=("맑은 고딕", 14, "bold"), bg="white")
        title_label.pack(anchor="w", pady=(10, 5))

        # 본문
        meta_label = tk.Label(self.detail_frame, text=post.content, wraplength=360, justify="left", font=("맑은 고딕", 11),bg="white")
        meta_label.pack(anchor="w", pady=(10, 0))

    def modify_post(self, post):
        menu = tk.Menu(self.detail_frame, tearoff=0, bg="white", fg="black", font=("맑은 고딕", 10))
        menu.add_command(label="수정", command=self.edit_selected_post)
        menu.add_command(label="삭제", command=self.delete_selected_post)

        try:
            menu.tk_popup(self.body_frame.winfo_pointerx(), self.body_frame.winfo_pointery())
        finally:
            menu.grab_release()

    def edit_selected_post(self):
        post = self.popup_post
        self.is_editing = True

        # 기존 폼이 없거나 파괴되었으면 다시 생성 (필요하다면)
        if not self.form_frame or not self.form_frame.winfo_exists():
            self.form_frame = tk.Frame(self.body_frame, bg="#FAFAF6")

            # 제목 Entry
            self.title_entry = tk.Entry(self.form_frame, width=40, font=("맑은 고딕", 10))
            self.title_entry.grid(row=0, column=1, sticky="w", padx=(7, 0))

            # 내용 Text (여러 줄)
            self.content_entry = tk.Text(self.form_frame, width=40, height=3, font=("맑은 고딕", 10))
            self.content_entry.grid(row=1, column=1, sticky="w", padx=(7, 0), pady=3)

            # 등록 버튼
            self.submit_btn = tk.Button(self.form_frame, text="등록", bg="#FF6F0F", fg="white",
                                        font=("맑은 고딕", 10, "bold"), width=8,
                                        command=self.submit_post, bd=0)
            self.submit_btn.grid(row=2, column=1, sticky="e", pady=(4, 0))

            self.form_frame.columnconfigure(1, weight=1)

        # 글쓰기 폼 보이기 (이미 보여져 있다면 중복 pack 안 되도록 체크 가능)
        if not self.form_visible:
            self.form_frame.pack(fill="x", padx=16, pady=(4, 4), side="top", anchor="n")
            self.form_visible = True


        # 기존 제목, 내용 채워넣기
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, post.title)
        self.title_entry.config(fg="black")

        self.content_entry.delete("1.0", "end")
        self.content_entry.insert("1.0", post.content)
        self.content_entry.config(fg="black")

        # 기존 글 삭제(수정은 새로은 글로 대체)
        if post in self.board.posts:
            self.board.posts.remove(post)

        # self.show_post_list() # 글 목록 갱신

    def call_modify_post(self):
        self.modify_post(self.popup_post)

    def delete_selected_post(self):
        post = self.popup_post
        confirm = messagebox.askyesno("삭제 확인", "정말 이 글을 삭제하시겠습니까?")
        if confirm:
            if post in self.board.posts:
                self.board.posts.remove(post)
            self.show_post_list() # 목록으로 돌아가기

    # 목록으로 복귀 함수
    def show_post_list(self):
        if self.detail_frame:
            self.detail_frame.destroy()
            self.detail_frame = None

        self.form_frame.pack_forget()  # 수정/글쓰기 폼 초기에는 숨김
        self.write_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

        # 글 목록은 스크롤 프레임 안에서 다시 로드
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()  # 기존 글 카드 제거

        self.load_posts()  # 기존 글 다시 불러오기