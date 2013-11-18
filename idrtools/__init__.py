import win32com.client
import os
from glob import glob
import re
from sys import exit
import shutil

try: #
        api = win32com.client.Dispatch("idrisi32.IdrisiAPIServer")
except: #
        print "Error: please install an appropriate version of pywin32." #
        exit() #

#These functions allow the creation of temporary "dump" directories for
#for unnecessary intermediary files.
                
#Added 10/11/2013
def addDumpDir(dir):
        os.chdir(dir)
        if dir[-1] != '\\':
                dir += '\\'
        dumpfile = dir + 'dump\\'
        
        try:
                os.mkdir(dumpfile[:-1])
        except OSError:
                pass

        return dumpfile

#Added 10/11/2013
def removeDumpDir(dumpdir):
        shutil.rmtree(dumpdir)

default_palette = ["quant"]

from idrtools.idrexplorer import *
from idrtools.idrfiles import *
from idrtools.modules import *
from idrtools import mytools

def displayLauncher(image, filetype, palette = default_palette[0]):
        project = IdrisiExplorer()
        dirlist = project.getProjectDirs()
        display_file = findFile(image, filetype, dirlist)
        display_doc = Documentation(display_file)
        if display_doc.DataType() == 'RGB24':
                api.DisplayFile(display_file)
        else:
                api.DisplayFile(display_file, palette)

#Function created 10/29/2013
def setDefaultPalette(new_palette):
        path = os.path.dirname(__file__)+'\\__init__.py'
        read_init_ = open(path, 'r')
        lines = read_init_.readlines()
        read_init_.close()
        index = []
        for line in lines:
                if 'default_palette = [' in line:
                        index.append(lines.index(line))
        lines[index[0]] = 'default_palette = ["%s"]\n'%(new_palette)
        write_init_ = open(path, 'w')
        for line in lines:
                write_init_.write(line)
        write_init_.close()
        default_palette[0] = new_palette


