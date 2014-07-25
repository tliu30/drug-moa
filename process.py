#import gn, similarity, utils
import sys, os

# Calculate similarity scores
#def similarity_score(ifname, ofname, (num_top, num_bot), method = 'HGD', transpose = True, verbose = True):
#    if method == 'HGD':
#        similarity.create_hgd_mtx(ifname, ofname, (num_top, num_bot), transpose, verbose) 
#    return None


# Calculate cluster
#def compute_clusters(ifname, odir, thresh, focus = None, method = 'GN'):
#    if method == 'GN':
#        g = utils.mtx_to_gt(ifname, thresh) 
#        gn.gn(g, odir)
#    return None

# Main 
if __name__ == '__main__':
    print """Clusters-by-Tony 07/25/2014
------------------------------
Given gene expression data, compute the similarity
score between probes, then cluster the results!

What would you like to do?
[1] Compute similarity scores
[2] Determine clusters
[3] Both"""
    action = raw_input('Select [1/2/3] and press enter: ')
    while action not in ['1','2','3']:
        action = raw_input('Please select [1/2/3]: ')

    print ''
    print 'Option - ' + ['Compute similarity scores', 'Determine clusters', 'Both'][int(action) - 1]
    print '-------------------------------'

    if (action == '1') or (action == '3'):
        ifile = raw_input('Expression data file path (.csv, .txt, .tsv): ')
        while not os.path.exists(ifile):
            ifile = raw_input('Sorry, could not find that file.  Please input a valid file path: ')
        ofile = raw_input('Output file path: ')
        if '/' not in ofile:
            ofile = './' + ofile
        while not os.path.exists(os.path.dirname(ofile)):
            ofile = raw_input('Sorry that directory does not exist.  Please input a valid file path: ')
            if '/' not in ofile: ofile = './' + ofile
        ### Method? ###
        num = raw_input('Number of top/down regulated to track: ')
        if not num.isdigit():
            num = raw_input('Please input a valid integer: ')
        num_top, num_bot = num, num

        transpose = raw_input('Are probes listed in rows [r] or columns [c]? ')
        if transpose not in ['r', 'c']:
            transpose = raw_input('Please answer [r/c]: ')
        transpose = (transpose == 'c')

    if (action == '2') or (action == '3'):
        ifile = raw_input('Similarity matrix file path: ')
        while not os.path.exists(ifile):
            ifile = raw_input('Please input a valid file path: ')
        
        odir = raw_input('Output directory: ')
        while not os.path.exists(os.path.dirname(odir)):
            odir = raw_input('Please input a valid output directory: ')

        thresh = raw_input('Threshold value between 0 and 1: ')
        if not (float(thresh) >= 0 and float(thresh) <= 1):
            thresh = raw_input('Please input a valid threshold: ')

    if (action == '1') or (action == '3'):
        similarity_score(ifname, ofname, (num_top, num_bot), transpose = transpose)

    if (action == '2') or (action == '3'):
        compute_clusters(ifname, odir, thresh)
