import pandas as pd
import folium
from Tools.scripts.dutree import display
from folium.plugins import MarkerCluster
import numpy as np
import random

# 對地圖可視化進行抽樣，提取 20000 條記錄
file_path = "small_data.csv"
num_rows = sum(1 for row in open(file_path, 'r', encoding='utf-8')) - 1
sample_size = 20000
skip_rows = sorted(random.sample(range(1, num_rows + 1), num_rows - sample_size))

df = pd.read_csv(file_path, skiprows=skip_rows)
print(df.head(10))

# 過濾掉缺失緯度和經度值的行
df_loc = df.loc[(~df.Start_Lat.isna()) & (~df.Start_Lng.isna())]

# 創建帶有聚類標記的 Folium 地圖的函數
def create_map(df_loc, latitude, longitude, zoom, tiles='OpenStreetMap'):
    world_map = folium.Map(location=[latitude, longitude], zoom_start=zoom, tiles=tiles)
    marker_cluster = MarkerCluster().add_to(world_map)

    # 遍歷 DataFrame 行，將每個標記添加到聚類中
    for idx, row in df_loc.iterrows():
        folium.Marker(
            location=[row['Start_Lat'], row['Start_Lng']],
            # 在此處可以添加更多標記的屬性，例如彈出窗口
            popup=f"緯度, 經度: {row['Start_Lat']}, {row['Start_Lng']}"
        ).add_to(marker_cluster)

    return world_map

# 美國城市的座標
us_cities_coords = {
    "紐約": {"lat": 40.7128, "lon": -74.0060},
    "洛杉磯": {"lat": 34.0522, "lon": -118.2437},
    # 根據需要添加更多城市的座標
}

# 創建並顯示一個 Folium 地圖，其中包含聚類標記，以展示事故位置，地圖中心位於美國地理中心
map_us = create_map(df_loc, 39.50, -98.35, 4, tiles="Cartodbdark_matter")

map_us.show_in_browser()
