import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class AreaMap(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        self.center = "36.348141,127.384815"
        self.zoom = 16  # 초기 줌 레벨
        self.size = "400x600"
        self.api_key = "AIzaSyDVpf_KQ0Wu_ex6dsr9qbSFP8b6y9_yWv4"  # 본인 키로 교체!

        self.label = tk.Label(self)
        self.label.pack()

        self.load_map()

        # 윈도우, 리눅스용 마우스 휠 이벤트 바인딩
        self.label.bind("<MouseWheel>", self.on_mouse_wheel)       # Windows, MacOS
        self.label.bind("<Button-4>", self.on_mouse_wheel_linux)    # Linux scroll up
        self.label.bind("<Button-5>", self.on_mouse_wheel_linux)    # Linux scroll down

    def load_map(self):
        url = "https://maps.googleapis.com/maps/api/staticmap"
        params = {
            "center": self.center,
            "zoom": str(self.zoom),
            "size": self.size,
            "markers": f"color:red|label:P|{self.center}",
            "language": "ko",
            "key": self.api_key
        }

        response = requests.get(url, params=params)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        self.photo = ImageTk.PhotoImage(img)

        self.label.config(image=self.photo)
        self.label.image = self.photo

    def on_mouse_wheel(self, event):
        # Windows / MacOS
        if event.delta > 0:
            self.zoom = min(self.zoom + 1, 21)  # 최대 21레벨
        else:
            self.zoom = max(self.zoom - 1, 0)   # 최소 0레벨
        self.load_map()

    def on_mouse_wheel_linux(self, event):
        # Linux는 버튼 4가 스크롤 업, 5가 스크롤 다운
        if event.num == 4:
            self.zoom = min(self.zoom + 1, 21)
        elif event.num == 5:
            self.zoom = max(self.zoom - 1, 0)
        self.load_map()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("420x620")
    AreaMap(root)
    root.mainloop()
