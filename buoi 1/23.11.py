

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import folium
from folium.plugins import HeatMap
import webbrowser
import os

# ==============================================================
# 1. TẠO DỮ LIỆU GIẢ LẬP
# ==============================================================
np.random.seed(42)

# Định nghĩa 8 khu vực ở TP.HCM
regions = {
    0: {"name": "Quận 1",     "lat": 10.7756, "lon": 106.7019, "base_demand": 50},
    1: {"name": "Quận 3",     "lat": 10.7834, "lon": 106.6868, "base_demand": 40},
    2: {"name": "Quận 7",     "lat": 10.7340, "lon": 106.7215, "base_demand": 35},
    3: {"name": "Bình Thạnh", "lat": 10.8056, "lon": 106.7094, "base_demand": 38},
    4: {"name": "Thủ Đức",    "lat": 10.8494, "lon": 106.7537, "base_demand": 30},
    5: {"name": "Tân Bình",   "lat": 10.8018, "lon": 106.6528, "base_demand": 33},
    6: {"name": "Gò Vấp",     "lat": 10.8386, "lon": 106.6652, "base_demand": 28},
    7: {"name": "Phú Nhuận",  "lat": 10.7990, "lon": 106.6802, "base_demand": 32},
}

data_rows = []

for day in range(1, 31):          # 30 ngày
    day_of_week = day % 7         # 0-6 (0=CN, 6=T7)
    is_weekend = 1 if day_of_week in [0, 6] else 0

    for hour in range(6, 24):     # 6h sáng đến 23h
        for region_id, info in regions.items():

            # Mô phỏng nhu cầu thực tế
            base = info["base_demand"]

            # Hiệu ứng giờ cao điểm (7-9h sáng, 17-19h chiều)
            if hour in [7, 8, 9]:
                hour_factor = 1.8
            elif hour in [17, 18, 19]:
                hour_factor = 2.0
            elif hour in [11, 12, 13]:
                hour_factor = 1.3
            elif hour >= 22:
                hour_factor = 0.5
            else:
                hour_factor = 1.0

            # Cuối tuần: nhu cầu giải trí tăng ở Q1, Q7
            if is_weekend:
                if region_id in [0, 2]:
                    weekend_factor = 1.4
                else:
                    weekend_factor = 0.85
            else:
                weekend_factor = 1.0

            # Tính nhu cầu + nhiễu ngẫu nhiên
            demand = base * hour_factor * weekend_factor
            demand += np.random.normal(0, demand * 0.15)  # nhiễu 15%
            demand = max(0, int(round(demand)))

            data_rows.append({
                "day": day,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "hour": hour,
                "region_id": region_id,
                "region_name": info["name"],
                "lat": info["lat"],
                "lon": info["lon"],
                "demand": demand
            })

df = pd.DataFrame(data_rows)
print(f"Tổng số mẫu dữ liệu: {len(df)}")
print(f"\nThống kê nhu cầu:")
print(df.groupby("region_name")["demand"].describe().round(1))

# ==============================================================
# 2. HUẤN LUYỆN MÔ HÌNH RANDOM FOREST
# ==============================================================
# Features: khu vực, giờ, ngày trong tuần, cuối tuần
features = ["region_id", "hour", "day_of_week", "is_weekend"]
target = "demand"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Huấn luyện Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Đánh giá
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"KẾT QUẢ MÔ HÌNH RANDOM FOREST")
print(f"{'='*50}")
print(f"MAE (Sai số trung bình):  {mae:.2f} lượt")
print(f"R² Score:                  {r2:.4f}")

# Độ quan trọng của features
importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)
print(f"\nĐộ quan trọng các đặc trưng:")
for feat, imp in importance.items():
    print(f"  {feat:15s}: {imp:.4f} ({imp*100:.1f}%)")

# ==============================================================
# 3. DỰ ĐOÁN VÀ TRỰC QUAN HÓA TRÊN BẢN ĐỒ
# ==============================================================

# --- BẢN ĐỒ 1: Dự đoán nhu cầu giờ cao điểm chiều (18h, ngày thường) ---
m1 = folium.Map(location=[10.79, 106.70], zoom_start=13,
                tiles='CartoDB positron')

folium.TileLayer('OpenStreetMap').add_to(m1)

# Dự đoán cho từng khu vực lúc 18h ngày thường
pred_data_weekday = []
for region_id, info in regions.items():
    pred_input = pd.DataFrame([{
        "region_id": region_id,
        "hour": 18,
        "day_of_week": 3,     # Thứ 4
        "is_weekend": 0
    }])
    predicted = model.predict(pred_input)[0]
    pred_data_weekday.append({
        "name": info["name"],
        "lat": info["lat"],
        "lon": info["lon"],
        "demand": predicted
    })

