import numpy as np
from utils import *
from fake_log import *

from scipy.misc import factorial as fac

################################################
# Utility function
# ------------------------------------
# Utility function for log factorial;
# requires initializing an array of logs,
# so that's why it returns a function
################################################

def mk_log_fac(max_x):
    """
    Creates lookup table for log-factorial of all integers
    less than or equal to max_x.
    --------------
    max_x - positive integer
    --------------
    Output is function f([x1,x2,...]) = [log(x1!), log(x2!), ...]
    --------------
    Example:
    >>> log_fac = mk_log_fac(10)
    >>> log_fac(3)
    1.791759469228055
    >>> log_fac(11)
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    IndexError: list index out of range
    >>> log_fac(0)
    np.inf
    >>> log_fac(-1)
    np.inf
    """
    vprint(VERBOSE, 'Setting up log-factorial table for x = [1,%i]'%(max_x))

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
    ------------------------------------
    Output is an (n x m) np.matrix with entries -1, 0, 1
    based on bot/top regulated.
    """
    vprint(VERBOSE, 'Determining up/down regulated genes')
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

def cross_hgd(mtx_a, names_a, mtx_b, names_b, dxn = 1):
    """
    Given two sig matrices, compute HGD sim score across
    the pairs, i.e., for x_i in `new` and y_j in `old`, compute
    HGD_sim(x_i, y_j) for all such i,j.  Here, `HGD sim` is
    defined to be P(X <= matches(x_i, y_j)), in other words the
    CDF of the HGD as parametrized by the current pairs.
    -----------------------------
    new_mtx: (n x m) matrix of n tests & m probes/genes
             where M[i,j] = -1,0,1 means down/not/up regulated
    old_mtx: (n x m) matrix of n tests & m probes/genes 
             where M[i,j] = -1,0,1 means down/not/up regulated
    new_names, old_names: the name associated with each test
    dxn    : if dxn == 1, match up regulated
             if dxn == -1, match down regulated
    """
    vprint(INFO, 'Computing the the log-HGD score between each probe')

    if   dxn ==  1: 
        mtx_a = (mtx_a ==  1) * 1
        mtx_b = (mtx_b ==  1) * 1
    elif dxn == -1: 
        mtx_a = (mtx_a == -1) * 1
        mtx_b = (mtx_b == -1) * 1
    else: raise KeyError

    vprint(VERBOSE, 'Setting up basic sub matrices...')
    total        = mtx_a.shape[1]

    sum_a = mtx_a.sum(1)
    sum_b = mtx_b.sum(1).transpose()

    tmin_sum_a = total - sum_a
    tmin_sum_b = total - sum_b

    sum_mtx_a = np.tile(sum_a, (1, len(names_b)))
    sum_mtx_b = np.tile(sum_b, (len(names_a), 1))

    tmin_sum_mtx_a = np.tile(tmin_sum_a, (1, len(names_b)))
    tmin_sum_mtx_b = np.tile(tmin_sum_b, (len(names_a), 1))

    log_fac = mk_log_fac(total)

    vprint(VERBOSE, 'Calculate factorial versions...')
    ftotal            = log_fac(total)

    fsum_mtx_a = np.tile(log_fac(sum_a), (1, len(names_b)))
    fsum_mtx_b = np.tile(log_fac(sum_b), (len(names_a), 1))

    ftmin_sum_mtx_a = np.tile(log_fac(tmin_sum_a), (1, len(names_b)))
    ftmin_sum_mtx_b = np.tile(log_fac(tmin_sum_b), (len(names_a), 1))

    prob = np.zeros(fsum_mtx_a.shape)

    ### Now that we've initialized the constants, time
    ### to iterate the stuffs!

    vprint(VERBOSE, "Iterate along number of matches to calculate CDF...")
    # Method 2
    match           = mtx_a * mtx_b.transpose()
    ssmin_match_row = sum_mtx_a - match
    ssmin_match_col = sum_mtx_b - match
    final_factor = total - sum_mtx_a - sum_mtx_b + match

    fmatch            = log_fac(match)
    fssmin_match_row  = log_fac(ssmin_match_row)
    fssmin_match_col  = log_fac(ssmin_match_col)
    ffinal_factor     = log_fac(final_factor)

    for i in range(np.triu(match, 1).max()+1):
        log_prob = (fsum_mtx_a + fsum_mtx_b + ftmin_sum_mtx_a +
                    ftmin_sum_mtx_b - ftotal - fmatch - 
                    fssmin_match_row - fssmin_match_col - ffinal_factor)
        
        prob += np.exp(log_prob)

        # Init _matrices to track what changes need to be made
        # to update factorial matrices.  Allows iterative calculation
        # of CMF by det PMF at each point.

        # First, set variables to approp values for next val of PMF...
        _match           = match - i
        _ssmin_match_row = ssmin_match_row + i + 1
        _ssmin_match_col = ssmin_match_col + i + 1
        _final_factor    = final_factor - i
        
        impt_indices = (_match <= 0)

        # Clip non-positive values...
        _match[_match <= 0] = 1
        _ssmin_match_row[_ssmin_match_row <= 0] = 1
        _ssmin_match_col[_ssmin_match_col <= 0] = 1
        _final_factor[_final_factor <= 0] = 1

        # Factor into the calcs so that they get added in 
        # on the next iter of loop!
        fmatch           -= np.log(_match)
        fssmin_match_row += np.log(_ssmin_match_row)
        fssmin_match_col += np.log(_ssmin_match_col)
        ffinal_factor    -= np.log(_final_factor)

        fmatch[impt_indices] = np.inf

        progress_bar(i, np.triu(match,1).max()+1, 1)
    progress_bar_complete(np.triu(match,1).max()+1)
    return prob

def self_hgd(mtx, names, dxn = 1):
    """
    Use cross_hgd to compute similarities with self.
    """
    m = cross_hgd(mtx, names, mtx, names, dxn)
    np.fill_diagonal(m, 1) # maybe 0 instead, so we ignore it?
    return m

def augment_hgd(new_sigs, new_names, old_sigs, old_names, old_hgd, dxn = 1):
    """
    Given `old` matrix of HGD sim scores (computed from `old_sigs`),
    create augmented matrix of HGD sim scores featuring both old and
    `new` sigs.
    -----------------------------------------------
    new_sigs, old_sigs: (n x m) matrix of n tests & m probes/genes
                        where M[i,j] = -1,0,1 means down/not/up regulated
    new_names, old_names: test names assoc'd with above sig matrices
    old_hgd: hgd_sim matrix of old_sigs
    dxn: 1,-1 for up/down regulated
    """
    comb_hgd = cross_hgd(new_sigs, new_names, old_sigs, old_names, dxn)
    new_hgd  = self_hgd(new_sigs, new_names, dxn)

    old_dim   = old_hgd.shape[0]
    new_dim   = new_hgd.shape[0]
    total_dim = old_dim + new_dim

    total_m = np.zeros((total_dim, total_dim))

    total_m[:old_dim, :old_dim] = old_hgd
    total_m[old_dim:, :old_dim] = comb_hgd
    total_m[:old_dim, old_dim:] = comb_hgd.transpose()
    total_m[old_dim:, old_dim:] = new_hgd

    return total_m

if __name__ == '__main__':
    from utils import read_mtx
    sig_mtx, testnames, rownames = read_mtx('./test/main/sig_mtx.csv', transpose = False, rowname = True, colname = True)
    up_hgd_mtx = self_hgd(sig_mtx, testnames, 1)
    down_hgd_mtx = self_hgd(sig_mtx, testnames, -1)
