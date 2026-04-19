import folium
m = folium.Map(location=[10.7769, 106.7009], zoom_start=15,
               tiles='OpenStreetMap')
fg_hospital = folium.FeatureGroup(name="Bệnh viện")
fg_mall = folium.FeatureGroup(name="Trung tâm TM")
fg_station = folium.FeatureGroup(name="Bến xe/Ga")
folium.Marker(
    location=[10.7790, 106.6950],
    popup="<b>Bệnh viện Chợ Rẫy</b><br>Bệnh viện hạng đặc",
    tooltip="BV Chợ Rẫy",
    icon=folium.Icon(color='red', icon='plus-sign')
).add_to(fg_hospital)
fg_hospital.add_to(m)
fg_mall.add_to(m)
fg_station.add_to(m)
folium.LayerControl().add_to(m)
m.save("bai_23_1.html")