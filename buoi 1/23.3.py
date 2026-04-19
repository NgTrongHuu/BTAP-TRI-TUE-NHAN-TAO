import folium
from folium.plugins import HeatMap
import numpy as np
np.random.seed(42)
center_lat, center_lon = 10.7769, 106.7009
data = []
clusters = [(10.78, 106.70, 80), (10.73, 106.72, 60), (10.85, 106.75, 60)]
for clat, clon, n in clusters:
    lats = np.random.normal(clat, 0.008, n)
    lons = np.random.normal(clon, 0.008, n)
    data.extend([[lat, lon] for lat, lon in zip(lats, lons)])
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
HeatMap(data, radius=15, blur=10, max_zoom=17).add_to(m)
m.save("bai_23_3_heatmap.html")