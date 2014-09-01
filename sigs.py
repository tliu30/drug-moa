import os
import numpy as np
#MASTER_PATH = 'path_to_master_list_of_stuff'

#from sys_settings import MASTER_PATH

# Full list of 
#MASTER_LIST = open(MASTER_PATH, 'r').read().strip().split('\n')

def read_sig_file(sig_file):
    """
    Assumes sig_files are formatted as
    
    UP
    sig
    sig
    sig
    ...
    last_sig

    DOWN
    sig
    sig
    ...

    """
    up, down = open(sig_file).read().split('\n\n')
    up = up.strip().split('\n')[1:]
    down = down.strip().split('\n')[1:]
    return (up, down)
    
def sig_to_row(sig_file, master):
    up, down = read_sig_file(sig_file)
    
    row = [0] * len(master)
    for (idx, name) in enumerate(master):
        if name in up: 
            row[idx] = 1
        elif name in down:
            row[idx] = -1
        else: continue

    name = os.path.splitext(os.path.split(sig_file)[1])[0]
    return (name, row)

def sigs_to_mtx(sig_files, master):
    tests, rows = zip(*map(lambda x: sig_to_row(x, master), sig_files))
    mtx = np.vstack(rows)

    return ( np.matrix(mtx), list(tests), master)
