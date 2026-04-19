import folium
warehouse = [10.7769, 106.7009]
m = folium.Map(location=warehouse, zoom_start=13)

folium.Marker(warehouse, popup="Kho trung tâm",
              icon=folium.Icon(color='red', icon='home')).add_to(m)
for radius, color in [(3000, 'green'), (5000, 'orange'), (10000, 'red')]:
    folium.Circle(
        location=warehouse, radius=radius,
        color=color, fill=True, fill_opacity=0.1,
        popup=f"Bán kính {radius//1000} km"
    ).add_to(m)
