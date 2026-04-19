import osmnx as ox
import networkx as nx
import time

G = ox.graph_from_place("Quận 1, Hồ Chí Minh, Vietnam",
                         network_type='drive')

orig = ox.nearest_nodes(G, 106.695, 10.780)  # X=lon, Y=lat
dest = ox.nearest_nodes(G, 106.705, 10.770)

t1 = time.time()
route_dij = nx.shortest_path(G, orig, dest, weight='length',
                              method='dijkstra')
t_dij = time.time() - t1
def heuristic(u, v):
    from geopy.distance import geodesic
    u_data = G.nodes[u]
    v_data = G.nodes[v]
    return geodesic((u_data['y'], u_data['x']),
                    (v_data['y'], v_data['x'])).m
t2 = time.time()
route_astar = nx.astar_path(G, orig, dest, heuristic=heuristic,
                             weight='length')
t_astar = time.time() - t2

print(f"Dijkstra: {len(route_dij)} nodes, {t_dij:.4f}s")
print(f"A*:       {len(route_astar)} nodes, {t_astar:.4f}s")

fig, ax = ox.plot_graph_routes(G, [route_dij, route_astar],
                                route_colors=['blue', 'red'])