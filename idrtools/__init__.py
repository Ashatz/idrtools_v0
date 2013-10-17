import win32com.client
import os
from glob import glob
import re
from sys import exit

try: #
        api = win32com.client.Dispatch("idrisi32.IdrisiAPIServer")
except: #
        print "Error: please install an appropriate version of pywin32." #
<<<<<<< HEAD
        exit() #

project_folder = 'C:\\Program Files (x86)\\IDRISI Selva\\Projects\\'
default_project = ["default"]
=======
        sys.exit() #

#Access working directory filepath
workdir = api.GetWorkingDir()

#Access resource directory (or directories) filepath(s)
count = api.GetResourceDirCount()
resdirs = []
for i in range(count):
        resdirs.append(api.GetResourceDir(i+1))

#List all available directories in the workspace
dirlist = []
dirlist.append(workdir)
dirlist.extend(resdirs)

>>>>>>> b601b1f8513778c1de5ca86426ac8396ada6b3b8
#Set default palette for file display
palette = 'quant'

from idrtools.idrexplorer import *
from idrtools.idrfiles import *
from idrtools.modules import *
from idrtools import mytools

def DisplayFile(file_name, disp_palette = palette):
        api.DisplayFile(file_name, disp_palette)
