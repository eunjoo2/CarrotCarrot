import tkinter as tk
from PIL import Image, ImageTk

class bottom(tk.Frame):
    def __init__(self, master, on_nav_click):
        super().__init__(master, bg="white")
        self.pack(side="bottom", fill="x")

        # SVG → PNG로 변환된 이미지 사용
        icon_files = {
            "홈": "./img/home.png",
            "동네생활": "./img/journal.png",
            "동네지도": "./img/location.png",
            "채팅": "./img/chat.png",
            "나의당근": "./img/user.png",
        }

        self.icons = {}
        for key, path in icon_files.items():
            img = Image.open(path)
            img = img.resize((24, 24))  # 아이콘 크기 조절
            self.icons[key] = ImageTk.PhotoImage(img)

        # 버튼 생성
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
                command=lambda t=text: on_nav_click(t)
            )
            btn.pack(side="left", expand=True, fill="x")
