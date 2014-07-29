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

<<<<<<< HEAD
def read_mtx(fname, FUNTYPE = float, transpose = True, rowname = True):
    vprint(INFO, 'Reading in %s as a numpy matrix (tranpose: %r)...'%(fname, transpose))

=======
def read_mtx(fname, FUNTYPE = float, transpose = True, 
             colname= True, rowname = True):
    """
    Read a csv file into a (np.matrix, rownames, colnames) tuple.
    ------------------
    fname     - the name of the input file
    FUNTYPE   - the type caster of the entries of the matrix
    transpose - whether or not to transpose the matrix
    rowname   - whether or not there are rownames 
    ------------------
    Output is a (mtx, rownames, colnames) tuple, where matrix
    is a numpy.matrix, and rownames/colnames are lists of headers.
    """
>>>>>>> 6c64ef6abdc653192932b3cd6e5a2f2cdb025cd8
    # Open CSV, read format of CSV, wrap CSV with csv.reader
    f = open(fname)
    dialect = csv.Sniffer().sniff( f.readline() ); f.seek(0)
    reader = csv.reader(f, dialect)

    # Read csv into an array-of-arrays => np.matrix
    if colname == True: colname = reader.next()
    else:               colname = None
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
<<<<<<< HEAD
    vprint(INFO, "Writing matrix to %s..."%(ofname))
=======
    """
    Writes a numpy matrix to a CSV file with row and col names.
    --------------------
    ofname  - the name of the output file
    mtx     - a numpy.matrix instance 
    rowname - a list of rownames
    colname - a list of column names
    --------------------
    Output is None.
    """
>>>>>>> 6c64ef6abdc653192932b3cd6e5a2f2cdb025cd8
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
    ----------------
    ofname - the name of the output file
    dim    - the dimension; integer
    ----------------
    Output is None
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
<<<<<<< HEAD
    vprint(INFO, "Opening %s as networkx object (thresh at %.2f)..."%(ifname, cutoff))
=======
    """
    Convert distance matrix (csv file) to networkx graph.
    Ignore edges below cutoff.
    ---------------------
    ifname - the input file name
    cutoff - the threshold
    ---------------------
    Output is a networkx.Graph instance with approp edges.
    """
>>>>>>> 6c64ef6abdc653192932b3cd6e5a2f2cdb025cd8
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
<<<<<<< HEAD
    vprint(INFO, "Opening %s as graph tool object (thresh at %.2f)..."%(ifname, cutoff))
=======
    """
    Convert distance matrix (csv file) to graphtools graph.
    Ignore edges below cutoff.
    ---------------------
    ifname - the input file name
    cutoff - the threshold
    ---------------------
    Output is a graphtools.Graph instance with approp edges.
    """
>>>>>>> 6c64ef6abdc653192932b3cd6e5a2f2cdb025cd8
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
    vprint(INFO, "Convert CSV to JSON; in = %s, out = %s"%(ifname, ofname))
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
    vprint(INFO, "Convert graph to JSON at %s"%(ofname))
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
    vprint(INFO, "Convert graph to JSON at %s"%(ofname))
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
