MASTER_PATH = 'path_to_master_list_of_stuff'

from sys_settings import MASTER_PATH

# Full list of 
MASTER_LIST = open(MASTER_PATH, 'r').read().strip().split('\n')

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
    
def sig_to_row(sig_file, master = MASTER_LIST):
    up, down = read_sig_file(sig_file)
    
    row = np.zeros( (1, len(master) )
    for idx, name in master:
        if name in up: 
            row[idx] = 1
        elif name in down:
            row[idx] = -1
        else: continue
    return row

def sigs_to_mtx(sig_files, master):
    rows = map(lambda x: sig_to_row(x, master), sig_files)
    mtx = np.vstack(rows)
    return mtx
