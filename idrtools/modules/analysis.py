from idrtools import *
from idrtools.idrfiles import *


def contour(input, output, minimum, maximum, interval, generalize, background='n'):
    minimum=str(minimum)
    maximum=str(maximum)
    interval=str(interval)
    background=str(background)
    if background != 'n':
        api.RunModule("CONTOUR", input+'*'+output+'*'+minimum+'*'+maximum+'*'+\
                      interval+'*'+generalize+'*y*'+background, 1, '', '', '', \
                      '', 1)
    else:
        api.RunModule("CONTOUR", input+'*'+output+'*'+minimum+'*'+maximum+'*'+\
                      interval+'*'+generalize+'*n', 1, '', '', '', '', 1)

def extract(featinput, procinput, summarytype, outtype, output):
    summarytype = str(summarytype)
    outtype = str(outype)
    if outtype == '1':
        api.RunModule("EXTRACT", featinput+'*'+procinput+'*1*'+summarytype+'*'\
                      +output, 1, '', '', '', '', 1)
    if outtype == '2':
        api.RunModule("EXTRACT", featinput+'*'+procinput+'*3*'+summarytype+'*'\
                      +output, 1, '', '', '', '', 1)
    return output

def overlay(input1, input2, output, operation):
    operation = str(operation)
    api.RunModule("OVERLAY", operation+'*'+input1+'*'+input2+'*'+output, \
                  1, '', '', '', '', 1)
    return output

def random(input, output, datatype, distribution, maxint_mean, stdev = None):
    datatype = str(datatype)
    distribution = str(distribution)
    maxint_mean = str(maxint_mean)
    stdev = str(stdev)
    if stdev != None:
        api.RunModule("RANDOM", output+'*1*'+datatype+'*'+input+'*'+\
                      distribution+'*'+maxint_mean+'*'+stdev, 1, '', ''\
                      , '', '', 1)
    else:
        api.RunModule("RANDOM", output+'*1*'+datatype+'*'+input+'*'+\
                      distribution+'*'+maxint_mean, 1, '', '', '', '',\
                      1)
    return output

def rank(input, output, order1, input2=None, order2=None):
    order1 = str(order1)
    if input2 == None and order2 == None:
        api.RunModule("RANK", input+'*none*'+output+'*'+order1, 1, '', '', '', \
                      '', 1)
    if input2 != None and order2 != None:
        order2 = str(order2)
        api.RunModule("RANK", input+'*'+input2+'*'+output+'*'+order1+'*'+order2,\
                      1, '', '', '', '', 1) 

def reclass(filetype, input, output, outtype, classtype, rcl):
    if filetype == 'raster' or filetype == 'rst':
        filetype = 'i'
    if filetype == 'vector' or filetype == 'vct':
        filetype = 'v'
    if filetype == 'attribute' or filetype == 'avl':
        filetype = 'a'
    classtype = str(classtype)
    outtype = str(outtype)
    if classtype == '1':
        api.RunModule("RECLASS", filetype+'*'+input+'*'+output+'*1*'+str(rcl[0])+'*'\
                      +str(rcl[1])+'*'+str(rcl[2])+'*'+outtype, 1, '', '', '', '', 1)
    if classtype == '2':
        tmprcl = writeRcl('tmprcl', workdir, rcl)
        api.RunModule("RECLASS", filetype+'*'+input+'*'+output+'*3*'+tmprcl+'*'+outtype, \
                      1, '', '', '', '', 1)
    if classtype == '3':
        api.RunModule("RECLASS", filetype+'*'+input+'*'+output+'*1*'+rcl+'*'+outtype,\
                      1, '', '', '', '', 1)
    return output

def scalar(input, output, operation, number):
    operation = str(operation)
    number = str(number)
    api.RunModule("SCALAR", input+'*'+output+'*'+operation+'*'+number, \
                  1, '', '', '', '', 1)
    return output

def standard(input, output, mask=None):
    if mask != None:
        api.RunModule("STANDARD", input+'*'+output+'*'+mask, 1, '', '', '',\
                      '', 1)
    else:
        api.RunModule("STANDARD", input+'*'+output, 1, '', '', '', '', 1)
    return output

def toprank(input, output, ranktype, n_percent, mask='none', reverse='2', revoutput='N/A'):
    reverse=str(reverse)
    ranktype=str(ranktype)
    n_percent=str(n_percent)
    if ranktype == '2' and (int(n_percent) > 100 or int(n_percent) < 0):
        print "Please insert a valid percentage value (0-100)"
    else:
        if reverse == '1':
            api.RunModule("TOPRANK", input+'*'+mask+'*'+ranktype+'*'+\
                          n_percent+'*'+output+'*'+reverse+'*'+revoutput,\
                          1, '', '', '', '', 1)
        else:
            api.RunModule("TOPRANK", input+'*'+mask+'*'+ranktype+'*'+\
                          n_percent+'*'+output+'*'+reverse, 1, '', '',\
                          '', '', 1)
