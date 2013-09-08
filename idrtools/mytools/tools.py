from idrtools import *
from idrtools.modules import *
import os
import shutil

dumpdir = workdir+'dump\\'

def nsamples(samples, mask, output, outtype='uniform'):
    try:
        os.mkdir(dumpdir[:-1])
    except OSError:
        pass
    random(mask, dumpdir+'tmp001', 3, 2, 127, 20)
    overlay(mask, dumpdir+'tmp001', dumpdir+'tmp002', 3)
    rank(dumpdir+'tmp002', dumpdir+'tmp003', 'd')
    reclass = [[0,0,2],[1,2,samples+2],[0,samples+2,99999999999]]
    if outtype == 'uniform':
        reclass('raster', dumpdir+'tmp003',output, 1, 2, reclass)
    elif outtype == 'ranked':
        reclass('raster', dumpdir+'tmp003',dumpdir+'tmp004', 1, 2, reclass)
        rank(dumpdir+'tmp004', dumpdir+'tmp005', 'd')
        overlay(dumpdir+'tmp004', dumpdir+'tmp005', output, 3)


