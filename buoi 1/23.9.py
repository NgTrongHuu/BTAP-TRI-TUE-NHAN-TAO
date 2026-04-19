from sklearn.cluster import KMeans
import numpy as np, folium

np.random.seed(42)
data = np.vstack([
    np.random.normal([10.78, 106.70], 0.005, (40, 2)),
    np.random.normal([10.75, 106.72], 0.005, (30, 2)),
    np.random.normal([10.82, 106.68], 0.005, (30, 2)),
])


kmeans = KMeans(n_clusters=3, random_state=42).fit(data)
labels = kmeans.labels_
centers = kmeans.cluster_centers_


m = folium.Map(location=[10.78, 106.70], zoom_start=13)
colors = ['red', 'blue', 'green']
for point, label in zip(data, labels):
    folium.CircleMarker(point.tolist(), radius=3,
                        color=colors[label], fill=True).add_to(m)
for i, c in enumerate(centers):
    folium.Marker(c.tolist(), popup=f"ĐỀ XUẤT: Kho {i+1}",
                  icon=folium.Icon(color=colors[i], icon='star')).add_to(m)
m.save("index4.html")