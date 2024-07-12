import igraph as ig

# Define your source and destination nodes
source = "A"
destination = "D"

g = ig.Graph(directed=True)
g.add_vertices(6)
g.vs["label"] = ["A", "B", "C", "D", "E", "F"]  # Assign labels to nodes
g.es['weight'] = []
# build Graph from panda data_frame
# G_airtraffic = ig.Graph.DataFrame(data_frame.loc[:, ['source', 'dest']], use_vids=False)
routs = [(2, "A", "B"), (1, "A", "C"), (5, "B", "D"), (4, "C", "D"), (7, "C", "E"), (3, "D", "F"), (2, "E", "F")]
for rout in routs:
    g.add_edges([[g.vs.find(label=name).index for name in rout[1:]]])
    g.es['weight'] = g.es['weight'][:-1] + [rout[0]]

# Find all simple paths between source and destination
all_paths = g.get_all_simple_paths(g.vs.find(label=source).index, g.vs.find(label=destination).index)
resoults = []
print("All possible routes from source to destination:")
for path in all_paths:
    total_weight = 0
    for i in range(len(path)-1):
        total_weight += g.distances(path[i], path[i+1], weights='weight')[0][0]
    names = [g.vs[e]["label"] for e in path]
    resoults.append({
                    "path": names,
                    "total_weight": total_weight,
                    "num_routs": len(path) - 1
                    })
sort_resoults_by_weight = sorted(resoults, key=lambda d: d['total_weight'])
for resoult in sort_resoults_by_weight:
    print(resoult)
