'''
This script was produced by A.J. Shatz to carry out the Land Surface Temperature
calculation of the thermal band for Landsat 5 and 7 using the methods of Sobrino
et al. 2004, Jimemez-Munoz et al. 2009, and Liu and Zhang 2011.
'''

'''
v1.1 - A bug was fixed involving the creation of the at sensor brightness temperature image
such that values divided through overlay by 0 remain zero instead of undefined.
v1.2 - An input prefix was given to the model to allow users to save and view all outputs
seperately without having to overwrite them.
v2.0 - Module and class were renamed from JMS to jms.  These files are now located in
the site-packages folder and can be accessed easily via the python shell.  
'''

import os
import shutil
import math
from glob import glob
from idrtools import *


dumpfile = workdir+'\\dump\\'
try:
    os.mkdir(dumpfile[:-1])
except OSError:
    pass

class jms():       
    
    def __init__(self):
        #Radiosounding data derived from modtran for TIGR61
        TIGR61dict = {'TM':[[0.08735,-0.09553,1.10188],[-0.69188,-0.58185,-0.29887],[-0.03724,1.53065,-0.45476]]\
                      ,'ETM+':[[0.07593,-0.07132,1.08565],[-0.61438,-0.70916,-0.19379],[-0.02892,1.46051,-0.43199]]}
        sens = raw_input("Sensor (TM\ETM+)\n")
        senslist =  ['TM','ETM+']
        test1 = sens in senslist
        if test1 == False:
            print "Catastrophic Failure: Input valid sensor name!!!"
        else:
            therm = raw_input("Thermal band\n")
            if therm[-4:] != '.rst':
                therm2 = therm+'.rst'
            else:
                therm2 = therm
            test2 = therm2 in filelist
            if test2 == False:
                print "Catastrophic Failure: Thermal band input not found!!!"
            else:
                ndvi = raw_input("NDVI image\n")
                if ndvi[-4:] != '.rst':
                    ndvi2 = ndvi+'.rst'
                else:
                    ndvi2 = ndvi
                test3 = ndvi2 in filelist
                if test3 == False:
                    print "Catastrophic Failure: NDVI input not found!!!"
                else:
                    #input temperature in Celsius
                    temp = raw_input("Temperature (Celsius)\n")
                    if temp.isdigit == False:
                        print "Catastrophic Failure: Temperature must be a number between"+\
                              "1e-30 to 1e30"
                    else:
                        #percentage between 0-1   
                        hum = raw_input("Relative Humidity (0-1)\n")
                        if hum.isdigit == False:
                            print "Catastrophic Failure: Relative humidity must be a"+\
                                  "number from 0-1"
                        elif float(hum) > 1 or float(hum) < 0:
                            print "Catastrophic Failure: Relative humidity must in units"+\
                                  "of percent between 0-1"
                        else:
                            prefix = raw_output("Output file prefix\n")
                            output = raw_input("Output filename\n")
                            self.lst(TIGR61dict, sens, therm, ndvi, temp, hum, prefix, output)
        shutil.rmtree(dumpfile[:-1])


    #Calculating spectral radiance from DNs
    def radiance(self, sens, therm, prefix):
        output = workdir+prefix+'_L6_Lsen.rst'
        if sens == 'TM':
            api.RunModule("SCALAR", therm+'*'+dumpfile+'tmp001*3*1.4065', 1, '', '', '', '', 1)
            api.RunModule("SCALAR", dumpfile+'tmp001*'+dumpfile+'tmp002*4*255', 1, '', '', '',\
                          '', 1)
            api.RunModule("SCALAR", dumpfile+'tmp002*'+output+'*1*0.1238', 1, '', '', '', \
                          '', 1)
        elif sens == 'ETM+':
            api.RunModule("SCALAR", therm+'*'+dumpfile+'tmp001*3*1.704', 1, '', '', '', '', 1)
            api.RunModule("SCALAR", dumpfile+'tmp001*'+output+'*4*255', 1, '', '', '', '', 1)
        return output

    #Calculate at-sensor brightness temperature
    def Tsen(self, sens, therm, prefix):
        output = workdir+prefix+'_T6_Tsen.rst'
        rad = self.radiance(sens, therm, prefix)
        if sens == 'TM':
            K1 = 60.776
            K2 = 1260.56
        elif sens == 'ETM+':
            K1 = 66.609
            K2 = 1282.71
        api.RunModule("INITIAL", dumpfile+'tmp001*2*1*'+str(K1)+'*1*'+rad, 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '42*'+dumpfile+'tmp001*'+rad+'*'+dumpfile+'tmp002', 1, '',\
                      '', '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp002*'+dumpfile+'tmp003*1*1', 1, '', '', '', '',\
                      1)
        api.RunModule("TRANSFORM", dumpfile+'tmp003*'+dumpfile+'tmp004*2', 1, '', '', '', \
                      '', 1)
        api.RunModule("INITIAL", dumpfile+'tmp005*2*1*'+str(K2)+'*1*'+rad, 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '42*'+dumpfile+'tmp005*'+dumpfile+'tmp004*'+output, 1, '',\
                      '', '', '', 1)
        return output

    #Calculate gamma and delta
    def gamma_delta(self, sens, therm, prefix):
        output1 = workdir+prefix+'_Gamma' 
        output2 = workdir+prefix+'_Delta' 
        self.Tsen(sens, therm, prefix)
        if sens == 'TM':
            lamb = 11.457
        elif sens == 'ETM+':
            lamb = 11.269
        c1 = 11910.4
        c2 = 14387.7
        api.RunModule("SCALAR", 'L6_Lsen*'+dumpfile+'tmp001*3*'+str(c2), 1, '', '', '', '', 1)
        api.RunModule("SCALAR", 'T6_Tsen*'+dumpfile+'tmp002*5*2', 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '4*'+dumpfile+'tmp001*'+dumpfile+'tmp002*'+dumpfile+'tmp003', 1, '', \
                      '', '', '', 1)
        api.RunModule("SCALAR", 'L6_Lsen*'+dumpfile+'tmp004*3*'+str((lamb**4)/c1), 1, '', \
                      '', '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp004*'+dumpfile+'tmp005*1*'+str(lamb**-1), 1, '', \
                      '', '', '', 1)
        api.RunModule("OVERLAY", '3*'+dumpfile+'tmp003*'+dumpfile+'tmp005*'+dumpfile+'tmp006', 1, '', \
                      '', '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp006*'+output1+'*5*-1', 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '3*L6_Lsen*'+output1+'*'+dumpfile+'tmp007', 1, '', '', '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp007*'+dumpfile+'tmp008*3*-1', 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '1*T6_Tsen*'+dumpfile+'tmp008*'+output2, 1, '', '', '', '', 1)
        return output1, output2
    
    #Calculate emissivity
    def emissivity(self, ndvi, prefix):
        output = workdir+prefix+'_E6_Emissivity'
        api.RunModule("RECLASS", 'i*'+ndvi+'*'+dumpfile+'tmp001*2*0.995*-999*-0.185*0.97*'+\
                      '-0.185*0.157*0*0.157*0.727*0.990*0.727*999*-9999*2', 1, '', '', '', \
                      '', 1)
        api.RunModule("RECLASS", 'i*'+ndvi+'*'+dumpfile+'tmp002*2*0*-999*0.157*0*0.727*'+\
                      '999*-9999*2', 1, '', '', '', '', 1)
        api.RunModule("TRANSFORM", dumpfile+'tmp002*'+dumpfile+'tmp003*2', 1, '', '', '',\
                      '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp003*'+dumpfile+'tmp004*3*0.047', 1, '', '', \
                      '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp004*'+dumpfile+'tmp005*1*1.0094', 1, '', '', \
                      '', '', 1)
        api.RunModule("RECLASS", 'i*'+dumpfile+'tmp005*'+dumpfile+'tmp006*2*0*'+\
                      '-9999999999999999999*0.4*-9999*2', 1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '1*'+dumpfile+'tmp006*'+dumpfile+'tmp001*'+output, 1, '',\
                      '', '', '', 1)
        return output

    #Water vapor calculation (g/cm^2)
    def w(self, temp, hum):
        part1 = math.e**((17.27*float(temp))/(237.3+float(temp)))
        w = ((part1*6.108*float(hum))*0.0981)+0.1697
        return w

    #Calculate psi
    def Psi(self, dictionary, sens, number, temp, hum):
        water = self.w(temp, hum)
        coef = dictionary[sens][number-1]
        psi = ((water**2)*coef[0])+(water*coef[1])+coef[2]
        return psi

    def lst(self, dictionary, sens, therm, ndvi, temp, hum, prefix, output):
        gamdelt = self.gamma_delta(sens, therm, prefix)
        em = self.emissivity(ndvi)
        psi1 = self.Psi(dictionary, sens, 1, temp, hum)
        psi2 = self.Psi(dictionary, sens, 2, temp, hum)
        psi3 = self.Psi(dictionary, sens, 3, temp, hum)
        api.RunModule("SCALAR", em+'*'+dumpfile+'tmp001*5*-1', 1, '', '', '', '', 1)
        api.RunModule("SCALAR", 'L6_Lsen*'+dumpfile+'tmp002*3*'+str(psi1), 1, '', '',\
                      '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp002*'+dumpfile+'tmp003*1*'+str(psi2), 1, '', '',\
                      '', '', 1)
        api.RunModule("OVERLAY", '3*'+dumpfile+'tmp001*'+dumpfile+'tmp003*'+dumpfile+\
                      'tmp004', 1, '', '', '', '', 1)
        api.RunModule("SCALAR", dumpfile+'tmp004*'+dumpfile+'tmp005*1*'+str(psi3), 1, '', '',\
                      '', '', 1)
        api.RunModule("OVERLAY", '3*'+dumpfile+'tmp005*'+gamdelt[0]+'*'+dumpfile+'tmp006', \
                      1, '', '', '', '', 1)
        api.RunModule("OVERLAY", '1*'+dumpfile+'tmp006*'+gamdelt[1]+'*'+output, \
                      1, '', '', '', '', 1)
        api.DisplayFile(output, 'quant')

jms()
