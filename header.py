import tkinter as tk

def create_header(root, change_page_callback):
    header = tk.Frame(root, bg="#ff6f0f", height=50)
    header.pack(fill="x")

    logo = tk.Label(header, text="🥕 CarrotCarrot", bg="#ff6f0f", fg="white", font=("Arial", 14, "bold"))
    logo.pack(side="left", padx=10)

    btn_home = tk.Button(header, text="홈", command=lambda: change_page_callback("home"))
    btn_upload = tk.Button(header, text="글쓰기", command=lambda: change_page_callback("upload"))

    btn_upload.pack(side="right", padx=5)
    btn_home.pack(side="right", padx=5)

    return header