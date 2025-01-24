import json
import random
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class MRTFoodRoulette:
    def __init__(self):
        # 設定主視窗
        self.root = ttk.Window(themename="cosmo")
        self.root.title("台北捷運美食轉盤")
        self.root.geometry("800x600")
        
        # 載入資料
        self.load_data()
        
        # 建立UI
        self.create_ui()
        
    def load_data(self):
        try:
            with open('mrt_food.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.restaurants = data['restaurants']
                
            # 取得所有唯一的區域和捷運線
            self.areas = sorted(list(set(r['area'] for r in self.restaurants)))
            self.mrt_lines = sorted(list(set(r['mrt_line'] for r in self.restaurants)))
        except FileNotFoundError:
            self.restaurants = []
            self.areas = []
            self.mrt_lines = []
    
    def create_ui(self):
        # 建立主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 標題
        title_label = ttk.Label(
            main_frame,
            text="台北捷運美食轉盤",
            font=("Taipei Sans TC Beta", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # 篩選區域
        filter_frame = ttk.LabelFrame(main_frame, text="篩選條件", padding="10")
        filter_frame.pack(fill=tk.X, pady=10)
        
        # 行政區選擇
        area_frame = ttk.Frame(filter_frame)
        area_frame.pack(fill=tk.X, pady=5)
        ttk.Label(area_frame, text="行政區：").pack(side=tk.LEFT)
        self.area_var = tk.StringVar(value="全部")
        area_cb = ttk.Combobox(
            area_frame,
            textvariable=self.area_var,
            values=["全部"] + self.areas,
            state="readonly",
            width=15
        )
        area_cb.pack(side=tk.LEFT, padx=5)
        
        # 捷運線選擇
        line_frame = ttk.Frame(filter_frame)
        line_frame.pack(fill=tk.X, pady=5)
        ttk.Label(line_frame, text="捷運線：").pack(side=tk.LEFT)
        self.line_var = tk.StringVar(value="全部")
        line_cb = ttk.Combobox(
            line_frame,
            textvariable=self.line_var,
            values=["全部"] + self.mrt_lines,
            state="readonly",
            width=15
        )
        line_cb.pack(side=tk.LEFT, padx=5)
        
        # 結果顯示區
        self.result_frame = ttk.LabelFrame(main_frame, text="抽選結果", padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_label = ttk.Label(
            self.result_frame,
            text="準備開始抽選...",
            font=("Taipei Sans TC Beta", 16)
        )
        self.result_label.pack(pady=20)
        
        # 抽選按鈕
        self.spin_button = ttk.Button(
            main_frame,
            text="開始抽選",
            command=self.spin,
            style="Accent.TButton",
            width=20
        )
        self.spin_button.pack(pady=20)
        
    def filter_restaurants(self):
        filtered = self.restaurants.copy()
        
        if self.area_var.get() != "全部":
            filtered = [r for r in filtered if r['area'] == self.area_var.get()]
            
        if self.line_var.get() != "全部":
            filtered = [r for r in filtered if r['mrt_line'] == self.line_var.get()]
            
        return filtered
    
    def spin(self):
        filtered_restaurants = self.filter_restaurants()
        
        if not filtered_restaurants:
            self.result_label.config(
                text="沒有符合條件的餐廳！\n請調整篩選條件後重試。",
                foreground="red"
            )
            return
        
        # 停用按鈕
        self.spin_button.configure(state="disabled")
        self.root.update()
        
        # 模擬轉動效果
        for _ in range(20):
            restaurant = random.choice(filtered_restaurants)
            self.result_label.config(
                text=f"抽選中...\n{restaurant['name']}",
                foreground="gray"
            )
            self.root.update()
            self.root.after(50)
        
        # 最終結果
        result = random.choice(filtered_restaurants)
        result_text = (
            f"恭喜！抽中了：\n\n"
            f"【{result['name']}】\n"
            f"位於：{result['area']} {result['station']}\n"
            f"類型：{result['type']}\n"
            f"價位：{result['price_range']}"
        )
        self.result_label.config(
            text=result_text,
            foreground="black"
        )
        
        # 重新啟用按鈕
        self.spin_button.configure(state="normal")

def main():
    app = MRTFoodRoulette()
    app.root.mainloop()

if __name__ == "__main__":
    main() 