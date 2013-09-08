from idrtools import *
from idrtools.idrfiles import *

def initial(output, outtype, outfile, value, define, definition):
    outtype = str(outtype)
    outfile = str(outfile)
    value = str(value)
    define = str(define)
    if define == '1':
        rdc = readDocFile(definition, 'rdc', dirlist)
        api.RunModule("INITIAL", output+'*'+outtype+'*'+outfile+'*'+value+'*1*'\
                      +definition+'*'+rdc['ref. units'], 1, '', '', '', '', 1)
    elif define == '2':
        api.RunModule("INITIAL", output+'*'+outtype+'*'+outfile+'*'+value+'*1*'\
                      +definition[0]+'*'+definition[1]+'*'+definition[2]+'*'+definition[3]\
                      +'*'+definition[4]+'*'+definition[5]+'*'+definition[6]+'*'+definition[7]\
                      +'*'+definition[8]+'*'+definition[9], 1, '', '', '', '', 1)
