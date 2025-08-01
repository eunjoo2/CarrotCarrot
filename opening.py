import tkinter as tk

class Opening(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=300, height=300, bg="white")
        self.place(relx=0.5, rely=0.5, anchor="center")
        self.configure_widgets()

    def configure_widgets(self):
        image = tk.PhotoImage(file="./img/Daangn_icon_RGB.png").subsample(8, 8)
        logo = tk.Label(self, image=image, bg="white")
        logo.image = image  # 이미지 참조 유지
        logo.place(relx=0.5, rely=0.5, anchor="center")

