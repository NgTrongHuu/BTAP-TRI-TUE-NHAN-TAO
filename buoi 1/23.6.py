
import osmnx as ox
import networkx as nx
import folium
import webbrowser, os

# 1. Tải mạng đường Quận 1, TP.HCM
print("⏳ Đang tải dữ liệu mạng đường từ OpenStreetMap...")
G = ox.graph_from_place("Quận 1, Hồ Chí Minh, Vietnam", network_type="drive")
print("✅ Tải xong!")

# 2. Thống kê cơ bản
stats = ox.basic_stats(G)
nodes, edges = ox.graph_to_gdfs(G)

print(f"""
{'='*50}
📊 THỐNG KÊ MẠNG GIAO THÔNG — QUẬN 1, TP.HCM
{'='*50}
  Số nút giao (nodes):        {stats['n']}
  Số đoạn đường (edges):      {stats['m']}
  Chiều dài đường TB:         {stats['street_length_avg']:.1f} m
  Tổng chiều dài mạng:        {stats['street_length_total']:.0f} m ({stats['street_length_total']/1000:.1f} km)
  Số nút trên mỗi km đường:   {stats['node_density_km']:.1f}
  Mật độ giao lộ:             {stats['intersection_density_km']:.1f} giao lộ/km²
  Số đường trung bình/nút:    {stats['streets_per_node_avg']:.2f}
""")

# 3. Trực quan hóa bằng OSMnx (lưu ảnh)
fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=5,
                        edge_color="#333", edge_linewidth=0.5,
                        bgcolor="white", show=False, close=True)
fig.savefig("bai_23_6_network.png", dpi=150, bbox_inches="tight")
print("✅ Đã lưu hình: bai_23_6_network.png")

# 4. Trực quan hóa trên Folium (bản đồ tương tác)
m = folium.Map(location=[10.775, 106.700], zoom_start=15, tiles="CartoDB positron")

# Vẽ các đoạn đường
for _, edge in edges.iterrows():
    coords = [(pt[1], pt[0]) for pt in edge.geometry.coords]  # (lat, lon)
    name = edge.get("name", "Không tên")
    if isinstance(name, list):
        name = ", ".join(name)
    length = edge.get("length", 0)
    folium.PolyLine(
        coords, color="#2c3e50", weight=2, opacity=0.7,
        tooltip=f"{name} — {length:.0f}m"
    ).add_to(m)

# Vẽ nút giao chính (degree >= 4 = ngã tư trở lên)
for node_id, data in G.nodes(data=True):
    degree = G.degree(node_id)
    if degree >= 4:
        folium.CircleMarker(
            [data["y"], data["x"]], radius=3,
            color="red", fill=True, fill_opacity=0.7,
            tooltip=f"Nút {node_id} — {degree} nhánh"
        ).add_to(m)

legend = f"""
<div style="position:fixed;bottom:30px;left:30px;z-index:9999;background:white;
     padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);font-size:12px">
    <b>Bài 23.6 — Mạng giao thông Quận 1</b><br>
    Nút giao: {stats['n']} | Đoạn đường: {stats['m']} | Tổng: {stats['street_length_total']/1000:.1f} km<br>
    🔴 = ngã tư trở lên (≥4 nhánh)
</div>"""
m.get_root().html.add_child(folium.Element(legend))
m.save("bai_23_6.html")
webbrowser.open('file://' + os.path.realpath("bai_23_6.html"))

# 5. Vai trò trong hệ thống AI đô thị thông minh
print(f"""
{'='*50}
🏙️ VAI TRÒ CỦA DỮ LIỆU MẠNG GIAO THÔNG TRONG AI ĐÔ THỊ
{'='*50}

1. TÌM ĐƯỜNG TỰ ĐỘNG (Navigation):
   Dữ liệu graph là nền tảng cho Dijkstra, A* → Google Maps, Grab.

2. DỰ ĐOÁN TẮC NGHẼN:
   Mật độ nút giao + lưu lượng → mô hình ML dự báo kẹt xe theo giờ.

3. TỐI ƯU LOGISTICS:
   Giải bài toán VRP (Vehicle Routing) trên graph thực tế, tiết kiệm
   chi phí giao hàng cho doanh nghiệp.

4. QUẢN LÝ XE TỰ LÁI:
   Xe autonomous cần bản đồ graph chính xác để lập kế hoạch di chuyển
   an toàn, tránh va chạm.

5. QUY HOẠCH ĐÔ THỊ:
   Phân tích mật độ mạng, kết nối giữa các khu vực → quyết định mở
   đường mới, cầu vượt, hầm chui.

6. ỨNG PHÓ KHẨN CẤP:
   Tìm đường nhanh nhất cho xe cứu thương, cứu hỏa dựa trên trạng
   thái giao thông real-time.
""")