import tkinter as tk

class Header(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#FF6F0F", height=50)
        self.pack(fill="x")
        self.create_widgets()

    def create_widgets(self):
<<<<<<< HEAD
        title = tk.Label(self, text="당근마켓", bg="#FF6F0F", fg="white", font=("Arial", 16, "bold"))
=======
        title = tk.Label(self, text="당근마켓", fg="white", font=("Arial", 16, "bold"))
>>>>>>> 0997ef83e04c3f5561e9f2ed221725238cd1a15b
        title.pack(padx=10, pady=10, anchor="w")
