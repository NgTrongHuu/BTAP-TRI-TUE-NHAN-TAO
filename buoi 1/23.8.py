from scipy.optimize import linear_sum_assignment
from geopy.distance import geodesic
import numpy as np, folium

np.random.seed(42)
customers = np.random.normal([10.78, 106.70], 0.01, (5, 2))
drivers = np.random.normal([10.78, 106.70], 0.015, (5, 2))

cost = np.array([[geodesic(c, d).km for d in drivers] for c in customers])

row_ind, col_ind = linear_sum_assignment(cost)

m = folium.Map(location=[10.78, 106.70], zoom_start=14)
colors = ['red','blue','green','purple','orange']
for i, j in zip(row_ind, col_ind):
    folium.Marker(customers[i].tolist(), popup=f"Khách {i}",
                  icon=folium.Icon(color=colors[i])).add_to(m)
    folium.Marker(drivers[j].tolist(), popup=f"Xe {j}",
                  icon=folium.Icon(color=colors[i], icon='car',
                                   prefix='fa')).add_to(m)
    folium.PolyLine([customers[i].tolist(), drivers[j].tolist()],
                     color=colors[i]).add_to(m)
m.save("index3.html")