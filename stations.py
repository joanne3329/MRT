import json

# Load station data from JSON file
with open('mrt_stations.json', 'r') as f:
    metro_stations = json.load(f)

def get_districts():
    districts = set()
    for line in metro_stations.values():
        for station in line['stations']:
            districts.add(station['district'])
    return sorted(list(districts))

def get_lines():
    return {code: data['name'] for code, data in metro_stations.items()}

# 用於測試的函數
def print_station_info():
    for line_code, line_data in metro_stations.items():
        print(f"\n{line_data['name']} ({line_code}):")
        for station in line_data['stations']:
            print(f"  - {station['name']} ({station['district']})")