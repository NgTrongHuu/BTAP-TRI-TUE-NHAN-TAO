
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson
import webbrowser, os, json
from datetime import datetime, timedelta

np.random.seed(42)

# 1. Định nghĩa mạng đường đơn giản (các nút giao TP.HCM)
nodes = {
    "A": (10.780, 106.700),  # Ngã tư Nguyễn Huệ
    "B": (10.785, 106.695),  # Ngã tư CMT8
    "C": (10.790, 106.700),  # Ngã tư Điện Biên Phủ
    "D": (10.785, 106.705),  # Hai Bà Trưng
    "E": (10.775, 106.695),  # Nguyễn Thị Minh Khai
    "F": (10.770, 106.700),  # Trần Hưng Đạo
    "G": (10.775, 106.705),  # Pasteur
    "H": (10.790, 106.690),  # Lý Thường Kiệt
}

# 2. Định nghĩa 4 xe với lộ trình khác nhau
vehicles = [
    {"id": "Xe 1", "color": "#e74c3c", "route": ["A", "B", "H", "C", "D", "A"]},
    {"id": "Xe 2", "color": "#3498db", "route": ["F", "E", "B", "C", "D", "G", "F"]},
    {"id": "Xe 3", "color": "#2ecc71", "route": ["C", "H", "B", "E", "F", "G", "D", "C"]},
    {"id": "Xe 4", "color": "#9b59b6", "route": ["G", "D", "C", "B", "A", "E", "F", "G"]},
]

# 3. Tạo dữ liệu di chuyển với nội suy (mượt hơn)
base_time = datetime(2024, 1, 1, 8, 0, 0)

def interpolate(p1, p2, steps=5):
    """Nội suy giữa 2 điểm để xe di chuyển mượt"""
    lats = np.linspace(p1[0], p2[0], steps + 1)[:-1]
    lons = np.linspace(p1[1], p2[1], steps + 1)[:-1]
    return list(zip(lats, lons))

features = []
for v in vehicles:
    coords = []
    times = []
    t = base_time
    for i in range(len(v["route"]) - 1):
        p1 = nodes[v["route"][i]]
        p2 = nodes[v["route"][i + 1]]
        interp = interpolate(p1, p2, steps=6)
        for pt in interp:
            coords.append([pt[1], pt[0]])  # GeoJSON: [lon, lat]
            times.append(t.strftime("%Y-%m-%dT%H:%M:%S"))
            t += timedelta(minutes=2)
    # Điểm cuối
    last = nodes[v["route"][-1]]
    coords.append([last[1], last[0]])
    times.append(t.strftime("%Y-%m-%dT%H:%M:%S"))

    features.append({
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "times": times,
            "style": {"color": v["color"], "weight": 5},
            "icon": "circle",
            "iconstyle": {
                "fillColor": v["color"], "fillOpacity": 0.9,
                "stroke": "true", "radius": 7
            },
            "popup": f"<b>{v['id']}</b><br>Lộ trình: {' → '.join(v['route'])}",
            "tooltip": v["id"]
        }
    })

# 4. Vẽ bản đồ
m = folium.Map(location=[10.782, 106.699], zoom_start=16, tiles="CartoDB positron")

# Vẽ mạng đường nền
edges = [("A","B"),("B","C"),("B","H"),("C","D"),("D","G"),("D","A"),
         ("A","E"),("E","B"),("E","F"),("F","G"),("G","A")]
for n1, n2 in edges:
    folium.PolyLine([nodes[n1], nodes[n2]], color="gray",
                    weight=2, opacity=0.4).add_to(m)

# Marker các nút giao
for name, coord in nodes.items():
    folium.CircleMarker(coord, radius=5, color="#333", fill=True,
                        fill_opacity=0.6, tooltip=f"Nút {name}").add_to(m)

# Animation xe di chuyển
TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT2M",        # mỗi bước = 2 phút
    duration="PT1M",      # vết xe hiển thị 1 phút
    auto_play=True,
    loop=True,
    max_speed=5,
    add_last_point=True,
).add_to(m)

legend = """
<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
     padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:12px">
    <b>Bài 23.14 — Mô phỏng điều phối xe</b><br>
    🔴 Xe 1 &nbsp; 🔵 Xe 2 &nbsp; 🟢 Xe 3 &nbsp; 🟣 Xe 4<br>
    Nhấn ▶ để xem xe di chuyển theo thời gian
</div>"""
m.get_root().html.add_child(folium.Element(legend))
m.save("bai_23_14.html")
webbrowser.open('file://' + os.path.realpath("bai_23_14.html"))

print("✅ Mở bản đồ → nhấn nút Play ▶ để xem 4 xe di chuyển trên mạng đường theo thời gian")
for v in vehicles:
    print(f"  {v['id']}: {' → '.join(v['route'])}")