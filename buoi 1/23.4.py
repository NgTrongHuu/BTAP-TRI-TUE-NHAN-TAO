import geopandas as gpd
import folium
import pandas as pd
geo_data = gpd.read_file("vietnam_provinces.geojson")
revenue_data = pd.DataFrame({
    'province': geo_data['name'].tolist(),
    'revenue': np.random.randint(100, 1000, len(geo_data))
})

geo_merged = geo_data.merge(revenue_data, left_on='name', right_on='province')

m = folium.Map(location=[16.0, 106.0], zoom_start=6)
folium.Choropleth(
    geo_data=geo_merged,
    data=revenue_data,
    columns=['province', 'revenue'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    legend_name='Doanh thu (tỷ VNĐ)'
).add_to(m)
m.save("index.html")