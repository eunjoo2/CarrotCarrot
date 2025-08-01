import tkinter as tk

class bottom (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#ffffff", height=30)
        self.pack(side=tk.BOTTOM, fill="x")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="하단 버튼", fg="#000000",bg="#ffffff" ,font=("Arial", 16, "bold") )
        title.pack(padx=10, pady=10, anchor="w")