'''
This script was designed by Andrew Shatz with the help of Dylan Broderick to
test the consistency of a resampled Species Distribution Model using the Boyce
Continuous Index. This script was originally created on 
'''

#Import string and Idrisi COM server
from idrtools import *
from idrtools.idrfiles import *
from idrtools.modules import modules
import os
import shutil
import numpy as np
from scipy.stats import spearmanr, norm #Edited 10/9/2013
from glob import glob
import csv
import math

#Create filepath for the trash directory
project = IdrisiExplorer()
workdir = project.workdir
dirlist = project.dirlist
dumpfile = workdir+'dump\\'
#Create trash directory
try:
    os.mkdir(dumpfile[:-1])
except OSError:
    pass

dirlist.append(dumpfile)

class bcindex():
    
    def __init__(self):
        hsmRgf = raw_input("Input SDM Raster Group File\n") 
        validRgf = raw_input("Insert Validation Raster Group File\n")
        saMask = raw_input("Insert mask file (.rst)\n")
        bias = raw_input("Does a bias file exist (True or False)?\n")
        if bias == "True":
            biasfile = raw_input("Insert Bias File\n")
        else:
            biasfile = 'N/A'
        initial = dumpfile+'Blank'
        api.RunModule('INITIAL', initial+'*2*1*0*1*'+saMask, \
                      1, '', '', '', '', 1)
        bclass = raw_input("Determine Number of Boyce Classes\n")
        bwindow = raw_input("Determine Window Size (number of classes)\n")
        confint = raw_input("Determine Confidence Interval (90, 95, or 99)\n")
        peFilePrefix = raw_input('Determine PE File Prefix\n')
        self.BoyceContIndex(hsmRgf, validRgf, saMask, biasfile, bclass, bwindow, confint, initial,\
                            peFilePrefix)
        shutil.rmtree(dumpfile)

    def totalValid(self, validation, initial):
        validsum = initial
        sumfile1 = dumpfile+'validtotal'
        #Sum all validation images together
        for i in range(len(validation)):
            api.RunModule('OVERLAY', '1*'+validsum+'*'+ validation[i]+'*'+\
                          sumfile1+str(i+1), 1, '', '', '', '', 1)
            validsum = sumfile1+str(i+1)
        #Produce .avl file of of total validation points
        api.RunModule('EXTRACT', initial+'*'+ validsum \
                      + '*1*3*'+sumfile1, 1, '',\
                      '', '', '', 1)
        total = readAvl('validtotal', dirlist, False)
        return total
        

    #Function to produce boyce threshold image
    #Parameters:
    #input - Raw habitat suitability image; mahalList[i]
    #threshold - user identified thresholds/classes; thresh
    #output - Boyce threshold image
    #initial - Blank image created using initial; initial
    def BoyceImage(self, hsmImage, bclass, mask):
        #Calculate maximum HSM value
        if hsmImage[-4] == '.':
            hsmImage = hsmImage[:-4]
        readRdc = open(workdir+hsmImage+'.RDC', 'r')
        maxtest = readRdc.readlines()
        maxline = [maxtest[16]]
        maximum = float(maxline[0].split()[-1])
        rclfile = dumpfile+'Boyce_'+bclass+'.RCL'
        writeRclFile = open(rclfile, 'w')
        width = maximum/int(bclass)
        trange = range(1,int(bclass))
        i = 1
        #First line of .rcl file must be written as '0 -99999 0' to remove
        #influence of assigned background values
        writeRclFile.write('0 -99999 0\n')
        #Second line of .rcl file must be written as '1 0 0.01'
        writeRclFile.write('1 0 ' + str(width) + '\n')
        #Write reclass values for Boyce classes 2-99
        while i < len(trange):
            low = i * width
            high = low + width
            torcl = str(trange[i]) + ' ' + str(low) + \
                    ' ' + str(high) + '\n'
            writeRclFile.write(torcl)
            i = i + 1
        #Write reclass values for Boyce class 100
        writeRclFile.write(str(bclass) + ' ' + str(maximum - width) + \
                   ' ' +'999\n')
        writeRclFile.write('-9999')
        writeRclFile.close()
        api.RunModule('RECLASS', 'i*' + hsmImage + '*'+dumpfile+\
                      'tmp001*3*' + rclfile + '*1',  1, '', '', '', '', 1)
        bclassImage = dumpfile+'BClass_'+bclass
        api.RunModule('OVERLAY', '3*'+dumpfile+'tmp001*'+mask+'*'+\
                      bclassImage, 1, '', '', '', '', 1)
        return bclassImage

    #Extract information about proportion of presence and area for each defined
    #Boyce class produced from the BoyceImage function above
    #Parameters:
    #bclassImage - HSM image converted from 1 to bclass
    #inputImage - the image from which information is extracted (e.g. Validation
    #or mask)
    #bclass - the number of classes to threshold the HSM image into
    def PEreadAvl(self, bclassImage, inputImage, bclass):
        #Create .avl file of P/E ratio per Habitat Suitability value
        output =  dumpfile+inputImage
        api.RunModule('EXTRACT', bclassImage+'*'+inputImage+'*1*'+\
                      '3*'+output, 1, '', '', '', '', 1)
        if inputImage[-4:] == '.rst':
            inputImage = inputImage[:-4]
        outlist = readAvl(inputImage, [dumpfile])
        return outlist

    def peCalculation(self, hsmImage, validation, mask, biasfile, bclass, window, peImage):
        #List of habitat suitability window image files
        bclassImage = self.BoyceImage(hsmImage, bclass, mask)
        peList = [-999]*int(bclass)
        
        hsmPF = self.PEreadAvl(bclassImage, validation, bclass)
        totalVal = 0.0
        if biasfile != 'N/A':
            hsmEF = self.PEreadAvl(bclassImage, biasfile, bclass)
        else:
            hsmEF = self.PEreadAvl(bclassImage, mask, bclass)
        totalArea = 0.0
        for i in range(int(bclass)):
            totalVal = totalVal + hsmPF[i]
            totalArea = totalArea + hsmEF[i]
        for i in range(int(bclass)):
            hsmPF[i] = hsmPF[i]/totalVal
            hsmEF[i] = hsmEF[i]/totalArea
        wpeList = []
        for i in range(int(bclass)-int(window)+1):
            wpf = 0.0
            wef = 0.0
            for j in range(i, i + int(window)):
                wpf = wpf + hsmPF[j]
                wef = wef + hsmEF[j]
            wpeList.append(wpf/wef)
        for i in range(int(bclass)):
            if i < int(window)-1:
                delpe = wpeList[0:i+1]
                peList[i] = np.mean(delpe)
            if int(window)-1 <= i < int(bclass)\
               -int(window)+1:
                delpe = wpeList[i-(int(window)-1):i+1]
                peList[i] = np.mean(delpe)
            if int(bclass)-int(window)+1 <= i < int(bclass):
                delpe = wpeList[i-int(window)+1:int(bclass)-int(window)+1]
                peList[i] = np.mean(delpe)
        rclfilename = dumpfile+'_PE_'+bclass+'.rcl'
        percl = open(rclfilename, 'w')
        for i in range(int(bclass)):
            percl.write('%s %s %s\n' % (str(peList[i]), str(i+1), str(i+2)))
        percl.write('-9999')
        percl.close()
        api.RunModule('RECLASS', 'i*'+bclassImage+'*'+peImage\
                      +'*3*'+rclfilename+'*2', 1, '', '', '', '',1)
        return peList, peImage


    def sumStats(self, pelistgroup, bclass, confint):
        outputMatrix = [["Boyce Class", "Mean", "Median", "Range", "Lower Bound", "Upper Bound"]]
        convertMatrix = []
        header = [["Mean", "Median", "Range", "Lower Bound", "Upper Bound"]]
        for i in range(len(pelistgroup[0])):
            tempList = []
            for list in pelistgroup:
                tempList.append(list[i])
            convertMatrix.append(tempList)
        for i in range(len(convertMatrix)):
            average = np.mean(convertMatrix[i])
            median = np.median(convertMatrix[i])
            convertMatrix[i].sort()
            ran = convertMatrix[i][-1] - convertMatrix[i][0]
            sterr = np.std(convertMatrix[i])/math.sqrt(len(convertMatrix[i]))
            alpha = float(confint)/100
            lbound = stats.norm.interval(alpha, average, sterr)[0]
            if lbound < 0:
                lbound = 0
            ubound = norm.interval(alpha, average, sterr)[1] #Edited 10/9/2013
            outputMatrix.append([str(i+1), average, median, ran, lbound, ubound])
        return convertMatrix, outputMatrix

    #Write both summary text file and csv file for graphing.  The latter graph can be plotted using
    #either microsoft excel or 
    def writeOutputFiles(self, prefix, bciList, totalPO, bciOverall, bclass, sumstats):
        txtOutput = workdir + prefix+' Boyce Continuous Index Results.txt'
        writeTxt = open(txtOutput,'w')
        writeTxt.write("Boyce Continuous Index Results\n")
        writeTxt.write("\n")
        writeTxt.write("%-20s %9s\n" % ('K-Fold Partitions: ', str(len(bciList))))
        writeTxt.write("%-20s %9s\n" % ('Presence Only Sites:', str(totalPO)))
        writeTxt.write("\n")
        writeTxt.write("***************************************************\n")
        writeTxt.write("\n")
        writeTxt.write("%-20s %20s\n" % ('K-Fold Partition', 'Boyce Continuous Index'))
        writeTxt.write("\n")
        for i in range(len(bciList)):
            if bciList[i] > 0:
                writeTxt.write("%-20s %22.4s\n" % ('Partition ' + str(i+1)+':', bciList[i]))
            elif bciList[i] < 0:
                writeTxt.write("%-20s %22.5s\n" % ('Partition ' + str(i+1)+':', bciList[i]))
        writeTxt.write("\n")
        writeTxt.write("***************************************************\n")
        writeTxt.write("\n")
        if bciOverall > 0:
            writeTxt.write("%-20s %22.5s\n" % ('Overall Boyce Index:', str(bciOverall)))
        elif bciOverall < 0:
            writeTxt.write("%-20s %22.5s\n" % ('Overall Boyce Index:', str(bciOverall)))
        #Qualitative model assessment
        if bciOverall <= -0.5:
            writeTxt.write("%-20s %22s" % ('Model Quality:', 'Very Poor'))
        if -0.5 < bciOverall < -0.1:
            writeTxt.write("%-20s %22s" % ('Model Quality:', 'Poor'))
        if -0.1 <= bciOverall <= 0.1:
            writeTxt.write("%-20s %22s" % ('Model Quality:', 'Random'))
        if 0.1 < bciOverall < 0.5:
            writeTxt.write("%-20s %22s" % ('Model Quality:', 'Good'))
        if bciOverall >= 0.5:
            writeTxt.write("%-20s %22s" % ('Model Quality:', 'Very Good'))
        writeTxt.close()
        csvOutput = workdir + prefix+" Boyce Continuous Index Chart.csv"
        writeCsv = open(csvOutput, 'wb')
        writer = csv.writer(writeCsv)
        for row in sumstats:
            del(row[3])
            writer.writerow(row)
        writeCsv.close()
                                               
    def BoyceContIndex(self, hsmRgf, validRgf, saMask, biasfile, bclass, bwindow, confint, initial, prefix):
        hsmList = readRgf(hsmRgf, dirlist)
        validList = readRgf(validRgf, dirlist)
        bciResults = []
        peListFull = []
        outputlist = []
        maxlist = []
        totalPO = self.totalValid(validList, initial)
        for i in range(len(hsmList)):
            hsmClass = dumpfile+"HSM_B"+str(bclass)+'_'+str(i+1)
            peFileName = 'BCI_PE_'+str(i+1)
            outputPE = prefix+'_'+peFileName+'_'+bclass+'_'+bwindow
            peList = self.peCalculation(hsmList[i], validList[i], saMask, biasfile, bclass, bwindow, outputPE)[0]
            peListFull.append(peList)
            outputlist.append(outputPE)
            bciResults.append(spearmanr(peList, range(1,int(bclass)+1))[0])
            readRdc = open(workdir+outputlist[i]+'.RDC', 'r')
            rdc = readRdc.readlines()
            maxline = [rdc[16]]
            tempmax = float(maxline[0].split()[-1])
            maxlist.append(tempmax)
        maxlist.sort()
        maximum = str(maxlist[-1])
        rgfname = prefix+'_BCI_PE_'+bclass+'_'+bwindow+'.rgf'
        writeRgf(workdir, outputlist, rgfname)
        api.RunModule("TSTATS", '11*'+rgfname+"*"+rgfname[:-4]+"*0*"+maximum+"*0*"\
                      +str(len(bciResults)), 1, '', '', '', '', 1)
        api.DisplayFile(rgfname[:-4]+"_Mean", 'quant')
        api.DisplayFile(rgfname[:-4]+"_Median", 'quant')
        bciOverall = np.mean(bciResults)
        sumstatslist  = self.sumStats(peListFull, bclass, confint)
        self.writeOutputFiles(prefix, bciResults, totalPO, bciOverall, bclass, sumstatslist[1])

if __name__ == '__main__':
    bcindex()
