import sys

GLOBAL_VERBOSE_FLAG = False

# Short for verbose-print
def vprint(level, *args):
    out = ''.join([str(x) for x in args])
    if level == 0:
        print out
    elif level == 1:
        if GLOBAL_VERBOSE_FLAG:
            print out
        else: pass
    else: pass
    return None

def progress_bar(current, total, sep):
    if current % sep  == 0: 
        bar  = '[' + '|' * (current * 30/ total) + ' ' * (30 - (current * 30 / total)) + ']'
        prog = '%.1f%% (%i/%i)'%(current * 100. / total, current, total)
        sys.stdout.write('\r' + bar + ' ' + prog)
        sys.stdout.flush()
    else: pass
    return None

def progress_bar_complete(total):
    bar = '[' + '|' * 30 + ']'
    prog = '100%% (%i/%i)'%(total, total)
    sys.stdout.write('\r' + bar + ' ' + prog + '\n')
    sys.stdout.flush()
