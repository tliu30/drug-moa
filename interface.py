#########################################################
#expression_matrix (+ existing) -> HGD_sim
#expression_matrix (+ exiting) -> sig files (I THINK THIS IS WASTEFUL)
#list_of_sigs (+ existing) -> HGD_sim
#
#HGD_sim -> GN
#
#View GN
#
#------------
#
#What for HGD_SIM output?
#
#HGD_UP
#HGD_DOWN
#HGD_AVERAGE
#MASTER_LIST
#SIG_MTX
from utils import * 
from sigs import *
from similarity2 import *
from numpy import vstack
import itertools
import os
from cluster import gn
from to_source import *

def gn_go(ifname, odir, cutoff, focus = None):
    g = mtx_to_gt(ifname, cutoff)
    gn(g, odir, focus)
    to_source(odir)
    copy_view(odir, './output/html/view.html')

def view_gn(idir):
    os.system('./ex.sh ' +  idir)

def create_hgd_from_expr(odir, ifname, transpose, num_top, num_bot):
    """
    Doesn't check match
    """
    expr_mtx, test_names, probe_names = read_mtx(ifname, transpose = transpose, rowname = True, colname = True)
    sig_mtx = expr_to_sigs(expr_mtx, num_top, num_bot)

    up_hgd_mtx   = self_hgd(sig_mtx, test_names, 1)
    down_hgd_mtx = self_hgd(sig_mtx, test_names, -1)
    avg_hgd_mtx  = (up_hgd_mtx + down_hgd_mtx) / 2

    # Filenames
    fname_up_hgd      = os.path.join(odir, 'HGD_UP_REG.csv')
    fname_down_hgd    = os.path.join(odir, 'HGD_DOWN_REG.csv')
    fname_avg_hgd     = os.path.join(odir, 'HGD_AVG.csv')
    fname_sigs        = os.path.join(odir, 'sig_mtx.csv')
    fname_master_list = os.path.join(odir, 'probelist.csv')

    # Write files
    write_mtx(fname_up_hgd, up_hgd_mtx, test_names, test_names)
    write_mtx(fname_down_hgd, down_hgd_mtx, test_names, test_names)
    write_mtx(fname_avg_hgd, avg_hgd_mtx, test_names, test_names)
    write_mtx(fname_sigs, sig_mtx, test_names, probe_names)
    open(fname_master_list, 'w').write( '\n'.join(probe_names) )

    return None

def add_hgd_from_expr(odir, old_dir, ifname, transpose, num_top, num_bot):
    # Filenames
    old_up_hgd_ifname   = os.path.join(old_dir, 'HGD_UP_REG.csv')
    old_down_hgd_ifname = os.path.join(old_dir, 'HGD_DOWN_REG.csv')
    old_sig_ifname      = os.path.join(old_dir, 'sig_mtx.csv')

    old_up_hgd_mtx, _, _ = read_mtx(old_up_hgd_ifname, transpose = False, rowname = True, colname = True)
    old_down_hgd_mtx, _, _ = read_mtx(old_down_hgd_ifname, transpose = False, rowname = True, colname = True)
    old_sig_mtx, old_test_names, old_probe_names = read_mtx(old_sig_ifname, transpose = False, rowname = True, colname = True)
    
    new_expr_mtx, new_test_names, new_probe_names = read_mtx(ifname, transpose = transpose, rowname = True, colname = True)
    new_sig_mtx = expr_to_sigs(new_expr_mtx, num_top, num_bot)

    up_hgd_mtx   = augment_hgd(new_sig_mtx, new_test_names, old_sig_mtx, old_test_names, old_up_hgd_mtx, 1)
    down_hgd_mtx = augment_hgd(new_sig_mtx, new_test_names, old_sig_mtx, old_test_names, old_down_hgd_mtx, -1)
    avg_hgd_mtx  = (up_hgd_mtx + down_hgd_mtx) / 2

    sig_mtx = vstack((old_sig_mtx, new_sig_mtx))
    
    test_names  = old_test_names + new_test_names
    probe_names = old_probe_names + new_probe_names

    # Filenames
    fname_up_hgd      = os.path.join(odir, 'HGD_UP_REG.csv')
    fname_down_hgd    = os.path.join(odir, 'HGD_DOWN_REG.csv')
    fname_avg_hgd     = os.path.join(odir, 'HGD_AVG.csv')
    fname_sigs        = os.path.join(odir, 'sig_mtx.csv')
    fname_master_list = os.path.join(odir, 'probelist.csv')

    # Write files
    write_mtx(fname_up_hgd, up_hgd_mtx, test_names, test_names)
    write_mtx(fname_down_hgd, down_hgd_mtx, test_names, test_names)
    write_mtx(fname_avg_hgd, avg_hgd_mtx, test_names, test_names)
    write_mtx(fname_sigs, sig_mtx, test_names, probe_names)
    open(fname_master_list, 'w').write( '\n'.join(probe_names) )

    return None

