import tkinter as tk

class AreaLifePage(tk.Frame):
    def __init__(self, parent, board, user):
        tk.Frame.__init__(self, parent)
        self.board = board
        self.user = user

        # body_frame 만들기
        self.body_frame = tk.Frame(self.parent, bg = "white")