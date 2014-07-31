import sys

SUPPRESSED = 0
INFO = 1
VERBOSE = 2

GLOBAL_VERBOSE_LEVEL = INFO

# Short for verbose-print
def vprint(level, *args):
    out = ''.join([str(x) for x in args])
    if level <= GLOBAL_VERBOSE_LEVEL :
        print out
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

# Some test
if __name__ == '__main__':
    print("FIRST, SET VPRINT LEVEL TO SUPPRESSED")
    GLOBAL_VERBOSE_LEVEL = SUPPRESSED
    vprint(INFO, "This is info")
    vprint(VERBOSE, "This is verbose")

    print("FIRST, SET VPRINT LEVEL TO INFO")
    GLOBAL_VERBOSE_LEVEL = INFO
    vprint(INFO, "This is info")
    vprint(VERBOSE, "This is verbose")

    print("FIRST, SET VPRINT LEVEL TO VERBOSE")
    GLOBAL_VERBOSE_LEVEL = VERBOSE
    vprint(INFO, "This is info")
    vprint(VERBOSE, "This is verbose")
