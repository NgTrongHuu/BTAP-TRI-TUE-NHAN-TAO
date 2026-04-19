from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

geolocator = Nominatim(user_agent="ai_homework")

# Danh sách 10 địa chỉ
addresses = [
    "Đại học Kinh tế TP.HCM",
    "Bệnh viện Chợ Rẫy, TP.HCM",
    "Chợ Bến Thành, TP.HCM",
    "Nhà thờ Đức Bà, TP.HCM",
    "Dinh Độc Lập, TP.HCM",
    "Bến xe Miền Đông mới",
    "Sân bay Tân Sơn Nhất",
    "Đại học Bách Khoa TP.HCM",
    "Bưu điện Trung tâm Sài Gòn",
    "Bitexco Financial Tower"
]
center = geolocator.geocode("Đại học Kinh tế TP.HCM")
center_coords = (center.latitude, center.longitude)
results = []
for addr in addresses:
    loc = geolocator.geocode(addr)
    if loc:
        coords = (loc.latitude, loc.longitude)
        dist = geodesic(center_coords, coords).km
        results.append({"address": addr, "lat": loc.latitude,
                       "lon": loc.longitude, "distance_km": dist})
    import time; time.sleep(1)  # Tránh rate limit

# Vẽ trên Folium
m = folium.Map(location=list(center_coords), zoom_start=13)
for r in results:
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"{r['address']}<br>Cách trung tâm: {r['distance_km']:.2f} km"
    ).add_to(m)
    folium.PolyLine(
        [center_coords, (r['lat'], r['lon'])],
        color='blue', weight=1, opacity=0.5
    ).add_to(m)