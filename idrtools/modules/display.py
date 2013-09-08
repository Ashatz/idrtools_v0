from idrtools import *
from idrtools.idrfiles import *

def composite(blue, green, red, output, stretch='1', background ='2', saturation='1', \
              outType='3'):
    stretch=str(stretch)
    background=str(background)
    saturation=str(saturation)
    if stretch != '1':
        saturaton = '#'
    outTye=str(outType)
    api.RunModule("COMPOSITE", blue+'*'+green+'*'+red+'*'+output+'*'+stretch+'*'+\
                  background+'*'+saturation+'*'+outType, 1, '', '', '', '', 1)

def displayLauncher(input):
    api.DisplayFile(input, palette)

def ortho(surface, output, resolution, drape=False, palette=palette, direction='#',\
          angle='#', exaggeration='#', newmin='#', newmax='#'):
    resolution = str(resolution)
    direction = str(direction)
    exaggeration=str(exaggeration)
    newmin=str(newmin)
    newmax=str(newmax)
    if surface[-4:] != '.rst':
        surface = surface+'.rst'
    directory = findfile(surface, 'rst', dirlist)
    if directory != None:
        surface = directory+surface
    if drape==False:
        api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                      '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax, 1, ''\
                      , '', '', '', 1)
    else:
        fileRdc = readDocFile(drape, 'RDC', dirlist)
        if fileRdc['data type'] == 'RGB24':
            api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                          '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax+'*'+\
                          drape+'*'+palette, 1, '', '', '', '', 1)
        else:
            api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                          '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax+'*'+\
                          drape+'*'+palette, 1, '', '', '', '', 1)



def pyramid(process, inputType, input):
    process = str(process)
    inputType = str(inputType)
    if inputType == '1' or inputType == '2':
        if inputType == '1':
            fileType = 'rst'
        elif inputType == '2':
            fileType = 'rgf'
        directory = findfile(input, inputType, dirlist)
        if directory != None:
            api.RunModule("PYRAMID", process+'*'+inputType+'*'\
                          +directory+input, 1, '', '', '', '', 1)
        else:
            api.RunModule("PYRAMID", process+'*'+inputType+'*'\
                          +input, 1, '', '', '', '', 1)
    else:
        print "Input filetype must be a raster image (1) or a raster" \
              +" group file (2)."
