from similarity import *
from utils import *
from fake_log import *
from cluster import *

if __name__ == '__main__':
    fname = './test.mtx'

    sigout = './test_sig.mtx'
    simout = './test_HGDsim.mtx'
    odir   = './test_gn'

    # Take expression data and compute HGD
    create_hgd_mtx(fname, simout, (30,30), transpose = True, rowname = False)

    # (Also create sig matrix for some test evaluation)
    expr_mtx, rowname, colname = read_mtx(fname, transpose = True)
    sigs_mtx = expr_to_sigs(expr_mtx, 30, 30)
    write_mtx(sigout, sigs_mtx, rowname, colname)

    # Do clustering
    graph = mtx_to_gt(simout, 0.8)
    gn(graph, odir)


    #### Next, the add one process
#   add_one = './test_add.mtx'
#   add_mtx, rowname, colname = read_mtx(add_one, transpose = TRUE)
#   add_sig_mtx = expr_to_sigs(add_mtx, 30, 30) 
