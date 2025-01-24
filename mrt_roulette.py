import json
import random
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MRTRoulette:
    def __init__(self):
        # 設定主視窗
        self.root = ttk.Window(themename="cosmo")
        self.root.title("台北捷運站轉盤")
        self.root.geometry("800x600")
        
        # 載入捷運資料
        self.load_mrt_data()
        
        # 建立UI
        self.create_ui()
        
    def load_mrt_data(self):
        try:
            # 讀取JSON檔案
            with open('mrt_stations.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 整理資料結構
            self.mrt_data = {}
            self.all_stations = {}
            
            # 各路線的站點列表（依序）
            line_stations = {
                '板南線': ['頂埔', '永寧', '土城', '海山', '亞東醫院', '府中', '板橋', '新埔', '江子翠', 
                          '龍山寺', '西門', '台北車站', '善導寺', '忠孝新生', '忠孝復興', '忠孝敦化', 
                          '國父紀念館', '市政府', '永春', '後山埤', '昆陽', '南港', '南港展覽館'],
                
                '文湖線': ['動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', 
                          '大安', '忠孝復興', '南京復興', '中山國中', '松山機場', '大直', '劍南路', '西湖', 
                          '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館'],
                
                '松山新店線': ['松山', '南京三民', '台北小巨蛋', '南京復興', '松江南京', '中山', '北門', 
                              '西門', '小南門', '中正紀念堂', '古亭', '台電大樓', '公館', '萬隆', '景美', 
                              '大坪林', '七張', '新店區公所', '新店'],
                
                '中和新蘆線': ['南勢角', '景安', '永安市場', '頂溪', '古亭', '東門', '忠孝新生', '松江南京', 
                              '行天宮', '中山國小', '民權西路', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', 
                              '頭前庄', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國中', '徐匯中學', 
                              '三民高中', '蘆洲'],
                
                '淡水信義線': ['淡水', '紅樹林', '竹圍', '關渡', '忠義', '復興崗', '北投', '奇岩', '唭哩岸', 
                              '石牌', '明德', '芝山', '士林', '劍潭', '圓山', '民權西路', '雙連', '中山', 
                              '台北車站', '台大醫院', '中正紀念堂', '東門', '大安森林公園', '大安', 
                              '信義安和', '台北101/世貿', '象山'],
                
                '環狀線': ['大坪林', '十四張', '秀朗橋', '景平', '景安', '中和', '橋和', '中原', '板新', 
                          '板橋', '新埔民生', '頭前庄', '幸福', '新北產業園區']
            }
            
            for station in data:
                station_name = station['StationName']['Zh_tw']
                
                # 找出該站所屬的路線
                lines = [line for line, stations in line_stations.items() if station_name in stations]
                
                # 建立站點資訊
                station_info = {
                    'name': station_name,
                    'id': station['StationID'],
                    'address': station.get('StationAddress', '地址未提供'),
                    'city': station.get('LocationCity', ''),
                    'district': station.get('LocationTown', ''),
                    'lines': lines
                }
                
                # 加入到路線資料
                for line in lines:
                    if line not in self.mrt_data:
                        self.mrt_data[line] = []
                    self.mrt_data[line].append(station_info)
                
                # 處理站點資料
                if station_name in self.all_stations:
                    # 如果站點已存在，合併路線資訊
                    for line in lines:
                        if line not in self.all_stations[station_name]['lines']:
                            self.all_stations[station_name]['lines'].append(line)
                else:
                    # 新增站點
                    self.all_stations[station_name] = station_info
            
            # 取得所有唯一的捷運線
            self.mrt_lines = sorted(list(line_stations.keys()))
            
        except Exception as e:
            print(f"載入資料時發生錯誤: {e}")
            self.mrt_data = {}
            self.mrt_lines = []
            self.all_stations = {}
    
    def create_ui(self):
        # 建立主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 標題
        title_label = ttk.Label(
            main_frame,
            text="台北捷運站轉盤",
            font=("Taipei Sans TC Beta", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # 篩選區域
        filter_frame = ttk.LabelFrame(main_frame, text="選擇條件", padding="10")
        filter_frame.pack(fill=tk.X, pady=10)
        
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
            width=20
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
    
    def get_filtered_stations(self):
        selected_line = self.line_var.get()
        if selected_line == "全部":
            return [station for stations in self.mrt_data.values() for station in stations]
        else:
            return self.mrt_data.get(selected_line, [])
    
    def spin(self):
        stations = self.get_filtered_stations()
        
        if not stations:
            self.result_label.config(
                text="沒有符合條件的捷運站！\n請調整選擇後重試。",
                foreground="red"
            )
            return
        
        # 停用按鈕
        self.spin_button.configure(state="disabled")
        self.root.update()
        
        # 模擬轉動效果
        for _ in range(20):
            station = random.choice(stations)
            self.result_label.config(
                text=f"抽選中...\n{station['name']}",
                foreground="gray"
            )
            self.root.update()
            self.root.after(50)
        
        # 最終結果
        result = random.choice(stations)
        
        # 取得該站的所有資訊
        station_info = self.all_stations[result['name']]
        
        # 使用 get 方法安全地取得資料
        result_text = (
            f"抽中了：\n\n"
            f"【{station_info['name']}】站\n"
            f"站點編號：{station_info['id']}\n"
            f"地址：{station_info.get('address', '地址未提供')}\n"
            f"所在地：{station_info.get('city', '')}{station_info.get('district', '')}\n"
            f"所屬路線：{'、'.join(station_info.get('lines', []))}"
        )
        
        self.result_label.config(
            text=result_text,
            foreground="black"
        )
        
        # 重新啟用按鈕
        self.spin_button.configure(state="normal")

def main():
    app = MRTRoulette()
    app.root.mainloop()

if __name__ == "__main__":
    main()