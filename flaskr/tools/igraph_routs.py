import igraph as ig

g = ig.Graph(directed=True)
g.add_vertices(6)
g.vs["label"] = ["A", "B", "C", "D", "E", "F"]  # Assign labels to nodes
routs = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
for rout in routs:
    g.add_edges([tuple([g.vs.find(label=name).index for name in rout])])

g.es["weight"] = [2, 1, 5, 4, 7, 3, 2]  # Assign weights to edges
# Define your source and destination nodes
source = "A"
destination = "F"

# Find all simple paths between source and destination
all_paths = g.get_all_simple_paths(g.vs.find(label=source).index, g.vs.find(label=destination).index)

resoults = []
print("All possible routes from source to destination:")
for path in all_paths:
    total_weight = sum(g.es[e]["weight"] for e in path)
    names = [g.vs[e]["label"] for e in path]
    resoults.append({
                    "path": names,
                    "total_weight": total_weight,
                    "num_routs": len(path)
                    })
sort_resoults_by_weight = sorted(resoults, key=lambda d: d['total_weight'])
for resoult in sort_resoults_by_weight:
    print(resoult)
