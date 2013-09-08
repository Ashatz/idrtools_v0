"""
Raster Group File Module
Created by A.J. Shatz
01/23/2013

This module was designed to allow user functionality with Raster Group Files in IDRISI. 

Log:
07/13/2013 - v1 - module file created and placed in idrtools package. readRgf and writeRgf modules 
modified using list comprehensions. 
"""
from idrtools import *
import os
from glob import glob

#List/find directories of raster group file names
#Parameters:
#filename - name of desired raster group file
#List/find directories of raster group file names
def findfile(filename, filetype, directories):
    for directory in directories:
        os.chdir(directory)
        filelist = glob('*')
        newlist = [file.lower() for file in filelist if file[-3:].lower() == filetype.lower()]
        if filename[-4:].lower() == '.'+filetype.lower():
            test = filename.lower() in newlist
        elif filename[-4] == '.' and filename[-3:].lower() != filetype.lower():
            test = filename[:-3].lower()+filetype.lower()
        else:
            test = filename.lower()+'.'+filetype.lower() in newlist 
        if test == True:
            return directory
            break
			
#Convert input raster group files to list
#Parameters:
#inputfile - name of the input raster group file
#directories - list of directories present in the 
def readRgf(inputfile, directories):
    if inputfile [-4:] != '.rgf':
        inputfile = inputfile+'.rgf'
    path = findfile(inputfile, 'rgf', directories)+inputfile
    readfile = open(path, 'r')
    #First line of .rgf files indicates number of filenames
    length = int(readfile.readline())
    list = readfile.readlines()
    for i in range(length):
        list[i] = list[i][:-1]
    return list
	
#Create raster group file of given name with
#list of files in given directory 
#Parameters:
#directory = output directory
#filelist = list of files 
#rgfname - name of the output raster group file
def writeRgf(directory, filelist, rgfname):
    if rgfname[-4:] != ".rgf":
	    rgfname = rgfname+".rgf"
    if directory[-1] != '\\':
	    directory = directory+'\\'
    rgfPath = directory+rgfname
    writefile = open(rgfPath, 'w')
    writefile.write(str(len(filelist))+'\n')
    [writefile.write(file+'\n') for file in filelist]
    writefile.close()

def readAvl(inputavl, directories, skipline1=True):
    #Create .avl file of P/E ratio per Habitat Suitability value
    #Open created .avl file
    directory = findfile(inputavl, 'avl', directories)
    if inputavl[-4:] != '.avl':
        inputavl = inputavl+'.avl'
    avlFile = directory + inputavl
    readavl = open(avlFile, 'r')
    #Read line 1 if skipline1=True
    if skipline1 == True:
        readavl.readline()
    #Create list out of remaining lines
    lines = readavl.readlines()
    outlist = []
    for line in lines:
        split = line.split()
        outlist.append(float(split[1]))
    readavl.close()
    return outlist

def writeRcl(rclname, directory, reclasslist):
    if rclname[-4:] != '.rcl':
        rclname = rclname+'.rcl'
    outputrcl = directory+rclname
    rclwrite=open(outputrcl, 'w')
    for row in reclasslist:
        rclwrite.write(str(row[0])+' '+str(row[1])+' '+str(row[2])+'\n')
    rclwrite.write('-9999')
    rclwrite.close()
    return outputrcl

def readDocFile(inputfile, filetype, directories):
    docDict = {}
    filetype = filetype.lower()
    if inputfile [-4:] != '.'+filetype:
        if inputfile[-4] == '.' and inputfile[-3:].lower() != filetype.lower():
            inputfile = inputfile[:-4]+'.'+filetype.lower()
        else:
            inputfile = inputfile+'.'+filetype
    path = findfile(inputfile, filetype, directories)+inputfile
    readfile = open(path, 'r')
    lines = readfile.readlines()
    for line in lines:
        tmplist = line.split(':')
        i = len(tmplist[0])-1
        while i >= 0:
            if tmplist[0][i] == ' ':
                i -=1
            else:
                break
        newtmpkey= tmplist[0][:i+1]
        newtmplist = tmplist[1:]
        if len(newtmplist) > 1:
            newtmplist[0] = newtmplist[0][1:]
            newtmpval=':'.join(newtmplist)[:-1]
        else:
            newtmpval=newtmplist[0][1:-1]
        keylist = docDict.keys()
        if newtmpkey in keylist:
            docDict[newtmpkey] += newtmpval
        else:
            docDict[newtmpkey] = newtmpval
    return docDict
    readfile.close()


