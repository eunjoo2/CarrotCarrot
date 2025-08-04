import tkinter as tk

class Header(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#FF6F0F", height=30)
        self.pack(fill="x")
        self.create_widgets()

    ##### title앞에 self
    def create_widgets(self):
        self.title = tk.Label(self, text="", fg="white", bg=self["bg"], font=("Arial", 16, "bold"))
        self.title.pack(padx=10, pady=10, anchor="w")


    ###### 아래 부분 추가
    def update_title(self, new_title):
        self.title.config(text=new_title)