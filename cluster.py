####################################
# cluster.py - 07/28/2014
# --------------------------------
# Library for exploring clusters
# of data; currently only gn is
# implemented.
####################################

# Import graph_tool library functions
import graph_tool as gt
from graph_tool.centrality import betweenness as gt_bt
from graph_tool.topology   import label_components as gt_cc
from graph_tool.topology   import label_out_component as gt_cc_out
from graph_tool.util       import find_edge

# Some utility functions
from utils import gt_to_json, write_mtx

# Other libraries
import numpy as np
import os

from fake_log import *

#import sklearn.cluster as skcluster

# Girvan-Newman Algorithm
# -----------------------
# Subtractive algorithm; iteratively delete
# edge with highest betweeness_centrality,
# and save each step.
# With graph_tool runs in 3814 seconds (i.e., 63 min) on hgd_thin

def gn(g, odir, focus = None):
    """
    Takes graph and uses Girvan Newman to slowly break graph down.
    Can operate in faster mode that constrains view to single graph.
    Creates new output_directory "odir" in which JSON graphs are placed,
    as well as names of clusters, and index mapping tests to clusters.
    -----------------------------------------
    g:     graph_tool graph
    odir:  output_directory
    focus: if True, only looks at clusters with vertex named "focus"
    """

    total_edges = g.num_edges()
    vprint(INFO, 'Applying Girvan Newman algorithm on %i edges...'%(g.num_edges()))
    if focus: vprint(INFO, 'Focused on %s'%(focus))

    ### Pull some properties of the graph out
    weight = g.ep['weight']
    name   = g.vp['name']

    ### If focus, make sure focus actually there!
    if focus:
        if focus not in name:
            raise KeyboardInterrupt

    ### Initialize output
    vprint(INFO, 'Output: %s'%(os.path.abspath(odir)))
    if not os.path.exists(odir):
        vprint(INFO, '\tDirectory did not exist!  Created.')
        os.mkdir(odir)
    json_name = os.path.join(odir, "%i_%i.json")
    text_name = os.path.join(odir, "%i_%i.txt")
    idx_name  = os.path.join(odir, "index.csv")

    ### Create new property for graph & configure for fast
    g.ep["ebc"] = g.new_edge_property("float") 
    g.set_fast_edge_removal(True)

    ### Initialize variables for tracking connected components
    ### and indexing
    if focus: cc_cts = [g.num_vertices()]
    else:     cc_cts = [0]
    index  = dict( [(name[v], [(0,0)]) for v in g.vertices()] ) 

    ### Begin Girvan Newman algorithm
    _, _    = gt_bt(g, eprop = g.ep["ebc"], weight = weight, norm = False) 
    while g.num_edges() != 0:
        ### Get & remove edge of max() betweenness; recalc betweenness 
        maxedge = find_edge(g, g.ep["ebc"], g.ep["ebc"].a.max())[0]
        g.ep["ebc"] = g.new_edge_property("float")
        g.remove_edge(maxedge)
        _, _    = gt_bt(g, eprop = g.ep["ebc"], weight = weight, norm = False)

        ### If we're in a focused situation, find relevant cc
        if focus:
            cc_lbl = gt_cc_out(g, focus)
            cc_ct  = cc_lbl.a.sum()
            g.set_vertex_filter(cc_lbl) # Mask all other edge/verts

            ### If edge removed creates new clusters
            if cc_ct != cc_cts[-1]: 
                iter_num = len(cc_cts)
                cc_cts.append(cc_ct)

                ### Write sections
                gt_to_json(g, json_name%(iter_num, 0))
                out = open(text_name%(i - iter_num, 0), 'w')
                for v in g.vertices():
                    if cc_lbl[v]:
                        out.write(name[v] + '\n')
                        index[name[v]].append((iter_num, 0))

        ### Otherwise...
        else:
            ### First, gather connected components
            cc_lbl, _ = gt_cc(g, directed = False)
            cc_ct     = cc_lbl.a.max()
            ### If we've generated new clusters...
            if cc_ct != cc_cts[-1]:
                iter_num = len(cc_cts) 
                cc_cts.append(cc_ct)

                ### Create a filter for each cc label 
                filters = dict([(i, g.new_vertex_property("bool")) for i in range(cc_lbl.a.max()+1)])
                for v in g.vertices():
                    lbl = cc_lbl[v]
                    filters[lbl][v] = True

                for (i, f) in filters.iteritems():
                    if f.a.sum() == 1:
                        index[name[v]].append((iter_num,i))
                        continue
                    g.set_vertex_filter(f)
                    gt_to_json(g, json_name%(iter_num, i))
                    out = open(text_name%(iter_num, i), 'w')
                    for v in g.vertices():
                        if f[v]:
                            out.write(name[v] + '\n')
                            index[name[v]].append((iter_num,i))
                    g.set_vertex_filter(None)            

        # Progress bar
        progress_bar(total_edges - g.num_edges(), total_edges, 100)

    ### Final step: break down index into legible file
    progress_bar_complete(total_edges)
    
    vprint(INFO, 'Making index file.')

    m = np.ones( (len(index), len(cc_cts) ) ) * -1
    ordered_keys = sorted(index.keys())
    for (key, i) in zip(ordered_keys, range(len(index))):
        for (iter_num, clust_num) in index[key]:
            m[i, iter_num] = clust_num
    write_mtx(idx_name, m, ordered_keys, range(len(cc_cts))) 

    vprint(INFO, 'Girvan Newman Complete!')

    return None


#def k_means(x, n, **kwargs)
    #"""
    #Scalable, but req's even cluster size, not too many clusts
    #"""
    #centroids, labels, inertia = skcluster.k_means(x, n, **kwargs)
    #return labels

#def affinity_propagation(x, **kwargs):
    #"""
    #NOT scalable, but allows for many clusters & uneven size
    #Uses a nearest neighbor graph.

    #Uses SIMILARITY matrix
    #Consider adding option to set bandwidth
    #"""
    #S = np.ones(x.shape) - x 
    #cluster_center_indices, labels = cluster.affinity_propagation(S, **kwargs)
    #return labels

#def mean_shift(x, **kwargs):
    #"""
    #NOT scalable, many clusters, uneven cluster size
    #Dist between pts.
    #"""
    #clustre_centers, labels = cluster.mean_shift(x, **kwargs)
    #return labels

#def spectral(x, n, **kwargs):
    #"""
    #Medium n_samples, few clusters, even cluster size
    #Graph distance.

    #Requires an AFFINITY matrix
    #"""
    #S = np.ones(x.shape) - x
    #labels = cluster.spectral_clustering(S, n, **kwargs)
    #return labels

#def hierarchical(x, n, **kwargs):
    #"""
    #Scalable, many clusters (but with connectivity constraints)
    #Play with connectivity settings?  (see sklearn docs)
    #"""
    #ward = cluster.Ward(n_clusters = n, **kwargs).fit(x)
    #labels = ward.labels_
    #return labels

#def DBSCAN(x, eps, min_samples, **kwargs):
    #"""
    #Scalable, uneven cluster sizes
    #Distances between NEAREST points
    #"""
    #db = DBSCAN(eps = eps, min_samples = min_samples, **kwargs).fit(x)
    #labels = db.labels_
    #return labels

if __name__ == '__main__':
    from mtx import mtx_to_gt
    g = mtx_to_gt('../hgdDataConnectAll_thin.csv', 0.8)
    import timeit
    print timeit.timeit('from __main__ import g, gn; gn(g, "./exprsDataConnectAll_thin")', number = 1)
