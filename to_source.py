import os
import json
def to_source(odir):
    f = open( os.path.join(odir, 'index.csv') ).read().strip().split('\n')

    d = {}
    for line in f[1:]:
        line = line.split(',')
        name = line[0]
        d[name] = []
        for i in range(len(line[1:])):
            item = int(float(line[i+1]))
            if item < 0: break
            else:
                d[name].append( str(i) + '_' + str(item) )

    open( os.path.join(odir, 'sources.json'), 'w').write( json.dumps(d) )

def copy_view(odir, template_path):
    # need a better way to deal with path...
    open( os.path.join(odir, 'view.html'), 'w').write( open(template_path).read() )
