import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class HomeArray(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        # 1. 상단 지역명
        location_frame = tk.Frame(self, bg="white")
        location_frame.pack(fill="x", pady=(10, 5), padx=12)
        tk.Label(location_frame, text="관저2동", font=("Arial", 14, "bold"), bg="white").pack(side="left")

        # 2. 필터 버튼들
        filter_frame = tk.Frame(self, bg="white")
        filter_frame.pack(fill="x", padx=12)
        filters = ["전체", "스포츠 관람권", "중고거래", "걸어서 10분"]
        for f in filters:
            tk.Button(filter_frame, text=f, font=("Arial", 9), padx=10, pady=4).pack(side="left", padx=4)

        # 3. 상품 리스트 (예시 데이터 2개)
        self.create_item(
            item_id="item001",
            image_path="./img/item1.jpg",
            title="한화이글스 vs KT 8.5(화) 3루 내야지정석A 6연석",
            location="둔산 · 23분 전",
            price="20,000원"
        )

        self.create_item(
            item_id="item002",
            image_path="./img/item1.jpg",
            title="한화 썸니품 105 새상품2",
            location="관저동 · 11시간 전",
            price="149,000원"
        )
        self.create_item(
            item_id="item003",
            image_path="./img/item1.jpg",
            title="한화 썸니품 105 새상품3",
            location="관저동 · 11시간 전",
            price="149,000원"
        )
        self.create_item(
            item_id="item004",
            image_path="./img/item1.jpg",
            title="한화 썸니품 105 새상품4",
            location="관저동 · 11시간 전",
            price="149,000원"
        )
        self.create_item(
            item_id="item005",
            image_path="./img/item1.jpg",
            title="한화 썸니품 105 새상품5",
            location="관저동 · 11시간 전",
            price="149,000원"
        )

        # 4. 글쓰기 버튼
        write_btn = tk.Button(self, text="+ 글쓰기", bg="#FF6F0F", fg="white", font=("Arial", 10, "bold"),
                              command=self.write_post)
        write_btn.place(relx=0.8, rely=0.85, width=80, height=40)

    def create_item(self, item_id ,image_path, title, location, price):
        item_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        item_frame.pack(fill="x", padx=12, pady=6)
        item_frame.item_id = item_id

        # 이미지
        try:
            img = Image.open(image_path).resize((70, 70))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None

        img_label = tk.Label(item_frame, image=photo, bg="white")
        img_label.image = photo  # 이미지 유지
        img_label.pack(side="left", padx=6)

        # 텍스트 정보
        text_frame = tk.Frame(item_frame, bg="white")
        text_frame.pack(side="left", fill="both", expand=True)

        tk.Label(text_frame, text=title, font=("Arial", 11, "bold"), bg="white", anchor="w").pack(fill="x", pady=(2, 0))
        tk.Label(text_frame, text=location, font=("Arial", 9), fg="gray", bg="white", anchor="w").pack(fill="x")
        tk.Label(text_frame, text=price, font=("Arial", 11, "bold"), fg="black", bg="white", anchor="w").pack(fill="x")

        item_frame.bind("<Button-1>", self.on_click)
        img_label.bind("<Button-1>", self.on_click)
        text_frame.bind("<Button-1>", self.on_click)



    def write_post(self):
        messagebox.showinfo("글쓰기", "글쓰기 버튼이 눌렸습니다.")

    def on_click(self, event):
        widget = event.widget
        while widget is not None:
            if hasattr(widget, "item_id"):
                item_id = widget.item_id
                #self.show_detail_callback(item_id)
                break
            widget = widget.master