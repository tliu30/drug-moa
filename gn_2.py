import graph_tool as gt
import os
from graph_tool.centrality import betweenness as gt_bt
from graph_tool.topology   import label_components as gt_cc
from graph_tool.topology   import label_out_component as gt_cc_out
from viz import gt_to_json
from mtx import write_mtx
import numpy as np
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
    ### Pull some properties of the graph out
    weight = g.ep['weight']
    name   = g.vp['name']

    ### If focus, make sure focus actually there!
    if focus:
        if focus not in name:
            raise KeyboardInterrupt

    ### Initialize output
    if not os.path.exists(odir):
        os.mkdir(odir)
    json_name = os.path.join(odir, "%i_%i.json")
    text_name = os.path.join(odir, "%i_%i.txt")
    idx_name  = os.path.join(odir, "index.mtx")

    ### Create new property for graph & configure for fast
    g.ep["ebc"] = g.new_edge_property("float") 
    g.set_fast_edge_removal(True)

    ### Initialize variables for tracking connected components
    ### and indexing
    cc_lbls = []
    index   = {}

    ### Begin Girvan Newman algorithm
    _, _    = gt_bt(g, eprop = g.ep["ebc"], weight = weight, norm = False) 
    while g.edges():
        ### Get & remove edge of max betweenness; recalc betweenness 
        maxedge = max(g.edges(), key = lambda e: g.ep["ebc"][e])
        g.remove_edge(maxedge)
        _, _    = gt_bt(g, eprop = g.ep["ebc"], weight = weight, norm = False)
    
        ### If we're in a focused situation, find relevant cc
        if focus:
            cc_lbl = gt_cc_out(g, focus)
            g.set_vertex_filter(cc_lbl) # Mask all other edge/verts

            ### If edge removed creates new clusters
            if cc_lbl.a.sum() != cc_lbls[-1].sum():
                cc_lbls.append( cc_lbl.a )

                ### Write sections
                iter_num = len(cc_lbls)
                gt_to_json(json_name%(iter_num, 0), g)
                out = open(text_name%(iter_num, 0), 'w')
                for v in g.vertices():
                    if cc_lbl[v]:
                        out.write(name[v] + '\n')
                        index[name[v]].append((iter_num, 0))

        ### Otherwise...
        else:
            ### First, gather connected components
            cc_lbl, _ = gt_cc(g, directed = False)

            ### If we've generated new clusters...
            if cc_lbl.a.max != cc_lbls[-1].max:
                cc_lbls.append(cc_lbl.a)

                ### Create a filter for each cc label 
                filters = dict([(i, g.new_vertex_property("bool")) for i in range(cc_lbl.a.max)])
                for v in g.vertices():
                    lbl = cc_lbl[v]
                    filters[lbl][v] = True

                iter_num = len(cc_lbls)
                for (i, f) in filters.items_iter():
                    g.set_vertex_filter(f)
                    gt_to_json(json_name%(iter_num, i), g)
                    out = open(text_name%(iter_num, i), 'w')
                    for v in g.vertices():
                        if f[v]:
                            out.write(name[v] + '\n')
                            index[name[v]].append((iter_num,i))
                    g.set_filter(None)            

    ### Final step: break down index into legible file
    m = np.ones( (len(index), len(cc_lbls) ) * -1
    for (key, i) in zip(index, range(len(index))):
        for (iter_num, clust_num) in index[key]:
            m[i, iter_num] = clust_num
    write_mtx(idx_name, m, index, range(len(cc_lbls))) 
            
    return None
