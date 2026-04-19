import folium
m = folium.Map(location=[10.7828, 106.6958], zoom_start=15)
# Trung tâm UEH
folium.Marker([10.7828, 106.6958],
              popup="<b>UEH Cơ sở A</b>",
              tooltip="UEH",
              icon=folium.Icon(color='green', icon='graduation-cap', prefix='fa')).add_to(m)
fg_hospital = folium.FeatureGroup(name="Bệnh viện")
fg_mall = folium.FeatureGroup(name="Trung tâm TM")
fg_station = folium.FeatureGroup(name="Bến xe/Ga")
# Hospital
folium.Marker([10.7790, 106.6950],
              popup="<b>Bệnh viện Chợ Rẫy</b>",
              tooltip="Chợ Rẫy",
              icon=folium.Icon(color='red', icon='plus', prefix='fa')).add_to(fg_hospital)
folium.Marker([10.7818, 106.7008],
              popup="<b>Nhi Đồng 2</b>",
              tooltip="Nhi Đồng 2",
              icon=folium.Icon(color='red', icon='plus', prefix='fa')).add_to(fg_hospital)
# Mall
folium.Marker([10.7812, 106.6987],
              popup="<b>Diamond Plaza</b>",
              tooltip="Diamond",
              icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')).add_to(fg_mall)
folium.Marker([10.7779, 106.7019],
              popup="<b>Vincom Đồng Khởi</b>",
              tooltip="Vincom",
              icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')).add_to(fg_mall)
# Station
folium.Marker([10.7765, 106.7015],
              popup="<b>Bến xe buýt Hàm Nghi</b>",
              tooltip="BX Hàm Nghi",
              icon=folium.Icon(color='green', icon='bus', prefix='fa')).add_to(fg_station)
fg_hospital.add_to(m)
fg_mall.add_to(m)
fg_station.add_to(m)
folium.LayerControl().add_to(m)
m.save("bai_23_1.html")
