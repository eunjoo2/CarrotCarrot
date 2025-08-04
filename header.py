import tkinter as tk

class Header(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#FFFFFF", height=30)
        self.pack(fill="x")
        self.create_widgets()

    ##### title앞에 self
    def create_widgets(self):
        self.top_frame = tk.Frame(self, bg=self["bg"])
        self.top_frame.pack(fill="x")

        self.back_img = tk.PhotoImage(file="./img/chat_left_arrow.png")
        self.back_btn = tk.Button(self.top_frame, image=self.back_img, command=self.handle_back,
                                  highlightthickness=0, borderwidth=0, bg=self["bg"], activebackground=self["bg"])

        self.title = tk.Label(self.top_frame, text="", fg="white", bg=self["bg"], font=("Arial", 16, "bold"))
        self.title.grid(row=0, column=1, sticky="w", padx=5, pady=10)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # self.title = tk.Label(self, text="", fg="#000000", bg=self["bg"], font=("Arial", 12))
        # self.title.pack(padx=10, pady=10, anchor="w")


    ###### 아래 부분 추가
    def update_title(self, new_title):
        self.title.config(text=new_title)

    def back_button(self, command=None):
        self.back_btn.grid_remove()
        self.back_command = command
        if command:
            self.back_btn.grid(row=0, column=0, padx=5, pady=5)

    def handle_back(self):
        if self.back_command:
            self.back_command()