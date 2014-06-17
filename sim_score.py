import os, sys, time, re, csv, pdb
import networkx  as nx
import numpy     as np
import itertools as iter

from scipy.misc import factorial as fac

DEFAULT_NUM_TOP = 300
DEFAULT_NUM_BOT = 300

#####################
# Utility Functions #
#####################

def items(olist):
    [i for sublist in olist for i in sublist]
    list(iter.chain(*olist))

def mean(*nums): # Do i really need this?
    np.vectorize(np.mean)

def match(a, b):
    return list(set(a) & set(b))

def write_mtx(output_fname, mtx, rowname, colname):
    f = open(output_fname, 'w')
    output = csv.writer(f)
    output.writerow(colname)
    for (cmpd, data) in zip(rowname, mtx.tolist()):
        output.writerow( list(cmpd) + data )
    f.close()

    return None

def read_mtx(fname, transpose = True, FUNTYPE = float, rowname = True):
    f = open(fname)
    dialect = csv.Sniffer().sniff( f.readline() ); f.seek(0)
    reader = csv.reader(f, dialect)

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

    if transpose:
        rowname, colname = colname, rowname
        mtx              = mtx.transpose()

    return(mtx, rowname, colname)

################
# Main Library #
################

def gene_sigs(expr_mtx, num_top, num_bot):
    sig_mtx = []
    for row in expr_mtx:
        bot_bd = np.sort(row)[0,num_bot-1]
        top_bd = np.sort(row)[0,-num_top]

        bot    = (row <= bot_bd) * -1.
        top    = (row >= top_bd) *  1.
        sig    = bot + top

        sig_mtx.append(sig.tolist()[0])
    sig_mtx = np.matrix(sig_mtx)
    return sig_mtx

def compute_hgd_sim(sig_mtx, names, dxn = 1):
    if   dxn ==  1: sig_mtx = (sig_mtx ==  1) * 1
    elif dxn == -1: sig_mtx = (sig_mtx == -1) * 1
    else:           sig_mtx = np.abs(sig_mtx)

    total        = sig_mtx.shape[1]
    sig_sum      = sig_mtx.sum(1)
    tmin_sig_sum = total - sig_sum

    sig_sum_mtx      = np.tile(sig_sum, (1, len(names)))
    tmin_sig_sum_mtx = np.tile(tmin_sig_sum, (1, len(names))) 

    match           = sig_mtx * sig_mtx.transpose()
    ssmin_match_row = sig_sum_mtx - match
    ssmin_match_col = sig_sum_mtx.transpose() - match

    final_factor = total - sig_sum_mtx - sig_sum_mtx.transpose() + match

    ### Factorial calculating time!
    ftotal            = fac(total)
    fsig_sum_mtx      = np.tile(fac(sig_sum), (1, len(names)))
    ftmin_sig_sum_mtx = np.tile(fac(tmin_sig_sum), (1, len(names)))
    fmatch            = fac(match)
    fssmin_match_row  = fac(ssmin_match_row)
    fssmin_match_col  = fac(ssmin_match_col)
    ffinal_factor     = fac(final_factor)
    
    prob = np.divide(
        np.multiply(
            np.multiply(fsig_sum_mtx, fsig_sum_mtx.transpose()),
            np.multiply(ftmin_sig_sum_mtx, ftmin_sig_sum_mtx.transpose())
        ), np.multiply(
            np.multiply(ftotal, fmatch),
            np.multiply(fssmin_match_row, fssmin_match_col)
        ) * ffinal_factor
    )
    
    return prob

def create_sim_mtx(infname, ofname, (num_top, num_bot), transpose = True):
    m, rowname, colname = read_mtx(infname, transpose)
    s = gene_sigs(m, num_top, num_bot)
    h = compute_hgd_sim(s, rowname)

    hdr = ','.join(rowname)
    np.savetxt(ofname, h, delimiter = ',', header = hdr)
    return None

if __name__ == "__main__":
    create_sim_mtx('test.mtx', 'testhgd.mtx', (3,3), False)
