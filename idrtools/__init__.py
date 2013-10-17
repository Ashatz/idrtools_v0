import win32com.client
import os
from glob import glob
import re
from sys import exit

try: #
        api = win32com.client.Dispatch("idrisi32.IdrisiAPIServer")
except: #
        print "Error: please install an appropriate version of pywin32." #
        exit() #

project_folder = 'C:\\Program Files (x86)\\IDRISI Selva\\Projects\\'
default_project = ["default"]
#Set default palette for file display
palette = 'quant'

from idrtools.idrexplorer import *
from idrtools.idrfiles import *
from idrtools.modules import *
from idrtools import mytools

def DisplayFile(file_name, disp_palette = palette):
        api.DisplayFile(file_name, disp_palette)
