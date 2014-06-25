import cProfile
import numpy as np
from mtx import *

from scipy.misc import factorial as fac

################################################
# Utility function
# ------------------------------------
# Utility function for log factorial;
# requires initializing an array of logs,
# so that's why it returns a function
################################################

def mk_log_fac(max_x):
    # If proves slow, consider writing ufunc in C
    a = np.log(np.arange(1, max_x + 1) )
    a = np.concatenate( (np.array([0]), np.add.accumulate(a)) )
    def log_fac(x):
        if   x < 0:  return np.inf # Ought to be -np.inf...but it's a hack
        else:        return a[x]
    return np.vectorize(log_fac)

#####################################################
# Initial Processing
# ------------------
# The following functions take gene expression data
# and create distance matrices.
#
# Currently implemented metric:
#   1) Distance = P(x) under HGD (success = y)
#####################################################

def expr_to_sigs(expr_mtx, num_top, num_bot):
    """
    Takes a matrix of expression data and extracts the
    x most up/down regulated genes.
    ------------------------------------
    expr_mtx:  (n x m) np.matrix of n tests & m probes/genes
    num_top :  num top reg genes to record
    num_bot :  num bot reg genes to record
    """
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

###############
# HGD Score
###############

def compute_hgd_sim(sig_mtx, names, dxn = 1):
    """
    Takes a matrix of signatures and computes the hgd
    score between each pair (x,y).  The score computes
    the probability of x & y sharing m matches using the
    hypergeometric distribution, treating the number of
    samples as |x| and the number of successes as |y|.
    The score is symmetric.
    
    Outputs square distance matrix.
    -----------------------------
    sig_mtx: (n x m) matrix of n tests & m probes/genes 
             where M[i,j] = -1,0,1 means down/not/up regulated
    names  : the name associated with each test
    dxn    : if dxn == 1, match up regulated
             if dxn == -1, match down regulated
    """
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

def compute_log_hgd_sim(sig_mtx, names, dxn = 1):
    """
    Takes a matrix of signatures and computes the hgd
    score between each pair (x,y).  The score computes
    the probability of x & y sharing m matches using the
    hypergeometric distribution, treating the number of
    samples as |x| and the number of successes as |y|.
    The score is symmetric.
    
    Outputs square distance matrix.
    -----------------------------
    sig_mtx: (n x m) matrix of n tests & m probes/genes 
             where M[i,j] = -1,0,1 means down/not/up regulated
    names  : the name associated with each test
    dxn    : if dxn == 1, match up regulated
             if dxn == -1, match down regulated
             else match both up and down reg
    """
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

    log_fac = mk_log_fac(total)
    ### Factorial calculating time!
    ftotal            = log_fac(total)
    fsig_sum_mtx      = np.tile(log_fac(sig_sum), (1, len(names)))
    ftmin_sig_sum_mtx = np.tile(log_fac(tmin_sig_sum), (1, len(names)))
    fmatch            = log_fac(match)
    fssmin_match_row  = log_fac(ssmin_match_row)
    fssmin_match_col  = log_fac(ssmin_match_col)
    ffinal_factor     = log_fac(final_factor)
    
    log_prob = (fsig_sum_mtx + fsig_sum_mtx.transpose() + ftmin_sig_sum_mtx +
                ftmin_sig_sum_mtx.transpose() - ftotal - fmatch - 
                fssmin_match_row - fssmin_match_col - ffinal_factor)
    
    prob = np.exp(log_prob)

    return prob

def compute_log_cdf_hgd_sim_1(sig_mtx, names, dxn = 1):
    """
    Takes a matrix of signatures and computes the hgd
    score between each pair (x,y).  The score computes
    the probability of x & y sharing m matches using the
    hypergeometric distribution, treating the number of
    samples as |x| and the number of successes as |y|.
    The score is symmetric.
    
    Outputs square distance matrix.
    -----------------------------
    sig_mtx: (n x m) matrix of n tests & m probes/genes 
             where M[i,j] = -1,0,1 means down/not/up regulated
    names  : the name associated with each test
    dxn    : if dxn == 1, match up regulated
             if dxn == -1, match down regulated
             else match both up and down reg
    """
    if   dxn ==  1: sig_mtx = (sig_mtx ==  1) * 1
    elif dxn == -1: sig_mtx = (sig_mtx == -1) * 1
    else:           sig_mtx = np.abs(sig_mtx)

    total        = sig_mtx.shape[1]
    sig_sum      = sig_mtx.sum(1)
    tmin_sig_sum = total - sig_sum

    sig_sum_mtx      = np.tile(sig_sum, (1, len(names)))
    tmin_sig_sum_mtx = np.tile(tmin_sig_sum, (1, len(names))) 

    log_fac = mk_log_fac(total)

    ftotal            = log_fac(total)
    fsig_sum_mtx      = np.tile(log_fac(sig_sum), (1, len(names)))
    ftmin_sig_sum_mtx = np.tile(log_fac(tmin_sig_sum), (1, len(names)))

    prob = np.zeros(fsig_sum_mtx.shape)

    ### Now that we've initialized the constants, time
    ### to iterate the stuffs!

    ### First, initialize the match values
    # Method 1
    match           = sig_mtx * sig_mtx.transpose()
    ssmin_match_row = sig_sum_mtx - match
    ssmin_match_col = sig_sum_mtx.transpose() - match
    final_factor = total - sig_sum_mtx - sig_sum_mtx.transpose() + match

    for i in range(np.triu(match, 1).max()+1):
        fmatch            = log_fac(match - i)
        fssmin_match_row  = log_fac(ssmin_match_row + i)
        fssmin_match_col  = log_fac(ssmin_match_col + i)
        ffinal_factor     = log_fac(final_factor - i)
            
        log_prob = (fsig_sum_mtx + fsig_sum_mtx.transpose() + ftmin_sig_sum_mtx +
                    ftmin_sig_sum_mtx.transpose() - ftotal - fmatch - 
                    fssmin_match_row - fssmin_match_col - ffinal_factor)
        
        prob += np.exp(log_prob)

        print i
    return prob

