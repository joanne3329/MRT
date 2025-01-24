from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__)

def load_mrt_data():
    with open('mrt_stations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
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
    
    mrt_data = {}
    all_stations = {}
    
    for station in data:
        station_name = station['StationName']['Zh_tw']
        lines = [line for line, stations in line_stations.items() if station_name in stations]
        
        station_info = {
            'name': station_name,
            'id': station['StationID'],
            'address': station.get('StationAddress', '地址未提供'),
            'city': station.get('LocationCity', ''),
            'district': station.get('LocationTown', ''),
            'lines': lines
        }
        
        for line in lines:
            if line not in mrt_data:
                mrt_data[line] = []
            mrt_data[line].append(station_info)
        
        if station_name in all_stations:
            for line in lines:
                if line not in all_stations[station_name]['lines']:
                    all_stations[station_name]['lines'].append(line)
        else:
            all_stations[station_name] = station_info
    
    return mrt_data, all_stations

mrt_data, all_stations = load_mrt_data()

@app.route('/')
def index():
    return render_template('index.html', lines=list(mrt_data.keys()))

@app.route('/spin')
def spin():
    selected_line = request.args.get('line', '全部')
    if selected_line == "全部":
        stations = [station for stations in mrt_data.values() for station in stations]
    else:
        stations = mrt_data.get(selected_line, [])
    
    if not stations:
        return jsonify({'error': '沒有符合條件的捷運站！'})
    
    result = random.choice(stations)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 