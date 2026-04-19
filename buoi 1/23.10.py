
import numpy as np
import folium
from folium.plugins import HeatMap
import webbrowser, os

# 1. Dữ liệu giả lập: 12 tuyến đường ở TP.HCM
np.random.seed(42)
roads = [
    {"name": "Nguyễn Huệ",        "lat": 10.7736, "lon": 106.7031, "lanes": 4, "density": 90, "peak": True},
    {"name": "Lê Lợi",            "lat": 10.7725, "lon": 106.6980, "lanes": 4, "density": 85, "peak": True},
    {"name": "Điện Biên Phủ",     "lat": 10.7870, "lon": 106.6960, "lanes": 6, "density": 80, "peak": True},
    {"name": "Cách Mạng Tháng 8", "lat": 10.7860, "lon": 106.6850, "lanes": 6, "density": 75, "peak": True},
    {"name": "Nguyễn Thị Minh Khai","lat":10.7810, "lon": 106.6920, "lanes": 4, "density": 88, "peak": True},
    {"name": "Võ Văn Tần",        "lat": 10.7780, "lon": 106.6880, "lanes": 3, "density": 70, "peak": False},
    {"name": "Nam Kỳ Khởi Nghĩa", "lat": 10.7830, "lon": 106.6930, "lanes": 4, "density": 65, "peak": False},
    {"name": "Pasteur",           "lat": 10.7850, "lon": 106.6970, "lanes": 3, "density": 45, "peak": False},
    {"name": "Hai Bà Trưng",      "lat": 10.7880, "lon": 106.7000, "lanes": 4, "density": 55, "peak": False},
    {"name": "Trần Hưng Đạo",     "lat": 10.7650, "lon": 106.6920, "lanes": 6, "density": 72, "peak": True},
    {"name": "Nguyễn Trãi (Q5)",  "lat": 10.7560, "lon": 106.6700, "lanes": 6, "density": 82, "peak": True},
    {"name": "Lý Thường Kiệt",    "lat": 10.7750, "lon": 106.6600, "lanes": 4, "density": 40, "peak": False},
]

# 2. Hàm Fuzzy Logic tính nguy cơ tắc nghẽn
def fuzzy_congestion(density, is_peak, num_lanes):
    """
    3 biến đầu vào mờ → 1 đầu ra: nguy cơ tắc nghẽn [0, 1]
    - mu_density: mật độ xe (0-100) → càng cao càng rủi ro
    - mu_peak: giờ cao điểm → rủi ro cao hơn
    - mu_lanes: ít làn → rủi ro cao hơn
    """
    mu_density = min(density / 100, 1.0)
    mu_peak = 1.0 if is_peak else 0.3
    mu_lanes = max(0, 1 - num_lanes / 8)

    # Luật mờ (Fuzzy Rules) — Max-Min inference
    r1 = min(mu_density, mu_peak)       # Đông + giờ cao điểm → tắc
    r2 = min(mu_density, mu_lanes)      # Đông + ít làn → tắc
    r3 = min(mu_peak, mu_lanes)         # Cao điểm + ít làn → tắc
    r4 = mu_density * 0.5              # Đông đơn thuần

    risk = max(r1, r2, r3, r4)  # Defuzzification: lấy max
    return round(risk, 3)

# 3. Tính nguy cơ cho từng tuyến
for r in roads:
    r["risk"] = fuzzy_congestion(r["density"], r["peak"], r["lanes"])
    r["level"] = "CAO" if r["risk"] >= 0.7 else ("TRUNG BÌNH" if r["risk"] >= 0.4 else "THẤP")

# 4. Vẽ bản đồ
m = folium.Map(location=[10.775, 106.690], zoom_start=15, tiles="CartoDB positron")

# Heatmap nguy cơ
heat_data = []
for r in roads:
    for _ in range(int(r["risk"] * 30)):
        heat_data.append([r["lat"] + np.random.normal(0, 0.001),
                          r["lon"] + np.random.normal(0, 0.001), r["risk"]])
HeatMap(heat_data, radius=20, blur=15, max_zoom=17).add_to(m)

# Markers từng tuyến
color_map = {"CAO": "red", "TRUNG BÌNH": "orange", "THẤP": "green"}
for r in roads:
    folium.CircleMarker(
        [r["lat"], r["lon"]], radius=10 + r["risk"] * 15,
        color=color_map[r["level"]], fill=True, fill_opacity=0.7,
        tooltip=f"{r['name']}: {r['level']} ({r['risk']:.0%})",
        popup=f"<b>{r['name']}</b><br>Mật độ: {r['density']}%<br>"
              f"Số làn: {r['lanes']}<br>Giờ cao điểm: {'Có' if r['peak'] else 'Không'}<br>"
              f"<b style='color:{color_map[r['level']]}'>Nguy cơ: {r['risk']:.0%} ({r['level']})</b>"
    ).add_to(m)

# 5. Đề xuất tuyến thay thế (nối các điểm rủi ro THẤP)
safe = [r for r in roads if r["level"] == "THẤP"]
if len(safe) >= 2:
    route = [[r["lat"], r["lon"]] for r in safe]
    folium.PolyLine(route, color="green", weight=5, opacity=0.8,
                    dash_array="10", tooltip="TUYẾN THAY THẾ ĐỀ XUẤT").add_to(m)

# Nối các điểm rủi ro CAO để cảnh báo
danger = [r for r in roads if r["level"] == "CAO"]
if len(danger) >= 2:
    route_d = [[r["lat"], r["lon"]] for r in danger]
    folium.PolyLine(route_d, color="red", weight=4, opacity=0.6,
                    dash_array="5", tooltip="⚠️ VÙNG TẮC NGHẼN").add_to(m)

# Chú thích
legend = """
<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
     padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:12px">
    <b>Bài 23.10 — Nguy cơ tắc nghẽn (Fuzzy Logic)</b><br>
    🔴 Cao (≥70%) &nbsp; 🟠 Trung bình (40-70%) &nbsp; 🟢 Thấp (<40%)<br>
    <span style="color:green">- - - Tuyến thay thế đề xuất</span> &nbsp;
    <span style="color:red">- - - Vùng tắc nghẽn</span>
</div>"""
m.get_root().html.add_child(folium.Element(legend))
m.save("bai_23_10.html")
webbrowser.open('file://' + os.path.realpath("bai_23_10.html"))

# 6. In kết quả
print("=== KẾT QUẢ PHÂN TÍCH TẮC NGHẼN ===")
for r in sorted(roads, key=lambda x: -x["risk"]):
    print(f"  {r['name']:25s} | Nguy cơ: {r['risk']:.0%} | {r['level']}")
print(f"\nVùng nguy hiểm: {', '.join(r['name'] for r in danger)}")
print(f"Tuyến thay thế : {' → '.join(r['name'] for r in safe)}")