def compute_log_cdf_hgd_sim_2(sig_mtx, names, dxn = 1):
    """
    Takes a matrix of signatures and computes the hgd
    score between each pair (x,y).  The score computes
    the probability of x & y sharing m matches using the
    hypergeometric distribution, treating the number of
    samples as |x| and the number of successes as |y|.
    The score is symmetric.
    
    Outputs square distance matrix.
    -----------------------------
    sig_mtx: (n x m) matrix of n tests & m probes/genes 
             where M[i,j] = -1,0,1 means down/not/up regulated
    names  : the name associated with each test
    dxn    : if dxn == 1, match up regulated
             if dxn == -1, match down regulated
             else match both up and down reg
    """
    if   dxn ==  1: sig_mtx = (sig_mtx ==  1) * 1
    elif dxn == -1: sig_mtx = (sig_mtx == -1) * 1
    else:           sig_mtx = np.abs(sig_mtx)

    total        = sig_mtx.shape[1]
    sig_sum      = sig_mtx.sum(1)
    tmin_sig_sum = total - sig_sum

    sig_sum_mtx      = np.tile(sig_sum, (1, len(names)))
    tmin_sig_sum_mtx = np.tile(tmin_sig_sum, (1, len(names))) 

    log_fac = mk_log_fac(total)

    ftotal            = log_fac(total)
    fsig_sum_mtx      = np.tile(log_fac(sig_sum), (1, len(names)))
    ftmin_sig_sum_mtx = np.tile(log_fac(tmin_sig_sum), (1, len(names)))

    prob = np.zeros(fsig_sum_mtx.shape)

    ### Now that we've initialized the constants, time
    ### to iterate the stuffs!

    # Method 2
    match           = sig_mtx * sig_mtx.transpose()
    ssmin_match_row = sig_sum_mtx - match
    ssmin_match_col = sig_sum_mtx.transpose() - match
    final_factor = total - sig_sum_mtx - sig_sum_mtx.transpose() + match

    fmatch            = log_fac(match)
    fssmin_match_row  = log_fac(ssmin_match_row)
    fssmin_match_col  = log_fac(ssmin_match_col)
    ffinal_factor     = log_fac(final_factor)
    for i in range(np.triu(match, 1).max()+1):
        log_prob = (fsig_sum_mtx + fsig_sum_mtx.transpose() + ftmin_sig_sum_mtx +
                    ftmin_sig_sum_mtx.transpose() - ftotal - fmatch - 
                    fssmin_match_row - fssmin_match_col - ffinal_factor)
        
        prob += np.exp(log_prob)

        fmatch           -= np.log(match - i)
        fssmin_match_row += np.log(ssmin_match_row + i + 1)
        fssmin_match_col += np.log(ssmin_match_col + i + 1)
        ffinal_factor    -= np.log(final_factor - i)

        print i
    return prob


def create_hgd_mtx(ifname, ofname, (num_top, num_bot), transpose = True):
    m, rowname, colname = read_mtx(ifname, transpose = transpose)
    s = expr_to_sigs(m, num_top, num_bot)
#   h = compute_hgd_sim(s, rowname)
    h = compute_log_hgd_sim(s, rowname)
    hdr = ','.join(rowname)
    np.savetxt(ofname, h, delimiter = ',', header = hdr)
    return None

if __name__ == "__main__":
    m, rowname, colname = read_mtx('../exprsDataConnectAll_thin_short.txt', transpose = True)
    rowname = rowname[10:14]
    s = expr_to_sigs(m[10:14,:], 200, 200)
    np.seterr(divide = 'ignore', invalid = 'ignore')
#   m, rowname, colname = read_mtx('./test.mtx', transpose = False) 
#   s = expr_to_sigs(m, 3, 3)
#   cProfile.run('compute_log_cdf_hgd_sim_1(s, rowname)')
#   create_hgd_mtx('../exprsDataConnectAll_thin.txt', '../hgdDataConnectAll_thin.csv', (300,300)) 
#   cProfile.run( 'compute_log_cdf_hgd_sim_1(s, rowname)' )
#   print '---------------------'
#   cProfile.run( 'compute_log_cdf_hgd_sim_2(s, rowname)' )
    h1 = compute_log_cdf_hgd_sim_1(s, rowname)
    h2 = compute_log_cdf_hgd_sim_2(s, rowname)
    print h1
    print h2
