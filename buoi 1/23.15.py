
import numpy as np
import folium
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
from geopy.distance import geodesic
import webbrowser, os

np.random.seed(42)

# ============================================================
# 1. BÀI TOÁN
# ============================================================
# Một doanh nghiệp muốn mở 3 quán cà phê mới tại TP.HCM.
# Cần tìm vị trí tối ưu dựa trên: mật độ dân cư, mức độ cạnh tranh,
# khả năng tiếp cận giao thông. Dùng AI để chấm điểm + gợi ý vị trí.

# ============================================================
# 2. DỮ LIỆU (giả lập)
# ============================================================

# 2a. Mật độ dân cư — 300 điểm dân cư
pop_clusters = [
    (10.780, 106.700, 80),   # Q1 - trung tâm
    (10.800, 106.680, 60),   # Q3
    (10.735, 106.720, 50),   # Q7
    (10.850, 106.760, 40),   # Thủ Đức
    (10.760, 106.670, 35),   # Q5
    (10.810, 106.650, 35),   # Tân Bình
]
population = np.vstack([
    np.random.normal([lat, lon], 0.006, (n, 2)) for lat, lon, n in pop_clusters
])

# 2b. Quán cà phê đối thủ hiện có — 20 quán
competitors = [
    {"name": "Highlands Q1",    "lat": 10.776, "lon": 106.701},
    {"name": "Starbucks Nguyễn Huệ", "lat": 10.774, "lon": 106.703},
    {"name": "Phúc Long Lê Lợi","lat": 10.772, "lon": 106.698},
    {"name": "TCH Pasteur",     "lat": 10.785, "lon": 106.697},
    {"name": "Highlands Q3",    "lat": 10.790, "lon": 106.685},
    {"name": "Starbucks Q3",    "lat": 10.795, "lon": 106.680},
    {"name": "Phúc Long Q7",    "lat": 10.738, "lon": 106.722},
    {"name": "TCH Q7",          "lat": 10.730, "lon": 106.718},
    {"name": "Highlands Q5",    "lat": 10.755, "lon": 106.665},
    {"name": "Phúc Long Q5",    "lat": 10.758, "lon": 106.672},
    {"name": "TCH Thủ Đức",     "lat": 10.848, "lon": 106.758},
    {"name": "Highlands TB",    "lat": 10.808, "lon": 106.652},
    {"name": "Starbucks BT",    "lat": 10.805, "lon": 106.710},
    {"name": "Coffee House NTL","lat": 10.792, "lon": 106.695},
    {"name": "Phúc Long ĐBP",   "lat": 10.787, "lon": 106.692},
    {"name": "Highlands GV",    "lat": 10.838, "lon": 106.665},
    {"name": "Ông Bầu Q10",    "lat": 10.775, "lon": 106.675},
    {"name": "Trung Nguyên Q1", "lat": 10.778, "lon": 106.695},
    {"name": "Cộng Cà Phê",    "lat": 10.780, "lon": 106.705},
    {"name": "Katinat ND Chiểu","lat": 10.793, "lon": 106.700},
]

# 2c. Trạm xe buýt / metro (tiếp cận giao thông)
transit = [
    (10.773, 106.700), (10.780, 106.692), (10.788, 106.697),
    (10.795, 106.685), (10.758, 106.670), (10.735, 106.720),
    (10.848, 106.755), (10.810, 106.650), (10.770, 106.705),
    (10.803, 106.710),
]

# ============================================================
# 3. PHƯƠNG PHÁP AI — Scoring Model
# ============================================================

# Tạo lưới ứng viên (grid) trên toàn TP.HCM
lat_range = np.arange(10.720, 10.860, 0.005)
lon_range = np.arange(10.640, 106.770, 0.005)
# Sửa lại lon_range
lon_range = np.arange(106.640, 106.770, 0.005)

candidates = []
for lat in lat_range:
    for lon in lon_range:
        # Score 1: Mật độ dân cư (đếm số dân trong bán kính 500m)
        pop_count = sum(1 for p in population
                        if geodesic((lat, lon), (p[0], p[1])).m < 500)
        pop_score = min(pop_count / 15, 1.0)  # chuẩn hóa 0-1

        # Score 2: Cạnh tranh (ít đối thủ gần = tốt)
        comp_nearby = sum(1 for c in competitors
                          if geodesic((lat, lon), (c["lat"], c["lon"])).m < 400)
        comp_score = max(0, 1 - comp_nearby / 3)  # 0 đối thủ=1, ≥3=0

        # Score 3: Gần giao thông công cộng
        min_transit = min(geodesic((lat, lon), t).m for t in transit)
        transit_score = max(0, 1 - min_transit / 800)  # <800m = tốt

        # Tổng điểm (trọng số: dân cư 50%, cạnh tranh 30%, giao thông 20%)
        total = pop_score * 0.5 + comp_score * 0.3 + transit_score * 0.2

        if total > 0.2:  # chỉ giữ điểm đáng xem xét
            candidates.append({
                "lat": lat, "lon": lon,
                "pop_score": round(pop_score, 2),
                "comp_score": round(comp_score, 2),
                "transit_score": round(transit_score, 2),
                "total": round(total, 3)
            })

# Sắp xếp theo điểm
candidates.sort(key=lambda x: -x["total"])
print(f"Tổng ứng viên đánh giá: {len(candidates)}")

