import os
from glob import glob
import re
from sys import exit
from shutil import rmtree, move

from idrtools import *

project_folder = os.path.dirname(__file__)+'\\Projects\\'
default_project = 'default'
current_project = ["CTA_Intensity"]

def listProjects(): #Created 9/25/2013
        os.chdir(project_folder)
        projList = [project[:-4] for project in glob('*.env')]
        return projList

projects = listProjects()#Created 10/01/2013

def getCurrentProject(project=current_project[0]):
        return current_project[0]

def setCurrentProject(project=current_project[0]):
        path = os.path.dirname(__file__)+'\\idrexplorer.py'
        read_init_ = open(path, 'r')
        lines = read_init_.readlines()
        read_init_.close()
        #Changed 10/2/2013
        for line in lines:
                if line[:18] == 'current_project = ':
                        new_line = lines[lines.index(line)][:18]+'["%s"]\n'%(project)
                        lines[lines.index(line)] = new_line               
        write_init_ = open(path, 'w')
        for line in lines:
                write_init_.write(line)
        write_init_.close()
        current_project[0] = project

def openNewProject(path): #Created 9/26/2013
        if path[-1] == '\\':
                path = path[:-1]
        projName = path.split('\\')
        fileName = projName[-1]+'.env'
        projPath = project_folder+fileName
        projWrite = open(projPath, 'w')
        projWrite.write(path+'\\')
        projWrite.close()
        projects.append(projName[-1]) #Added 10/01/2013
        projects.sort()
        setCurrentProject(projName[-1])

#Added 11/15/2013
def renameCurrentProject(proj_name, project = current_project[0]):
        if proj_name[-4:] == '.env':
                proj_name = proj_name[:-4]
        os.rename(project_folder+project+'.env', project_folder+proj_name+'.env')
        projects[projects.index(project)] = proj_name
        current_project[0] = proj_name
        

#Updated 10/22/2013       
def removeProject(project):
        os.chdir(project_folder)
        if project == current_project[0]:
                print "Warning: unable to remove currently active project."
        else:
                if project in projects:
                        del(projects[projects.index(project)])
                        dump = addDumpDir(project_folder)
                        project += '.env'
                        move(project_folder+project, dump+project)
                        removeDumpDir(dump)
                else:
                        print "Warning: input project does not exist."

#Necessary failsafe for starting idrtools - Divert project to default or create default
#project if removed
if current_project[0] not in projects:
        print "Warning: current project path not found...redirecting to default project path."
        if default_project not in projects:
                openNewProject('C:\Users\Public\Documents\IDRISI Tutorial Data\Using Idrisi')
                renameCurrentProject(default_project, current_project[0])
                setCurrentProject(default_project)
        else:
               setCurrentProject(default_project) 
        
################################################################################
'''
Dear Hao,

Please check out the validity of these functions using the built-in
api methods.  The methods within these functions were copied from page
9 of the IDRISI API document.  There was some confusion surrounding
the actual names of the methods, for they were not entirely clear within
the document.  Please let me know how the testing for these methods goes

Thank you very much, and I wish you all the best,

A.J.
'''

def openNewProject2(project):
        project_path = project_folder+project+'.env'
        api.OpenProjectFromFile(project)

def getCurrentProject2():
        return api.Get_CurrentProjectFileName()

def setCurrentProject2(project):
        project_path = project_folder+project+'.env'
        api.Set_CurrentProjectFileName(project_path)

def setDefaultProject(project):
        project_path = project_folder+project+'.env'
        api.Set_DefaultProjectFileName(project_path)#There is some confusion on p9 of the Idrisi API Document

def setDefaultProject2(project):
        project_path = project_folder+project+'.env'
        api.SetDefaultProjectFile(project_path)


################################################################################        
        
#Added 10/3/2013
###
filters = ['rst', 'rgf','tsf', 'vct', 'vlx','vgf']

def addFileType(filetype):
        if type(filetype) == str:
                filters.append(filetype)
        elif type(filetype) == list: #Added 10/10/2013
                filters.extend(filetype)
        filters.sort()

def removeFileType(filetype):
        if type(filetype) != list: #Added 10/10/2013
                filetype = [filetype]
        for file_type in filetype:
                try:
                        i = filters.index(file_type)
                except:
                        print 'Warning: Input file type %s is not active.'%(file_type)
                        exit()
                del(filters[i])
###


#This class allows for the creation of Idrisi Project Objects

