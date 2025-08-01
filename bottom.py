import tkinter as tk
from PIL import Image, ImageTk
from tkinter import PhotoImage

class bottom(tk.Frame):
    def __init__(self, master, on_nav_click):
        super().__init__(master, bg="white")
        self.pack(side="bottom", fill="x")

        self.icons = {
            "홈": PhotoImage(file="./img/home-svgrepo-com.svg"),
            "동네생활": PhotoImage(file="./img/journal-page-svgrepo-com.svg"),
            "동네지도": PhotoImage(file="./img/location-svgrepo-com.svg"),
            "채팅": PhotoImage(file="./img/chat-round-dots-svgrepo-com.svg"),
            "나의당근": PhotoImage(file="./img/users-svgrepo-com.svg"),
        }

        for text, icon in self.icons.items():
            btn = tk.Button(
                self,
                image=icon,
                text=text,
                compound="top",
                bd=0,
                relief="flat",
                bg="white",
                fg="black",
                font=("Arial", 9),
                command=lambda t=text: on_nav_click(t)  # 👈 콜백 연결
            )
            btn.pack(side="left", expand=True, fill="x")
