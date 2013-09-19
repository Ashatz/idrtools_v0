import win32com.client
import os
from glob import glob
import re

try: #
        api = win32com.client.Dispatch("idrisi32.IdrisiAPIServer")
except: #
        print "Error: please install an appropriate version of pywin32." #
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

#Set default palette for file display
palette = 'quant'

#Sort files based upon Idrisi-specific sorting properties
def sortFile(list):
        numPair=[]
        newList = [file[:-4] for file in list if file[-5].isdigit() == True]
        for file in newList:
                i = len(file)-1
                while i >= 0:
                        if file[i].isdigit()==True:
                                i -=1
                        else:
                                break
                numPair.append((int(file[i+1:]),file[:i+1]))
        numDict = {}
        for item in numPair:
                keylist = numDict.keys()
                if item[1] in keylist:
                        numDict[item[1]].append(item[0])
                else:
                        numDict[item[1]] = [item[0]]
        i = len(numDict)-1
        while i >= 0:
                if len(numDict.values()[i]) <=1:
                        del(numDict[numDict.keys()[i]])
                i -= 1
        [numDict[item].sort() for item in numDict]
        for item in numDict:
                searchFile = item+str(numDict[item][0])
                for i in range(len(list)):
                        if list[i][:-4] == searchFile:
                                filetype = list[i][-4:]
                                j=i
                                k=0
                                for j in range(j, j+len(numDict[item])):
                                        list[j] = item+str(numDict[item][k])+filetype
                                        k += 1
                                i = i+len(numDict[item])

#List files in a chosen working or resource directory according to filetype
def listFile(dir, wildcard='', case=True, filetype=\
                ['rst', 'rgf','vct', 'vlx','vgf']):
        list = []
        os.chdir(dir)
        tmplist = glob('*')
        for file in tmplist:
                if file[-3:].lower() in filetype:
                        list.append(file)
                else:
                        continue
        sortDict = {}
        for file in list:
                upperFile = file.upper()
                sortDict[upperFile] = file
        outlist = []
        upperKey = sortDict.keys()
        upperKey.sort()
        sortFile(upperKey)
        [outlist.append(sortDict[file]) for file in upperKey]
        if wildcard != '':
                newOutlist = []
                if case == False:
                        wildcard = wildcard.upper()
                        for file in upperKey:
                                if re.findall(wildcard, file) == [wildcard]:
                                        newOutlist.append(sortDict[file])
                                else:
                                        continue
                for file in outlist:
                        if re.findall(wildcard, file) == [wildcard]:
                                newOutlist.append(file)
                        else:
                                continue
                return newOutlist
        else:
                return outlist



