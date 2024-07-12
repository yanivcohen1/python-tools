import igraph as ig
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

g = ig.Graph(directed=True)
g.add_vertices(6)
g.vs["label"] = ["A", "B", "C", "D", "E", "F"]

# Define your source and destination nodes
source = "A"
destination = "D"

df = pd.DataFrame({
    'source': ['A', 'A', 'A', 'A', 'C'],
    'target': ['B', 'C', 'D', 'E', 'D'],
    'weight': [ 1 ,  2 ,  8 ,  4 ,  5 ]
})

# Generate the graph
g = g.TupleList(df.itertuples(index=False),
                        directed=True,
                        edge_attrs='weight',
                        vertex_name_attr='label')  # Remove 'weights=True'

# Choose a layout algorithm (e.g., Kamada-Kawai)
g.layout("kamada_kawai")

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# Plot the graph with edge weights displayed
width = g.es["weight"]
width_norm = np.array(width) / max(width)
ig.plot(g, target= ax, edge_label= g.es["weight"], edge_width= width_norm*2)
ax.set_title(f"igraph auto from panda")

# Find all simple paths between source and destination
all_paths = g.get_all_simple_paths(g.vs.find(label=source).index, g.vs.find(label=destination).index)
resoults = []
print("All possible routes from source to destination sort by weights:")
for path in all_paths:
    total_weight = 0
    for i in range(len(path)-1):
        total_weight += g.es[g.get_eid(path[i], path[i+1])]['weight']
    names = [g.vs[e]["label"] for e in path]
    resoults.append({
                    "path": names,
                    "total_weight": total_weight,
                    "num_routs": len(path) - 1
                    })
sort_resoults_by_weight = sorted(resoults, key=lambda d: d['total_weight'])
for resoult in sort_resoults_by_weight:
    print(resoult)

plt.show()
