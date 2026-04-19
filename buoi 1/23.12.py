
import numpy as np
import folium
from geopy.distance import geodesic
import webbrowser, os

np.random.seed(42)

# 1. Dữ liệu: 2 kho + 16 điểm giao hàng ở TP.HCM
warehouses = [
    {"name": "Kho Q1",  "lat": 10.7756, "lon": 106.7019},
    {"name": "Kho Q7",  "lat": 10.7340, "lon": 106.7215},
]
delivery_points = []
for i in range(16):
    delivery_points.append({
        "name": f"Đơn {i+1}",
        "lat": 10.74 + np.random.uniform(-0.04, 0.06),
        "lon": 106.67 + np.random.uniform(-0.02, 0.06),
    })

def dist(a, b):
    return geodesic((a["lat"], a["lon"]), (b["lat"], b["lon"])).km

# 2. Gán mỗi điểm cho kho gần nhất
for p in delivery_points:
    dists = [dist(p, w) for w in warehouses]
    p["warehouse"] = int(np.argmin(dists))

# 3. Nearest Neighbor heuristic (tối ưu)
def nearest_neighbor(warehouse, points):
    route = [warehouse]
    remaining = points.copy()
    current = warehouse
    total = 0
    while remaining:
        nearest = min(remaining, key=lambda p: dist(current, p))
        total += dist(current, nearest)
        route.append(nearest)
        remaining.remove(nearest)
        current = nearest
    total += dist(current, warehouse)  # quay về kho
    route.append(warehouse)
    return route, round(total, 2)

# 4. Phương án không tối ưu (theo thứ tự nhận đơn)
def naive_route(warehouse, points):
    route = [warehouse] + points + [warehouse]
    total = sum(dist(route[i], route[i+1]) for i in range(len(route)-1))
    return route, round(total, 2)

# 5. Tính tuyến đường cho mỗi kho
colors = ["blue", "red"]
m = folium.Map(location=[10.76, 106.70], zoom_start=14, tiles="CartoDB positron")

total_opt, total_naive = 0, 0
for w_idx, w in enumerate(warehouses):
    pts = [p for p in delivery_points if p["warehouse"] == w_idx]

    route_opt, dist_opt = nearest_neighbor(w, pts)
    route_naive, dist_naive = naive_route(w, pts)
    saving = ((dist_naive - dist_opt) / dist_naive) * 100

    total_opt += dist_opt
    total_naive += dist_naive

    # Vẽ tuyến tối ưu
    folium.PolyLine(
        [[p["lat"], p["lon"]] for p in route_opt],
        color=colors[w_idx], weight=4, opacity=0.8,
        tooltip=f"{w['name']} — Tối ưu: {dist_opt} km (tiết kiệm {saving:.0f}%)"
    ).add_to(m)

    # Vẽ tuyến naive (mờ hơn)
    folium.PolyLine(
        [[p["lat"], p["lon"]] for p in route_naive],
        color=colors[w_idx], weight=2, opacity=0.3, dash_array="8",
        tooltip=f"{w['name']} — Không tối ưu: {dist_naive} km"
    ).add_to(m)

    # Marker kho
    folium.Marker([w["lat"], w["lon"]], tooltip=w["name"],
                  icon=folium.Icon(color=colors[w_idx], icon="home")).add_to(m)

    # Marker điểm giao
    for i, p in enumerate(pts):
        folium.CircleMarker(
            [p["lat"], p["lon"]], radius=6,
            color=colors[w_idx], fill=True, fill_opacity=0.8,
            tooltip=f"{p['name']} (→ {w['name']})"
        ).add_to(m)

    print(f"{w['name']}: {len(pts)} điểm | Tối ưu: {dist_opt}km | Naive: {dist_naive}km | Tiết kiệm: {saving:.1f}%")

# Chú thích
saving_total = ((total_naive - total_opt) / total_naive) * 100
legend = f"""
<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
     padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:12px">
    <b>Bài 23.12 — Tối ưu tuyến giao hàng</b><br>
    🔵 Kho Q1 &nbsp; 🔴 Kho Q7<br>
    ── Tuyến tối ưu (Nearest Neighbor) &nbsp; - - Tuyến không tối ưu<br>
    <b>Tổng tiết kiệm: {saving_total:.1f}% quãng đường</b>
</div>"""
m.get_root().html.add_child(folium.Element(legend))
m.save("bai_23_12.html")
webbrowser.open('file://' + os.path.realpath("bai_23_12.html"))

print(f"\nTỔNG: Tối ưu {total_opt:.1f}km vs Naive {total_naive:.1f}km → Tiết kiệm {saving_total:.1f}%")