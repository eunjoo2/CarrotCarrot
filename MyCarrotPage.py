import tkinter as tk

class MyCarrotPage(tk.Frame):
    def __init__(self, parent, user_info=None):
        super().__init__(parent, bg="#f7f7f7")  # 연회색 배경

        # --- 1. 프로필 영역 ---
        profile_frame = tk.Frame(self, bg="white")
        profile_frame.pack(fill="x", pady=(10, 2))

        tk.Label(profile_frame, text=user_info.get("name", "닉네임"), font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=15, pady=10)
        tk.Label(profile_frame, text=f'{user_info.get("temp", "36.5")}℃', bg="#e0f7ff", fg="#2196F3", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Label(profile_frame, text=">", bg="white").pack(side="right", padx=15)

        # --- 2. 서비스 아이콘 2x4 ---
        service_frame = tk.Frame(self, bg="white")
        service_frame.pack(fill="x", pady=(0, 10))

        service_items = [
            ("중고거래", "🛍️"), ("알바", "🔍"),
            ("부동산", "🏠"), ("중고차", "🚗"),
            ("모임", "👥"), ("스토리", "🎬"),
        ]

        for i in range(0, len(service_items), 2):
            row = tk.Frame(service_frame, bg="white")
            row.pack(pady=3)
            for name, emoji in service_items[i:i+2]:
                tk.Label(row, text=f"{emoji} {name}", font=("Arial", 10), width=15, bg="white").pack(side="left", padx=10)

        # --- 3. 관심목록 / 최근 본 글 / 이벤트 ---
        bottom_menu = tk.Frame(self, bg="white")
        bottom_menu.pack(fill="x", pady=(0, 10))

        for text in ["관심목록", "최근 본 글", "이벤트"]:
            tk.Label(bottom_menu, text=text, font=("Arial", 10), width=13, bg="white").pack(side="left", padx=5, pady=10)

        # --- 4. 나의 거래 내역 ---
        my_trades = tk.Frame(self, bg="white")
        my_trades.pack(fill="x")

        for text in ["📋 판매내역", "🛍️ 구매내역"]:
            row = tk.Frame(my_trades, bg="white")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=text, font=("Arial", 10), bg="white").pack(side="left", padx=15, pady=5)
            tk.Label(row, text=">", bg="white").pack(side="right", padx=15)
