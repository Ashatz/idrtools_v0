from idrtools import *
from idrtools.idrfiles import *
import os
import shutil
from glob import glob

def metaupdate(intype, input, option, value):
    intype = str(intype)
    option = str(option)
    value = str(value)
    if type(input) == 'list':
        api.RunModule("METAUPDTE", intype +'*'+input+'*'+option+\
                      '*'+str(value), 1, '', '', '', '', 1)
    else:
        list = [input]
        rgfName = input+'.rgf'
        #Create filepath for the trash directory
        dumpfile = dirlist[0]+'dump\\'
        #Create trash directory
        try:
            os.mkdir(dumpfile[:-1])
        except OSError:
            pass
        if intype == '1':
            filetype = 'rst'
        elif intype == '2':
            filetype = 'vct'
        rgfPath = findfile(input, filetype, dirlist)
        writeRgf(rgfPath, list, rgfName)
        api.RunModule("METAUPDTE", intype+'*'+input+'*'+option+\
                      '*'+value, 1, '', '', '', '', 1)
        shutil.move(rgfPath+rgfName, dumpfile+rgfName)
        shutil.rmtree(dumpfile)

        
