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
from idrtools.idrexplorer import *
import os
from os.path import exists, realpath #Updated
from glob import glob
from sys import exit

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

    #Updated 09/15/2013
def findFile(filename, filetype, dirs):
    filename = fixFile(filename, filetype)
    testdir = {}
    if type(dirs) != list:
        dirs = [dirs]
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
        exit()

def getDirectories(project = current_project[0]):
    project = IdrisiExplorer(project)
    return project.dirlist

def WriteRef(input_path, parameters):
    #Automatically ensure that the input file path has the proper extension.
    input_path = fixFile(input_path, 'REF')
    ref_lines = [['ref. system : '],['projection  : '],['datum       : '],\
                 ['delta WGS84 : '],['ellipsoid   : '],['major s-ax  : '],\
                 ['minor s-ax  : '],['origin long : '],['origin lat  : '],\
                 ['origin X    : '],['origin Y    : '],['scale fac   : '],\
                 ['units       : '],['parameters  : ']]
    for i in range(len(parameters)):
        ref_lines[i].append(parameters[i])
    write_ref = open(input_path, 'w')
    for line in ref_lines:
        write_ref.write(line[0]+line[1]+'\n')
    write_ref.close()

class Documentation(): #
    def __init__(self, filename):
        project = IdrisiExplorer()
        dirlist = getDirectories()
        self.docLines = []
        input_type = filename[-3:].lower() #Added 10/9/2013
        type_dict = {'rst':'rdc','vct':'vdc','avl':'adc'}#Edited 10/9/2013
        try: #
            doc_type = type_dict[input_type] #Edited 10/9/2013
        except: #
            print "Error: please provide valid documentation file extension" #
            exit()#
        filename = fixFile(filename, doc_type)
        self.filetype = doc_type #Edited 10/9/2013
        self.path = findFile(filename, doc_type, dirlist) #Edited 10/29/2013
        
        try:
            readfile = open(self.path, 'r')
        except:
            print "Error: %s does not exist.  Please insert valid file name."%(path)
            exit() #

        lines = readfile.readlines()
        for line in lines:
            self.docLines.append([line[:14],line[14:-1]])
        self.defaultLines = self.docLines[:]
        readfile.close()

    def DisplayDocFile(self):
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
    def ReadLegend(self):
        index = self.findIndex('legend cats : ')
        if int(self.docLines[index][1]) == 0:
            print 'Error: input file contains no legend.'
            exit()
        else:
            legendDict = {}
            for i in range(index+1, index+int(self.docLines[index][1])+1):
                code = int(self.docLines[i][0][-6:-3])
                legendDict[code] = self.docLines[i][1]
        return legendDict

    #Created 9/17/2013
    def WriteLegend(self, legend):
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

    #Created 9/17/2013
    def updateDocFile(self):
        writeDocFile = open(self.path, 'w')
        for line in self.docLines:
            writeDocFile.write('%s%s\n'%(line[0],line[1]))
        writeDocFile.close()
        print "Documentation File update was successful."
                
            
    #Created 09/16/2013, Updated 09/25/2013
    def FileFormat(self, output=None, attrib='file format : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/16/2013, Updated 09/25/2013
    def FileTitle(self, output=None, attrib='file title  : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/16/2013, Updated 09/25/2013
    def DataType(self, output=None, attrib='data type   : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/16/2013, Updated 09/25/2013
    def FileType(self, output=None, attrib='file type   : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/17/2013
    def ObjectType(self, output=None, attrib=''):
        if self.filetype != 'vdc':
            print "Error: only vector files contain Object Type information."
            sys.exit()
        else:
            return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def Columns(self, output=None, attrib='columns     : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def Rows(self, output=None, attrib='rows        : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def RefSystem(self, output=None, attrib='ref. system : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def RefUnits(self, output=None, attrib='ref. units  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def UnitDist(self, output=None, attrib='unit dist.  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MinX(self, output=None, attrib='min. X      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MaxX(self, output=None, attrib='max. X      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MinY(self, output=None, attrib='min. Y      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MaxY(self, output=None, attrib='max. Y      : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def PosError(self, output=None, attrib="pos'n error : "):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def Resolution(self, output=None, attrib='resolution  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MinValue(self, output=None, attrib='min. value  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def MaxValue(self, output=None, attrib='max. value  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def DisplayMin(self, output=None, attrib='display min : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/17/2013
    def DisplayMax(self, output=None, attrib='display max : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/17/2013
    def ValUnits(self, output=None, attrib='value units : '):
        return self.attribOut(self.findIndex(attrib), output)
        self.updateDocFile()

    #Created 09/17/2013
    def ValError(self, output=None, attrib='value error : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def FlagValue(self, output=None, attrib='flag value  : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def FlagDef(self, output=None, attrib="flag def'n  : "):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def LegendCats(self, output=None, attrib='legend cats : '):
        return self.attribOut(self.findIndex(attrib), output)

    #Created 09/17/2013
    def Lineage(self, output=None, attrib='lineage     : '):
        lineageList = []
        for line in self.docLines:
            if line[0] == attrib:
                lineageList.append(line[1])
        return lineageList


#Created 10/07/2013    
class IdrisiFiles():

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
        
    #Convert input raster group files to list
    #Parameters:
    #inputfile - name of the input raster group file
    #directories - list of directories present in the
    #Lines 58-60 updated 9/15/2013
    def ReadRgf(self, filename, dirs=getDirectories()):
        filename = fixFile(filename,'rgf') 
        path = findFile(filename,'rgf', dirs) 
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
    def WriteRgf(self, directory, filelist, rgfname):
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

    def ReadAvl(self, inputavl, skipline1=True, dirs=getDirectories()):
        #Create .avl file of P/E ratio per Habitat Suitability value
        #Open created .avl file
        avlFile = findFile(inputavl, 'avl', dirs)
        if inputavl[-4:] != '.avl':
            inputavl = inputavl+'.avl'
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

    #Writes attribute documentation file
    #Values should be in embedded list format\
    #Created 10/04/2013
    def WriteAdc(self, directory, avlfile, values, datatype):
        file_name = fixFile(avlfile, 'adc')
        filePath = directory + file_name
        records = len(values)
        fields = len(values[0])
        raw_template = [['file format : ', 'IDRISI Values A.1'],\
                        ['file title  : ', ''],\
                        ['file type   : ', 'ascii'],\
                        ['records     : ', str(records)],\
                        ['fields      : ', str(fields)]]
        for i in range(fields):
            field_num = ['field %s     : '%(i)]
            if i == 0:
                field_num.append('idr_id')
                data_type = ['data type   :  ', 'integer']
            else:
                field_num.append('value%s'%(i))
                data_type = ['data type   : ', datatype.lower()]
            field_format = ['format      : ','0']
            val_num = [value[i] for value in values]
            val_min = min(val_num)
            val_max = max(val_num)
            min_value = ['min. value  : ', str(val_min)]
            max_value = ['max. value  : ', str(val_max)]
            min_display = ['display min : ', str(val_min)]
            max_display = ['display max : ', str(val_max)]
            field_template = [field_num, data_type,\
                              field_format, min_value, max_value,\
                              min_display, max_display,\
                              ['value units : ', 'identifiers'],\
                              ['value error : ', 'unknown'],\
                              ['flag value  : ', 'none'],\
                              ["flag def'n  : ", 'na'],\
                              ['legend cats : ', '0']]
            raw_template.extend(field_template)
        write_adc = open(filePath, 'w')
        for line in raw_template:
            write_adc.write('%s%s\n'%(line[0],line[1]))
        write_adc.close()

    #Writes attribute values and attribute documentation file to directory
    #Created 10/4/2013
    def WriteAvl(self, directory, avlfile, values, filetype):
        good_filetype = ['integer', 'real']

        try:
            good_filetype.index(filetype)
        except:
            "Warning: please insert valid file type (integer/real)."
            exit()
        
        file_name = fixFile(avlfile, 'avl')
        filePath = directory + file_name
        write_avl = open(filePath, 'w')
        for value in values:
            write_avl.write('%s %s\n'%(value[0], value[1]))
        write_avl.close()
        self.WriteAdc(directory,avlfile, values, filetype)

    def WriteRcl(self, rclname, directory, reclasslist):
        if rclname[-4:] != '.rcl':
            rclname = rclname+'.rcl'
        outputrcl = directory+rclname
        rclwrite=open(outputrcl, 'w')
        for row in reclasslist:
            rclwrite.write(str(row[0])+' '+str(row[1])+' '+str(row[2])+'\n')
        rclwrite.write('-9999')
        rclwrite.close()
        return outputrcl

IdrisiFiles = IdrisiFiles()
