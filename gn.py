import networkx as nx

def girvan_newman(g):
    
    def get_edges(paths):
        edges = []
        for path in paths:
            edges += zip(path[:-1], path[1:])
            edges += zip(path[1:] , path[:-1])
        return set(edges)

    def count_nodes(paths):
        nodes = {}
        for path in paths:
            for node in path[1:-1]:
                nodes[node] = nodes.get(node, 0) + 1
        return nodes

    def update_sp(shortest_path, sigma_per, ebc, edge):
        to_edit = set()
        for source in shortest_path:
            for target in shortest_path[source]:
                edges = get_edges(shortest_path[source][target])
                if (source, target) in edges: 
                    to_edit.add( (source, target) )

        for (source, target) in to_edit:
            old_paths = shortest_path[source][target]
            new_paths = nx.algorithms.shortest_path(g, source, target)

            old_counts = count_nodes(old_paths)
            new_counts = count_nodes(new_paths)

            for node in old_counts:
                ebc[node] -= sigma_per[node][source][target]

            for node in new_counts:
                sigma_per[node][source][target] = counts[node] / len(new_paths)
                ebc[node] += sigma_per[node][source][target]

            shortest_path[source][target] = new_paths

        return shortest_path, sigma_per, ebc
    
    ccs = nx.algorithms.components.connected_component_subgraphs

    def compare(a,b):
        if len(a) == len(b):
            return True
 
    ### Initialize
    shortest_path  = nx.algorithms.shortest_path(g)
    sigma_per, ebc = {}, {} 
    for u in g.nodes():
        ebc[u] = 0
        sigma_per[u] = {}
        for v in g.nodes():
            sigma_per[u][v]= {}
            for w in g.nodes():
                sigma_per[u][v][w] = 0
    for source in shorest_path:
        for target in shortest_path[source]:
            paths = shortest_path[source][target]
            counts = count_nodes(paths)
            for node in counts:
                sigma_per[node][source][target] = counts[node] / len(paths)
                ebc[node] += sigma_per[node][source][target]
    l = [ccs(g)]

    while len(g.edges()) != 0:
        (v,w) = sorted(ebc.iteritems(),key=lambda x: x[1],reverse=True)[0][0]
        g.remove_edge(v,w)
        z = ccs(g)
        if not compare(z, g[-1]):
            l.append(z)
        shortest_path, sigma_per, ebc = sp_update(shortest_path, sigma_per, ebc, (v,w))

def girvan_newman_2(g):
    def compare(a,b):
        if len(a) == len(b):
            return True
    ccs = nx.algorithms.components.connected_component_subgraphs

    l = [ccs(g)]
    while len(g.edges()) != 0:
        ebc = nx.centrality.edge_betweenness_centrality(g)
        (v,w) = sorted(ebc.iteritems(),key=lambda x: x[1],reverse=True)[0][0]
        g.remove_edge(v,w)
        z = ccs(g)
        if not compare(z, g[-1]):
            l.append(z)
        print len(g.edges())
    return l

if __name__ == "__main__":
    from viz import mtx_to_nx
    g = mtx_to_nx('randhgd.mtx', 0.5)
    steps = girvan_newman(g)
    for s in steps:
        print ' '.join( [len(r.nodes()) for r in s] )
    
