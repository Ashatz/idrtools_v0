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
from os.path import exists, realpath #Updated
from glob import glob
import sys

#This function formats all input file strings and returns
#Updated 
def fixFile(filename, filetype):
    if filename[-4:].lower() != '.'+filetype.lower():
        if filename[-4] == '.' and filename[-3:].lower() != filetype.lower():
            return '%s.%s'%(filename[:-4],filetype.lower())
        else:
            return '%s.%s'%(filename, filetype.lower())
    else:
        return '%s.%s'%(filename[:-4],filetype.lower())

'''
Function - findFile
Purpose - return file name and file path of given input file with extension.
Parameters:
    filename - name of input file.
    filetype - file type extension of output file.
    dirs - list of directories from which to search for the input file.
        default - all working and resource directories within IDRISI
                  Explorer
'''
#Updated 09/15/2013
def findFile(filename, filetype, dirs = dirlist):
    filename = fixFile(filename, filetype)
    testdir = {}
    for dir in dirs:
        os.chdir(dir)
        path = os.path.realpath(filename)
        test = os.path.exists(path)
        testdir[test] = path      
    try:
        output = testdir[True]
        return output
    except KeyError:
        print "Error: input file %s does not contain a valid path."%(filename)
        sys.exit()
        
#Convert input raster group files to list
#Parameters:
#inputfile - name of the input raster group file
#directories - list of directories present in the
#Lines 58-60 updated 9/15/2013
def readRgf(filename, dirs=dirlist): 
    filename = fixFile(filename,'rgf') 
    path = findFile(filename,'rgf') 
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
    for file in filelist:
        if file[-4:] == '.rst':
            file = file[:-4]
        writefile.write(file+'\n')
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

class docFile(): #

    def __init__(self, filename, filetype, dirs = dirlist):
        self.docLines = []
        typelist = ['rdc','vdc','adc']#
        try: #
            typelist.index(filetype.lower()) #
        except: #
            print "Error: please provide valid documentation file extension" #
            sys.exit()#
        
        filename = fixFile(filename, filetype)
        self.filetype = filetype#
        path = findFile(filename, filetype) #
        self.path = path #
        
        try:
            readfile = open(self.path, 'r')
        except:
            print "Error: %s does not exist.  Please insert valid file name."%(path)
            sys.exit() #

        lines = readfile.readlines()
        for line in lines:
            self.docLines.append([line[:14],line[14:-1]])
        readfile.close()

    def displayDocFile(self):
        for line in self.docLines:
            print line[0]+line[1]

    def findIndex(self,attribute):
        attribList = []
        [attribList.append(self.docLines[i][0]) for i in range(len(self.docLines))]
        return attribList.index(attribute)

    def attribOut(self, index, output):
        if output == None:
            return self.docLines[index][1]
        else:
            self.docLines[index][1] = output
            return self.docLines[index][1]

    #Created 9/17/2013
    def readLegend(self):
        index = self.findIndex('legend cats : ')
        if int(self.docLines[index][1]) == 0:
            print 'Error: input file contains no legend.'
            sys.exit()
        else:
            legendDict = {}
            for i in range(index+1, index+int(self.docLines[index][1])+1):
                code = int(self.docLines[i][0][-6:-3])
                legendDict[code] = self.docLines[i][1]
        return legendDict

    #Created 9/17/2013
    def writeLegend(self, legend):
        index = self.findIndex('legend cats : ')
        if int(self.docLines[index][1]) > 0:
            print 'Error: input file already contains a legend.'
            sys.exit()
        else:
            length = len(legend)
            self.docLines[index][1] = str(length)
            legendList = []
            for cat in legend:
                cat = str(cat)
                codeNum = ' '*(3-len(cat))+cat
                attrib = 'code    %s : '%(codeNum)
                legCat = legend[int(cat)]
                legendList.append([attrib,legCat])
            self.docLines[index+1:index+1] = legendList
                
            
    #Created 09/16/2013, Updated 09/17/2013
    def fileFormat(self, output=None, attrib='file format : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/16/2013, Updated 09/17/2013
    def fileTitle(self, output=None, attrib='file title  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/16/2013, Updated 09/17/2013
    def dataType(self, output=None, attrib='data type   : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/16/2013, Updated 09/17/2013
    def fileType(self, output=None, attrib='file type   : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def objectType(self, output=None, attrib=''):
        if self.filetype != 'vdc':
            print "Error: only vector files contain Object Type information."
            sys.exit()
        else:
            return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def columns(self, output=None, attrib='columns     : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def rows(self, output=None, attrib='rows        : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def refSystem(self, output=None, attrib='ref. system : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def refUnits(self, output=None, attrib='ref. units  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def unitDist(self, output=None, attrib='unit dist.  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def minX(self, output=None, attrib='min. X      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def maxX(self, output=None, attrib='max. X      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def minY(self, output=None, attrib='min. Y      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def maxY(self, output=None, attrib='max. Y      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def posError(self, output=None, attrib="pos'n error : "):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def resolution(self, output=None, attrib='resolution  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def minValue(self, output=None, attrib='min. value  :'):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def maxValue(self, output=None, attrib='max. value  :'):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def displayMin(self, output=None, attrib='display min : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def displayMax(self, output=None, attrib='display max : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def valUnits(self, output=None, attrib='value units : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def valError(self, output=None, attrib='value error : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def flagValue(self, output=None, attrib='flag value  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def flagDef(self, output=None, attrib="flag def'n  : "):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def legendCats(self, output=None, attrib='legend cats : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def lineage(self, output=None, attrib='lineage     : '):
        lineageList = []
        for line in self.docLines:
            if line[0] == attrib:
                lineageList.append(line[1])
        return lineageList

    #Created 9/17/2013
    def updateDocFile(self):
        writeDocFile = open(self.path, 'w')
        for line in self.docLines:
            writeDocFile.write('%s%s\n'%(line[0],line[1]))
        writeDocFile.close()
        print "Documentation File update was successful."
            
 


