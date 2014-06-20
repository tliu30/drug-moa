from sim_score import read_mtx
import networkx as nx
import json

def mtx_to_nx(ifname, cutoff):
    m, hdr, hdr2 = read_mtx(ifname, transpose = False, rowname = False)
    g = nx.Graph()
    for i in range(len(hdr)):
        g.add_node(hdr[i])
        for j in range(i+1, len(hdr)):
            weight = m[i,j]
            if weight < cutoff: continue
            else:
                g.add_edge(hdr[i], hdr[j], weight = m[i,j])
    return g

def mtx_to_json(ifname, ofname, cutoff):
    def mknode(name):
        node = {'name': name}
        return node

    def mkedge(v,w,weight):
        edge = {'source':v, 'target':w}
        edge['value'] = weight
        return edge

    m, hdr, hdr2 = read_mtx(ifname, transpose = False, rowname = False)
    graph = {"nodes": [], "links": []}
    for i in range(len(hdr)):
        node = mknode(hdr[i])
        graph['nodes'].append(node)
        for j in range(i+1, len(hdr)):
            weight = m[i,j]
            if weight < cutoff: continue
            else:
                edge = mkedge(i,j,weight)
                graph['links'].append(edge)
    json_fmt = json.dumps(graph)
    open(ofname, 'w').write(json_fmt)
    return None

def nx_to_json(graph, ofname):
    def mknode(name):
        node = {'name': name}
        return node

    def mkedge((v,w)):
        edge = {'source': v, 'target': w}
        data = graph.get_edge_data(v,w)
        for key in data:
            edge[key] = data[key]
        return edge

    nodes = map(mknode, graph.nodes_iter())
    edges = map(mkedge, graph.edges_iter())

    graph = {"nodes": nodes, "links": edges}

    json_fmt = json.dumps(graph)
    open(ofname, 'w').write(json_fmt)
    return None
if __name__ == '__main__':
    mtx_to_json('testhgd.mtx', './site/js/testhgd.json', 0)