# ============================================================
# 4. AI — KMeans chọn 3 vị trí tối ưu (phân tán, không chồng nhau)
# ============================================================
top_n = min(30, len(candidates))
top_candidates = candidates[:top_n]
top_coords = np.array([[c["lat"], c["lon"]] for c in top_candidates])

kmeans = KMeans(n_clusters=3, random_state=42).fit(top_coords)
# Chọn ứng viên điểm cao nhất trong mỗi cluster
best_3 = []
for cluster_id in range(3):
    cluster_cands = [c for c, l in zip(top_candidates, kmeans.labels_) if l == cluster_id]
    best = max(cluster_cands, key=lambda x: x["total"])
    best_3.append(best)

# ============================================================
# 5. TRỰC QUAN HÓA TRÊN BẢN ĐỒ
# ============================================================
m = folium.Map(location=[10.785, 106.700], zoom_start=13, tiles="CartoDB positron")

# Lớp 1: Heatmap dân cư
fg_pop = folium.FeatureGroup(name="🌡️ Mật độ dân cư")
HeatMap(population.tolist(), radius=12, blur=8).add_to(fg_pop)
fg_pop.add_to(m)

# Lớp 2: Đối thủ
fg_comp = folium.FeatureGroup(name="☕ Đối thủ hiện có")
for c in competitors:
    folium.CircleMarker(
        [c["lat"], c["lon"]], radius=5, color="gray", fill=True, fill_opacity=0.7,
        tooltip=c["name"]
    ).add_to(fg_comp)
fg_comp.add_to(m)

# Lớp 3: Giao thông
fg_transit = folium.FeatureGroup(name="🚌 Trạm giao thông")
for t in transit:
    folium.CircleMarker(t, radius=4, color="blue", fill=True,
                        fill_opacity=0.5, tooltip="Trạm xe buýt/metro").add_to(fg_transit)
fg_transit.add_to(m)

# Lớp 4: 3 vị trí đề xuất
fg_result = folium.FeatureGroup(name="⭐ VỊ TRÍ ĐỀ XUẤT")
colors = ["red", "green", "purple"]
for i, loc in enumerate(best_3):
    folium.Marker(
        [loc["lat"], loc["lon"]],
        icon=folium.Icon(color=colors[i], icon="star"),
        tooltip=f"ĐỀ XUẤT #{i+1} — Điểm: {loc['total']:.2f}",
        popup=f"<b>Vị trí đề xuất #{i+1}</b><br>"
              f"Dân cư: {loc['pop_score']:.0%}<br>"
              f"Cạnh tranh: {loc['comp_score']:.0%}<br>"
              f"Giao thông: {loc['transit_score']:.0%}<br>"
              f"<b>TỔNG: {loc['total']:.0%}</b>"
    ).add_to(fg_result)
    folium.Circle([loc["lat"], loc["lon"]], radius=500,
                  color=colors[i], fill=True, fill_opacity=0.1).add_to(fg_result)
fg_result.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

legend = """
<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
     padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:12px">
    <b>Bài 23.15 — AI đề xuất vị trí mở quán cà phê</b><br>
    ⭐ Vị trí đề xuất &nbsp; ☕ Đối thủ &nbsp; 🚌 Giao thông &nbsp; 🌡️ Dân cư<br>
    Scoring: Dân cư 50% + Ít cạnh tranh 30% + Giao thông 20%
</div>"""
m.get_root().html.add_child(folium.Element(legend))
m.save("bai_23_15.html")
webbrowser.open('file://' + os.path.realpath("bai_23_15.html"))

# ============================================================
# 6. BÁO CÁO KẾT QUẢ
# ============================================================
print(f"""
{'='*55}
📋 BÁO CÁO: ĐỀ XUẤT VỊ TRÍ MỞ QUÁN CÀ PHÊ TẠI TP.HCM
{'='*55}

1. BÀI TOÁN:
   Tìm 3 vị trí tối ưu mở quán cà phê dựa trên dữ liệu không gian.

2. DỮ LIỆU:
   - 300 điểm dân cư (giả lập theo phân bố thực tế 6 quận)
   - 20 quán cà phê đối thủ (Highlands, Starbucks, Phúc Long...)
   - 10 trạm giao thông công cộng

3. PHƯƠNG PHÁP AI:
   a) Scoring Model: Lưới 728 ứng viên, chấm điểm 3 tiêu chí
      - Mật độ dân cư trong 500m (trọng số 50%)
      - Mức độ cạnh tranh trong 400m (trọng số 30%)
      - Khoảng cách đến giao thông (trọng số 20%)
   b) KMeans (K=3): Phân cụm top 30 ứng viên → chọn tốt nhất
      mỗi cụm → đảm bảo 3 vị trí phân tán, không cannibalize.

4. KẾT QUẢ:""")
for i, loc in enumerate(best_3):
    print(f"   ⭐ Vị trí #{i+1}: ({loc['lat']:.3f}, {loc['lon']:.3f})")
    print(f"      Dân cư={loc['pop_score']:.0%}  Cạnh tranh={loc['comp_score']:.0%}  "
          f"Giao thông={loc['transit_score']:.0%}  TỔNG={loc['total']:.0%}")

print(f"""
5. GIÁ TRỊ ỨNG DỤNG:
   - Giảm rủi ro chọn sai vị trí (nguyên nhân #1 thất bại F&B).
   - Tái sử dụng cho chuỗi bất kỳ: trà sữa, minimart, gym...
   - Mở rộng: tích hợp dữ liệu giá thuê, lưu lượng người đi bộ,
     doanh thu khu vực → mô hình chính xác hơn.
""")