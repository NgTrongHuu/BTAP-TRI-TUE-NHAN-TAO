
import numpy as np
import folium
from folium.plugins import HeatMap, MiniMap, Fullscreen
import webbrowser, os

np.random.seed(42)
center = [10.78, 106.70]

m = folium.Map(location=center, zoom_start=13, tiles="CartoDB positron")
folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)

# === LỚP 1: ĐIỂM — Kho hàng ===
fg_warehouses = folium.FeatureGroup(name="🏭 Kho hàng")
wh_list = [
    {"name": "Kho Trung tâm", "lat": 10.775, "lon": 106.700, "cap": 500},
    {"name": "Kho Bắc",       "lat": 10.810, "lon": 106.680, "cap": 300},
    {"name": "Kho Nam",        "lat": 10.740, "lon": 106.720, "cap": 350},
]
for w in wh_list:
    folium.Marker(
        [w["lat"], w["lon"]], tooltip=f"{w['name']} ({w['cap']} đơn/ngày)",
        popup=f"<b>{w['name']}</b><br>Công suất: {w['cap']} đơn/ngày",
        icon=folium.Icon(color="red", icon="home")
    ).add_to(fg_warehouses)
fg_warehouses.add_to(m)

# === LỚP 2: VÙNG — Service area (bán kính phục vụ) ===
fg_zones = folium.FeatureGroup(name="🔵 Vùng phục vụ (3km, 5km)")
for w in wh_list:
    folium.Circle([w["lat"], w["lon"]], radius=3000,
                  color="blue", fill=True, fill_opacity=0.05,
                  tooltip=f"{w['name']} — 3km").add_to(fg_zones)
    folium.Circle([w["lat"], w["lon"]], radius=5000,
                  color="navy", fill=True, fill_opacity=0.03,
                  dash_array="5", tooltip=f"{w['name']} — 5km").add_to(fg_zones)
fg_zones.add_to(m)

# === LỚP 3: ĐIỂM — Khách hàng ===
fg_customers = folium.FeatureGroup(name="👤 Khách hàng (80 điểm)")
customers = np.vstack([
    np.random.normal([10.775, 106.700], 0.008, (30, 2)),
    np.random.normal([10.810, 106.680], 0.006, (25, 2)),
    np.random.normal([10.740, 106.720], 0.006, (25, 2)),
])
for i, c in enumerate(customers):
    folium.CircleMarker(
        c.tolist(), radius=3, color="orange", fill=True, fill_opacity=0.7,
        tooltip=f"Khách {i+1}"
    ).add_to(fg_customers)
fg_customers.add_to(m)

# === LỚP 4: HEATMAP — Mật độ khách hàng ===
fg_heat = folium.FeatureGroup(name="🌡️ Heatmap mật độ khách")
HeatMap(customers.tolist(), radius=18, blur=12).add_to(fg_heat)
fg_heat.add_to(m)

# === LỚP 5: TUYẾN ĐƯỜNG — Giao hàng mẫu ===
fg_routes = folium.FeatureGroup(name="🚚 Tuyến giao hàng")
colors = ["blue", "green", "purple"]
for idx, w in enumerate(wh_list):
    # Lấy 5 khách gần kho nhất
    from geopy.distance import geodesic
    dists = [(geodesic((w["lat"], w["lon"]), (c[0], c[1])).km, i) for i, c in enumerate(customers)]
    dists.sort()
    nearest_5 = [customers[i] for _, i in dists[:5]]
    route = [[w["lat"], w["lon"]]] + [c.tolist() for c in nearest_5] + [[w["lat"], w["lon"]]]
    folium.PolyLine(route, color=colors[idx], weight=3, opacity=0.7,
                    tooltip=f"Tuyến từ {w['name']}").add_to(fg_routes)
fg_routes.add_to(m)

# === LỚP 6: VÙNG CẢNH BÁO — Khu vực chưa phục vụ tốt ===
fg_alert = folium.FeatureGroup(name="⚠️ Vùng cần mở rộng")
folium.Circle([10.82, 106.74], radius=2000, color="red",
              fill=True, fill_opacity=0.1,
              tooltip="Vùng chưa có kho — cần mở rộng").add_to(fg_alert)
fg_alert.add_to(m)

# Plugins
MiniMap(toggle_display=True).add_to(m)
Fullscreen().add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

# Tiêu đề
title = """
<div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:9999;
     background:white;padding:10px 20px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);
     font-family:Arial;font-size:13px">
    <b>Dashboard quản trị Logistics TP.HCM</b> — 6 lớp dữ liệu | Bật/tắt bên phải
</div>"""
m.get_root().html.add_child(folium.Element(title))
m.save("bai_23_13.html")
webbrowser.open('file://' + os.path.realpath("bai_23_13.html"))
print("✅ Dashboard gồm: Kho, Vùng phục vụ, Khách hàng, Heatmap, Tuyến giao hàng, Vùng cảnh báo")