# Tìm min/max để scale màu
demands = [d["demand"] for d in pred_data_weekday]
max_demand = max(demands)
min_demand = min(demands)

# Vẽ CircleMarker với kích thước và màu theo nhu cầu
for d in pred_data_weekday:
    # Scale bán kính từ 15 đến 40
    ratio = (d["demand"] - min_demand) / (max_demand - min_demand + 1e-9)
    radius = 15 + ratio * 25

    # Màu: xanh (thấp) → vàng → đỏ (cao)
    if ratio < 0.33:
        color = "green"
    elif ratio < 0.66:
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=[d["lat"], d["lon"]],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=folium.Popup(
            f"<b>{d['name']}</b><br>"
            f"Nhu cầu dự đoán (18h, ngày thường):<br>"
            f"<b style='font-size:16px; color:{color}'>{d['demand']:.0f} lượt</b>",
            max_width=250
        ),
        tooltip=f"{d['name']}: {d['demand']:.0f} lượt"
    ).add_to(m1)

# Tiêu đề bản đồ
title_html = """
<div style="position:fixed; top:10px; left:50%; transform:translateX(-50%);
     z-index:9999; background:white; padding:10px 20px; border-radius:8px;
     box-shadow:0 2px 6px rgba(0,0,0,0.3); font-family:Arial">
    <h3 style="margin:0; color:#333">Dự đoán nhu cầu gọi xe — 18h Ngày thường</h3>
    <p style="margin:4px 0 0; color:#666; font-size:12px">
        🟢 Thấp &nbsp; 🟠 Trung bình &nbsp; 🔴 Cao
        &nbsp;|&nbsp; Kích thước vòng tròn ~ mức nhu cầu
    </p>
</div>
"""
m1.get_root().html.add_child(folium.Element(title_html))

m1.save("bai_23_11_map1_weekday.html")
print("\n✅ Đã lưu bản đồ 1: bai_23_11_map1_weekday.html")

# --- BẢN ĐỒ 2: So sánh ngày thường vs cuối tuần (Heatmap) ---
m2 = folium.Map(location=[10.79, 106.70], zoom_start=13,
                tiles='CartoDB positron')

# Tạo 2 FeatureGroup: ngày thường vs cuối tuần
fg_weekday = folium.FeatureGroup(name="🟦 Ngày thường (18h)")
fg_weekend = folium.FeatureGroup(name="🟥 Cuối tuần (18h)")

for region_id, info in regions.items():
    # Dự đoán ngày thường
    pred_wd = model.predict(pd.DataFrame([{
        "region_id": region_id, "hour": 18,
        "day_of_week": 3, "is_weekend": 0
    }]))[0]

    # Dự đoán cuối tuần
    pred_we = model.predict(pd.DataFrame([{
        "region_id": region_id, "hour": 18,
        "day_of_week": 6, "is_weekend": 1
    }]))[0]

    # Chênh lệch
    diff = pred_we - pred_wd
    diff_pct = (diff / pred_wd) * 100 if pred_wd > 0 else 0
    arrow = "↑" if diff > 0 else "↓"

    # Marker ngày thường
    folium.CircleMarker(
        [info["lat"] - 0.002, info["lon"] - 0.002],
        radius=max(8, pred_wd / 4),
        color="blue", fill=True, fill_opacity=0.5,
        popup=f"<b>{info['name']}</b><br>Ngày thường: {pred_wd:.0f} lượt"
    ).add_to(fg_weekday)

    # Marker cuối tuần
    folium.CircleMarker(
        [info["lat"] + 0.002, info["lon"] + 0.002],
        radius=max(8, pred_we / 4),
        color="red", fill=True, fill_opacity=0.5,
        popup=f"<b>{info['name']}</b><br>Cuối tuần: {pred_we:.0f} lượt"
    ).add_to(fg_weekend)

    # Label chênh lệch
    folium.Marker(
        [info["lat"], info["lon"]],
        icon=folium.DivIcon(html=f"""
            <div style="font-size:11px; font-weight:bold; color:#333;
                 background:white; padding:2px 6px; border-radius:4px;
                 border:1px solid #ccc; white-space:nowrap">
                {info['name']}<br>
                <span style="color:{'green' if diff > 0 else 'red'}">
                    {arrow} {abs(diff_pct):.0f}%
                </span>
            </div>
        """)
    ).add_to(m2)

fg_weekday.add_to(m2)
fg_weekend.add_to(m2)
folium.LayerControl().add_to(m2)