class IdrisiExplorer(): #Created 9/26/2013
        

        def __init__(self, project = current_project[0]):
                if project != getCurrentProject():
                        setCurrentProject(project)

                self.project_path = project_folder+project+'.env' #Updated 10/04/2013
                try:
                        read_project = open(self.project_path, 'r')
                except:
                        print "Warning: Project file path %s does not exist."%(self.project_path)
                        exit()
                        
                self.dirlist = [lines[:-1] for lines in read_project.readlines()]
                self.workdir = self.dirlist[0]
                if len(self.dirlist) > 1:
                        self.resdirs = self.dirlist[1:]
                else:
                        self.resdirs = []
                read_project.close()                

        def getWorkingDir(self): #Created 10/1/2013
                return self.workdir

        def setWorkingDir(self, path): #Created 10/01/2013
                if path[-1] != '\\':
                        path += '\\'
                api.SetWorkingDir(path)
                self.workdir = path
                self.dirlist[0] = self.workdir
                

        def getResourceDirs(self): #Created 10/1/2013
                return self.resdirs

        def getProjectDirs(self):
                return self.dirlist

        def updateEnv(self, dirlist):
                write_project = open(self.project_path, 'w')
                for dir in dirlist:
                        write_project.write(dir+'\n')
                write_project.close()                

        def addResourceDir(self, path): #Created 10/01/2013
                if path[-1] != '\\':
                        path += '\\'
                api.AddResourceDirToProject(path)
                self.dirlist.append(path)
                self.resdirs = self.dirlist[1:]
                self.updateEnv(self.dirlist)

        def remResourceDir(self, path): #Created 10/01/2013
                if path[-1] != '\\':
                        path += '\\'
                api.RemoveResourceDirFromProject(path)
                api.SaveProjectToFile(self.project_path)
                del(self.dirlist[self.dirlist.index(path)])
                self.resdirs = self.dirlist[1:]                
                self.updateEnv(self.dirlist)
                
        def remAllResourceDir(self): #Created 10/01/2013
                api.RemoveAllResourceDirs()
                api.SaveProjectToFile(self.project_path)
                self.dirlist = [self.workdir]
                self.resdirs = []
                self.updateEnv(self.dirlist)
                
        #Sort files based upon Idrisi-specific sorting properties
        def sortFile(self, list):
                file_list = []
                file_keys = []
                #Added 10/10/2013
                for file in list:
                        #Select files with number characters before file extension name.
                        #Index 1 (i_1) marks the location of the period.
                        i_1 = file.find('.')
                        if file[i_1-1].isdigit() == True:
                                #Index 2 marks the location of the first iteration number, or Index 1 - 1
                                i_2 = i_1-1
                                while i_2 >= 0:
                                        if file[i_2].isdigit() == True:
                                                i_2 -= 1
                                        else:
                                                i_2 += 1
                                                break
                                #Create embedded list with file name, iteration number, and extension
                                file_list.append([file[:i_2],int(file[i_2:i_1]),file[i_1:]])
                                if file[:i_2] not in file_keys:
                                        file_keys.append(file[:i_2])
                        else:
                                #Create embedded list with file name and extension
                                file_list.append([file[:i_1], '', file[i_1:]])
                                #Save the base file names in a key list for later reference
                                if file[:i_1] not in file_keys:
                                        file_keys.append(file[:i_1])

                #Stores all sorted file names that are sorted by iteration and joined
                file_output = []
                for key in file_keys:
                        #Store files with identical file key names
                        temp_sort = [file for file in file_list if file[0] == key]
                        #Stores iteration values within files above 
                        temp_iter = [file[1] for file in temp_sort if file]
                        #Create temporary integer place holder for '' iteration numbers.
                        for i in range(len(temp_iter)):
                                if temp_iter[i] == '':
                                        temp_iter[i] = 0
                        temp_iter.sort()
                        #Replace old iteration values with new sorted iteration values
                        for i in range(len(temp_sort)):
                                #Return original '' value to placeholder
                                if temp_iter[i] == 0:
                                        temp_iter[i] = ''
                                temp_sort[i][1] = str(temp_iter[i])
                                file_output.append(''.join(temp_sort[i]))
                return file_output
                
        #List files in a chosen working or resource directory according to filetype
        def ListFile(self, dir, wildcard='', case=True, filetype=filters):
                os.chdir(dir)
                tmplist = glob('*')
                #Create list of filenames according to the filter
                file_list = [file for file in tmplist if file[file.find('.')+1:].lower() in filetype]
                sortDict = {}
                for file in file_list:
                        upperFile = file.upper()
                        sortDict[upperFile] = file
                outlist = []
                upperKey = sortDict.keys()
                upperKey.sort()
                output = self.sortFile(upperKey)
                #Reformat output file list from upper case to input default
                [outlist.append(sortDict[file]) for file in output]
                #Under circumstances of wildcards...
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

        def DisplayFileList(self, file_list):
                print '%-6s%s'%('Index','File name')
                for i in range(len(file_list)):
                        print '%-6s%s'%(str(i),file_list[i])

        def ListAllFiles(self):
                dirlist = self.dirlist
                list_file = []
                [list_file.append(self.ListFile(dir)) for dir in dirlist]
                return list_file
