#########################################
# utils.py
# ---------
# Series of functions dealing with
# reading/writing/converting files.
#########################################

import csv, random, json
import networkx as nx
import graph_tool as gt
import numpy as np

#############################
# Basic I/O of matrices
#############################

def read_mtx(fname, FUNTYPE = float, transpose = True, rowname = True):
    # Open CSV, read format of CSV, wrap CSV with csv.reader
    f = open(fname)
    dialect = csv.Sniffer().sniff( f.readline() ); f.seek(0)
    reader = csv.reader(f, dialect)

    # Read csv into an array-of-arrays => np.matrix
    colname = reader.next()
    if rowname == True:
        rowname, mtx = [], []
        for row in reader:
            rowname.append(row[0])
            mtx.append( map(FUNTYPE, row[1:]) )
    else:
        rowname = colname
        mtx     = []
        for row in reader:
            mtx.append( map(FUNTYPE, row) )
    mtx = np.matrix(mtx)

    # Transpose matrix if appropriate
    if transpose:
        rowname, colname = colname, rowname
        mtx              = mtx.transpose()

    # Return matrix & labels
    return(mtx, rowname, colname)

def write_mtx(ofname, mtx, rowname = None, colname = None):
    # Open out-CSV & wrap handler with csv.writer
    f = open(ofname, 'w')
    output = csv.writer(f)

    # Write rows
    if colname: 
        output.writerow(colname)
    if rowname:
        for (cmpd, data) in zip(rowname, mtx.tolist()):
            output.writerow( list(cmpd) + data )
    else:
        for data in mtx.tolist():
            output.writerow(data)
    f.close()

    return None

#########################
# Generate matrix
#########################

def rand_mtx(ofname, dim):
    """
    Create a square matrix of dimension 'dim' with random entries
    between 0 and 1.  Writes output to 'ofname'.
    """
    mtx = []
    for i in range(dim):
        mtx.append( [random.random() for j in range(dim)] )
    mtx = np.matrix(mtx)
    write_mtx(ofname, mtx, colname = range(dim))
    return None

############################
# Conversions: mtx => graph
############################

def mtx_to_nx(ifname, cutoff):
    m, hdr, _ = read_mtx(ifname, transpose = False, rowname = False)
    g = nx.Graph()
    for i in range(len(hdr)):
        g.add_node(hdr[i])
        for j in range(i+1, len(hdr)):
            weight = m[i,j]
            if weight < cutoff: continue
            else:
                g.add_edge(hdr[i], hdr[j], weight = m[i,j])
    return g

def mtx_to_gt(ifname, cutoff):
    m, hdr, _ = read_mtx(ifname, transpose = False, rowname = False)
    g = gt.Graph(directed = False)
    weight = g.new_edge_property("float")
    name   = g.new_vertex_property("string")

    for i in range(len(hdr)):
        v = g.add_vertex()
        name[v] = hdr[i]
    for i in range(len(hdr)):
        for j in range(i+1, len(hdr)):
            if m[i,j] < cutoff: continue
            else:
                v, w      = g.vertex(i), g.vertex(j)
                e         = g.add_edge(v,w)
                weight[e] = m[i,j]

    g.edge_properties['weight'] = weight
    g.vertex_properties['name'] = name

    return g

#########################
# Conversions: x => json
#########################

def mtx_to_json(ifname, ofname, cutoff):
    def mknode(name):
        node = {'name': name}
        return node

    def mkedge(v,w,weight):
        edge = {'source':v, 'target':w}
        edge['value'] = weight
        return edge

    m, hdr, _ = read_mtx(ifname, transpose = False, rowname = False)
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

def gt_to_json(graph, ofname):
    def mknode(v, name_dic = graph.vertex_properties['name']):
        node = {'name': name_dic[v]}
        return node

    def mkedge(e, name_dic = graph.vertex_properties['name']):
        v, w = name_dic[e.source()], name_dic[e.target()]
        edge = {'source': v, 'target': w}
        for prop in graph.edge_properties:
            edge[prop] = graph.edge_properties[prop][e] 
        return edge

    nodes = map(mknode, graph.vertices())
    edges = map(mkedge, graph.edges())

    graph = {"nodes": nodes, "links": edges}
    json_fmt = json.dumps(graph)
    open(ofname, 'w').write(json_fmt)
    return None