def create_hgd_from_sigs(odir, sig_files, master_fname):
    if master_fname != None:
        master = open(master_fname).read().strip().split('\n')
    else:
        master = list(set(list(itertools.chain(*list(itertools.chain(*[read_sig_file(sig_file) for sig_file in sig_files]))))))
    sig_mtx, test_names, probe_names = sigs_to_mtx(sig_files, master) 

    up_hgd_mtx   = self_hgd(sig_mtx, test_names, 1)
    down_hgd_mtx = self_hgd(sig_mtx, test_names, -1)
    avg_hgd_mtx  = (up_hgd_mtx + down_hgd_mtx) / 2

    # Filenames
    fname_up_hgd      = os.path.join(odir, 'HGD_UP_REG.csv')
    fname_down_hgd    = os.path.join(odir, 'HGD_DOWN_REG.csv')
    fname_avg_hgd     = os.path.join(odir, 'HGD_AVG.csv')
    fname_sigs        = os.path.join(odir, 'sig_mtx.csv')
    fname_master_list = os.path.join(odir, 'probelist.csv')

    # Write files
    write_mtx(fname_up_hgd, up_hgd_mtx, test_names, test_names)
    write_mtx(fname_down_hgd, down_hgd_mtx, test_names, test_names)
    write_mtx(fname_avg_hgd, avg_hgd_mtx, test_names, test_names)
    write_mtx(fname_sigs, sig_mtx, test_names, probe_names)
    open(fname_master_list, 'w').write( '\n'.join(probe_names) )

    return None

def add_hgd_from_sigs(odir, old_dir, sig_files):
    # Filenames
    old_up_hgd_ifname   = os.path.join(old_dir, 'HGD_UP_REG.csv')
    old_down_hgd_ifname = os.path.join(old_dir, 'HGD_DOWN_REG.csv')
    old_sig_ifname      = os.path.join(old_dir, 'sig_mtx.csv')
    master              = open( os.path.join(old_dir, 'probelist.csv') ).read().strip().split('\n')

    old_up_hgd_mtx, _, _ = read_mtx(old_up_hgd_ifname, transpose = False, rowname = True, colname = True)
    old_down_hgd_mtx, _, _ = read_mtx(old_down_hgd_ifname, transpose = False, rowname = True, colname = True)
    old_sig_mtx, old_test_names, old_probe_names = read_mtx(old_sig_ifname, transpose = False, rowname = True, colname = True)

    num_top = (old_sig_mtx[0,] ==  1).sum()
    num_bot = (old_sig_mtx[0,] == -1).sum()
    
    new_sig_mtx, new_test_names, new_probe_names = sigs_to_mtx(sig_files, master) #CHECK? Test Names? Probe Names?

    up_hgd_mtx   = augment_hgd(new_sig_mtx, new_test_names, old_sig_mtx, old_test_names, old_up_hgd_mtx, 1)
    down_hgd_mtx = augment_hgd(new_sig_mtx, new_test_names, old_sig_mtx, old_test_names, old_down_hgd_mtx, -1)
    avg_hgd_mtx  = (up_hgd_mtx + down_hgd_mtx) / 2

    sig_mtx = vstack((old_sig_mtx, new_sig_mtx))
    
    test_names  = old_test_names + new_test_names
    probe_names = old_probe_names + new_probe_names

    # Filenames
    fname_up_hgd      = os.path.join(odir, 'HGD_UP_REG.csv')
    fname_down_hgd    = os.path.join(odir, 'HGD_DOWN_REG.csv')
    fname_avg_hgd     = os.path.join(odir, 'HGD_AVG.csv')
    fname_sigs        = os.path.join(odir, 'sig_mtx.csv')
    fname_master_list = os.path.join(odir, 'probelist.csv')

    # Write files
    write_mtx(fname_up_hgd, up_hgd_mtx, test_names, test_names)
    write_mtx(fname_down_hgd, down_hgd_mtx, test_names, test_names)
    write_mtx(fname_avg_hgd, avg_hgd_mtx, test_names, test_names)
    write_mtx(fname_sigs, sig_mtx, test_names, probe_names)
    open(fname_master_list, 'w').write( '\n'.join(probe_names) )

    return None

if __name__ == '__main__':
    
    #create_hgd_from_expr('./test/main/', './test/main_expr_mtx.csv', True, 10, 10)
    add_hgd_from_expr('./test/aug/', './test/main/', './test/aux_expr_mtx.csv', True)
    #create_hgd_from_sigs('./test/just_sigs/', ['./test/sigs/' + x for x in os.listdir('./test/sigs/')], './test/main/probelist.csv')
    #add_hgd_from_sigs( './test/aug_sigs/', './test/main/', ['./test/sigs/' + x for x in os.listdir('./test/sigs/')])
