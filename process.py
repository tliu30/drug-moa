import sys, os
from similarity import *
from cluster import *
# Calculate similarity scores
def similarity_score(ifname, ofname, (num_top, num_bot), method = 'HGD', transpose = True, verbose = True):
    if method == 'HGD':
        similarity.create_hgd_mtx(ifname, ofname, (num_top, num_bot), transpose, verbose) 
    return None

# Calculate cluster
#def compute_clusters(ifname, odir, thresh, focus = None, method = 'GN'):
#    if method == 'GN':
#        g = utils.mtx_to_gt(ifname, thresh) 
#        gn.gn(g, odir)
#    return None
def raw_input_check(s, err, FUN):
    x = raw_input(s)
    while not FUN(x):
        x = raw_input(err)
    return x
        
def cluster_an_expr_mtx():
    ifname = raw_input_check("Path to expression matrix: ",
                             "File does not exist! Path to expression matrix: ",
                             os.path.exists)
    ofname = raw_input_check("Output filename for similarity matrix: ",
                             "Parent directory does not exist! Output filename: ",
                             lambda x: os.path.exists(os.path.split(x)[0]))
    odir   = raw_input_check("Output directory for clusters: ",
                             "Parent directory does not exist! Output filename: ",
                             lambda x: os.path.exists(os.path.split(x)[0]))
    num_top = num_bot = int( raw_input_check(
        "Number of up/down regulated genes to track: ",
        "Please input an integer: ",
        lambda x: x.isdigit()) )
    transpose = "y" == raw_input_check(
        "Are probes in columns [y/n]? ",
        "Please input [y/n] ",
        lambda x: x in ["y", "n"])
    
    create_hgd_mtx(ifname, ofname, (num_top, num_bot), transpose)
    graph = mtx_to_gt(ofname, 0.8)
    gn(graph, odir)

def add_to_db():
    newfname = raw_input_check("New expression data: ",
                               "File does not exist! Path to expression matrix: ",
                               os.path.exists)
    olddb    = raw_input_check("Path to similarity matrix: ",
                               "File does not exist! Path to similarity matrix: ",
                               os.path.exists)
    oldfname = raw_input_check("Corresponding expression data: ",
                               "File does not exist! Path to similarity matrix: ",
                               os.path.exists)
    odir   = raw_input_check("Output directory for clusters: ",
                             "Parent directory does not exist! Output filename: ",
                             lambda x: os.path.exists(os.path.split(x)[0]))
    num_top = num_bot = int( raw_input_check(
        "Number of up/down regulated genes to track: ",
        "Please input an integer: ",
        lambda x: x.isdigit()) )
    transpose = "y" == raw_input_check(
        "Are probes in columns [y/n]? ",
        "Please input [y/n] ",
        lambda x: x in ["y", "n"])

    new_expr_mtx, new_rows, new_cols = read_matrix(newfname, transpose = transpose)
    old_expr_mtx, old_rows, old_cols = read_matrix(oldfname, transpose = transpose)
    old_sim_mtx, _, _                = read_matrix(olddb, transpose = False)

    new_sigs = expr_to_sigs(new_expr_mtx, num_top, num_bot)
    old_sigs = expr_to_sigs(old_expr_mtx, num_top, num_bot)

    total_sim = augment_hgd(new_sigs, old_sigs, new_rows, old_rows, old_sim_mtx)

    write_mtx(olddb, total_sim, old_rows + new_rows, old_rows + new_rows)

    return None

# Main 
if __name__ == '__main__':
    cluster_an_expr_mtx()
    #print """Clusters-by-Tony 07/25/2014
#------------------------------
#Given gene expression data, compute the similarity
#score between probes, then cluster the results!
#
#What would you like to do?
#[1] Compute similarity scores
#[2] Determine clusters
#[3] Both"""
    #action = raw_input('Select [1/2/3] and press enter: ')
    #while action not in ['1','2','3']:
        #action = raw_input('Please select [1/2/3]: ')
#
    #print ''
    #print 'Option - ' + ['Compute similarity scores', 'Determine clusters', 'Both'][int(action) - 1]
    #print '-------------------------------'
#
    #if (action == '1') or (action == '3'):
        #ifile = raw_input('Expression data file path (.csv, .txt, .tsv): ')
        #while not os.path.exists(ifile):
            #ifile = raw_input('Sorry, could not find that file.  Please input a valid file path: ')
        #ofile = raw_input('Output file path: ')
        #if '/' not in ofile:
            #ofile = './' + ofile
        #while not os.path.exists(os.path.dirname(ofile)):
            #ofile = raw_input('Sorry that directory does not exist.  Please input a valid file path: ')
            #if '/' not in ofile: ofile = './' + ofile
        #### Method? ###
        #num = raw_input('Number of top/down regulated to track: ')
        #if not num.isdigit():
            #num = raw_input('Please input a valid integer: ')
        #num_top, num_bot = num, num
#
        #transpose = raw_input('Are probes listed in rows [r] or columns [c]? ')
        #if transpose not in ['r', 'c']:
            #transpose = raw_input('Please answer [r/c]: ')
        #transpose = (transpose == 'c')
#
    #if (action == '2') or (action == '3'):
        #ifile = raw_input('Similarity matrix file path: ')
        #while not os.path.exists(ifile):
            #ifile = raw_input('Please input a valid file path: ')
        #
        #odir = raw_input('Output directory: ')
        #while not os.path.exists(os.path.dirname(odir)):
            #odir = raw_input('Please input a valid output directory: ')
#
        #thresh = raw_input('Threshold value between 0 and 1: ')
        #if not (float(thresh) >= 0 and float(thresh) <= 1):
            #thresh = raw_input('Please input a valid threshold: ')
#
    #if (action == '1') or (action == '3'):
        #similarity_score(ifname, ofname, (num_top, num_bot), transpose = transpose)
#
    #if (action == '2') or (action == '3'):
        #compute_clusters(ifname, odir, thresh)
