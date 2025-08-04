import tkinter as tk
from PIL import Image, ImageTk


class DetailPage(tk.Frame):
    def __init__(self, parent, item_data,item_id):
        super().__init__(parent, bg="white")
        self.item_data = item_data  # 딕셔너리로 아이템 정보 받음
        #data = get_item_by_id(item_id)
        #self.create_ui(data)

        # 상단 이미지
        img = Image.open(item_data["image_path"])
        img = img.resize((400, 300))
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(self, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(pady=(10, 0))

        # 사용자 정보 영역
        user_frame = tk.Frame(self, bg="white")
        user_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(user_frame, text="🌼 " + item_data["user_nickname"], bg="white", font=("Arial", 11, "bold")).pack(side="left")
        tk.Label(user_frame, text=f"{item_data['region']}", bg="white", fg="gray", font=("Arial", 9)).pack(side="left", padx=10)
        tk.Label(user_frame, text=f"{item_data['temp']}℃ 😆", bg="white", fg="orange", font=("Arial", 9)).pack(side="right")

        # 상품 제목 + 가격
        tk.Label(self, text=item_data["title"], bg="white", font=("Arial", 14, "bold")).pack(anchor="w", padx=20)
        tk.Label(self, text=item_data["price"] + "원", bg="white", fg="green", font=("Arial", 13)).pack(anchor="w", padx=20)

        # 카테고리, 업로드 시간
        tk.Label(self, text=item_data["category_time"], bg="white", fg="gray", font=("Arial", 9)).pack(anchor="w", padx=20, pady=(5, 0))

        # 상품 설명
        desc = tk.Label(self, text=item_data["description"], bg="white", justify="left", wraplength=360, font=("Arial", 11))
        desc.pack(anchor="w", padx=20, pady=(10, 0))

        # 거래 희망 장소
        place = tk.Label(self, text="📍 거래 희망 장소: " + item_data["location"], bg="white", fg="gray", font=("Arial", 10))
        place.pack(anchor="w", padx=20, pady=(10, 20))

        # 하단 관심 메시지
        bottom_frame = tk.Frame(self, bg="white", relief="ridge", bd=1)
        bottom_frame.pack(side="bottom", fill="x")

        entry = tk.Entry(bottom_frame, font=("Arial", 10), width=40)
        entry.insert(0, "안녕하세요. 관심있어서 연락드려요!")
        entry.pack(side="left", padx=10, pady=10)

        tk.Button(bottom_frame, text="보내기", bg="orange", fg="white", font=("Arial", 10)).pack(side="right", padx=10)


# 샘플 데이터 예시
sample_item = {
    "item_id": "item001",
    "image_path": "./img/item1.jpg",
    "title": "한화이글스 25 썸머 유니폼 L",
    "price": "155,000",
    "category_time": "스포츠/레저 · 꿀옷 3시간 전",
    "description": "한화이글스 2025 썸머 유니폼 노마킹 새상품입니다.\n스파이더 콜라보 제품이고, 사이즈는 100(L)입니다.\n정가는 149,000원이에요\n흡습속건 기능성 원단이라 시원하게 입을 수 있어요",
    "location": "초록마을2단지",
    "user_nickname": "괜찮아",
    "region": "서구 복수동",
    "temp": "56.7",
}