title2 = """
<div style="position:fixed; top:10px; left:50%; transform:translateX(-50%);
     z-index:9999; background:white; padding:10px 20px; border-radius:8px;
     box-shadow:0 2px 6px rgba(0,0,0,0.3); font-family:Arial">
    <h3 style="margin:0; color:#333">So sánh nhu cầu: Ngày thường vs Cuối tuần</h3>
    <p style="margin:4px 0 0; color:#666; font-size:12px">
        🟦 Ngày thường &nbsp; 🟥 Cuối tuần &nbsp;|&nbsp;
        % = mức thay đổi cuối tuần so với ngày thường
    </p>
</div>
"""
m2.get_root().html.add_child(folium.Element(title2))
m2.save("bai_23_11_map2_compare.html")
print("✅ Đã lưu bản đồ 2: bai_23_11_map2_compare.html")

# --- BẢN ĐỒ 3: Heatmap nhu cầu theo các khung giờ ---
m3 = folium.Map(location=[10.79, 106.70], zoom_start=13,
                tiles='CartoDB positron')

time_slots = {
    "Sáng sớm (7h)": 7,
    "Trưa (12h)": 12,
    "Chiều cao điểm (18h)": 18,
    "Tối khuya (22h)": 22
}

for slot_name, hour in time_slots.items():
    fg = folium.FeatureGroup(name=slot_name)
    heat_data = []

    for region_id, info in regions.items():
        pred = model.predict(pd.DataFrame([{
            "region_id": region_id, "hour": hour,
            "day_of_week": 3, "is_weekend": 0
        }]))[0]

        # Tạo nhiều điểm xung quanh trung tâm khu vực để tạo heatmap đẹp
        for _ in range(int(pred)):
            lat = info["lat"] + np.random.normal(0, 0.004)
            lon = info["lon"] + np.random.normal(0, 0.004)
            heat_data.append([lat, lon, 1])

    HeatMap(heat_data, radius=15, blur=10, max_zoom=15).add_to(fg)
    fg.add_to(m3)

folium.LayerControl(collapsed=False).add_to(m3)

title3 = """
<div style="position:fixed; top:10px; left:50%; transform:translateX(-50%);
     z-index:9999; background:white; padding:10px 20px; border-radius:8px;
     box-shadow:0 2px 6px rgba(0,0,0,0.3); font-family:Arial">
    <h3 style="margin:0">Heatmap nhu cầu gọi xe theo khung giờ</h3>
    <p style="margin:4px 0 0; color:#666; font-size:12px">
        Bật/tắt từng khung giờ ở bảng điều khiển bên phải
    </p>
</div>
"""
m3.get_root().html.add_child(folium.Element(title3))
m3.save("bai_23_11_map3_heatmap.html")
print("✅ Đã lưu bản đồ 3: bai_23_11_map3_heatmap.html")

# ==============================================================
# 4. PHÂN TÍCH VÀ NHẬN XÉT
# ==============================================================
print(f"""
{'='*60}
📊 PHÂN TÍCH SỰ KHÁC BIỆT NHU CẦU GIỮA CÁC KHU VỰC
{'='*60}

1. KHU VỰC NHU CẦU CAO:
   - Quận 1: Trung tâm thương mại, văn phòng → nhu cầu cao cả ngày
   - Quận 3: Khu vực dân cư + thương mại mật độ cao
   → Cần bố trí NHIỀU tài xế nhất ở 2 khu vực này

2. SỰ KHÁC BIỆT NGÀY THƯỜNG vs CUỐI TUẦN:
   - Quận 1, Quận 7: Nhu cầu TĂNG cuối tuần (giải trí, mua sắm)
   - Thủ Đức, Gò Vấp: Nhu cầu GIẢM cuối tuần (ít đi làm)
   → Cần điều chuyển tài xế từ ngoại thành vào trung tâm cuối tuần

3. KHUNG GIỜ CAO ĐIỂM:
   - 7h-9h sáng: Nhu cầu cao ở khu dân cư (đi làm)
   - 17h-19h chiều: Nhu cầu cao nhất trong ngày (tan làm + giải trí)
   - 22h+: Nhu cầu giảm mạnh → có thể giảm số xe hoạt động

4. Ý NGHĨA TRONG ĐIỀU PHỐI NGUỒN LỰC:
   - Dùng mô hình dự đoán để phân bổ tài xế TRƯỚC giờ cao điểm
   - Áp dụng giá surge (giá động) ở khu vực nhu cầu > cung
   - Khuyến khích tài xế di chuyển đến vùng sắp có nhu cầu cao
   - Tiết kiệm chi phí bằng cách giảm xe ở giờ/vùng nhu cầu thấp
""")

# Mở bản đồ chính trong trình duyệt
webbrowser.open('file://' + os.path.realpath("bai_23_11_map1_weekday.html"))