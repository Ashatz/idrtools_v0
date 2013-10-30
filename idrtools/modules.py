from idrtools import *
from idrtools.idrexplorer import *
from idrtools.idrfiles import *
from sys import exit

class modules():

    def arcraster(self, conversion, input, output, integer=1, outref='latlong', outunit='deg', outdist=1):
        conversion=str(conversion)
        integer=str(integer)
        outdist=str(outdist)
        if conversion == '1':
            if output[-4:] != '.ftl':
                output=output+'.ftl'
            api.RunModule("ARCRASTER", '1*'+input+'*'+output, 1, '', '', '', '', 1)
        if conversion == '2':
            if output[-4:] != '.asc':
                output=output+'.asc'
            api.RunModule("ARCRASTER", '2*'+input+'*'+output, 1, '', '', '', '', 1)
        if conversion == '3':
            if input[-4:] != '.ftl':
                input=input+'.ftl'
            api.RunModule("ARCRASTER", '3*'+input+'*'+output+'*'+integer+'*'+outref\
                          +'*'+outunit+'*'+outdist, 1, '', '', '', '', 1)
        if conversion == '4':
            if input[-4:] != '.asc'and input[-4:] != '.txt':
                input=input+'.asc'
            api.RunModule("ARCRASTER", '4*'+input+'*'+output+'*'+integer+'*'+outref\
                          +'*'+outunit+'*'+outdist, 1, '', '', '', '', 1)

    def area(self, input, output, out_format, unit_type):
        unit_types = range(1,8)

        try:
            unit_types.index(unit_type)
        except:
            print "Warning: please input correct unit type."
            exit()

        api.RunModule("AREA", '%s*%s*%s*%s'%(input, out_format, unit_type, output), \
                      1, '', '', '', '', 1)
        
    def assign(self, input, avlfile, output):
        
        try:
            avl_test = findFile(avlfile, 'avl', getDirectories())
        except:
            print "Warning: Input Attribute Value File %s was not found!"%(avlfile)
            exit()

        api.RunModule("ASSIGN", '%s*%s*%s'%(input, output, avlfile), 1, '',\
                      '', '', '', 1)

    def Buffer(self, input, output, target_val, buffer_val, non_buff_val, buff_width):
        api.RunModule("BUFFER", '%s*%s*%s*%s*%s*%s'%(input, output, target_val, buffer_val,\
                                                     non_buff_val, buff_width),\
                      1, '', '', '', '', 1)
               
    def composite(self, blue, green, red, output, stretch='1', background='2', saturation='1', outType='3'):
        stretch=str(stretch)
        background=str(background)
        saturation=str(saturation)
        if stretch != '1':
            saturaton = '#'
        outTye=str(outType)
        api.RunModule("COMPOSITE", blue+'*'+green+'*'+red+'*'+output+'*'+stretch+'*'+\
                      background+'*'+saturation+'*'+outType, 1, '', '', '', '', 1)


    def contour(self, input, output, minimum, maximum, interval, generalize, background='n'):
        minimum=str(minimum)
        maximum=str(maximum)
        interval=str(interval)
        background=str(background)
        if background != 'n':
            api.RunModule("CONTOUR", '%s*%s*%s*%s*%s*%s*y*%s'%\
                          (input, output, minimum, maximum, interval, generalize, background)\
                          , 1, '', '', '', '', 1)
        else:
            api.RunModule("CONTOUR", '%s*%s*%s*%s*%s*%s*n'%\
                          (input, output, minimum, maximum, interval, generalize)\
                          , 1, '', '', '', '', 1)

    def distance(input, output):
        api.RunModule("DISTANCE", '%s*%s'%(input, output), 1, '', '', '', '', 1)

    def expand(self, input, output, magnitude):
        api.RunModule("EXPAND", '%s*%s*%s'%(input, output, magnitude), 1, '', '', '', '', 1)

    def extract(self, featinput, procinput, summarytype, outtype, output):
        summarytype = str(summarytype)
        outtype = str(outype)
        if outtype == '1':
            api.RunModule("EXTRACT", featinput+'*'+procinput+'*1*'+summarytype+'*'\
                          +output, 1, '', '', '', '', 1)
        if outtype == '2':
            api.RunModule("EXTRACT", featinput+'*'+procinput+'*3*'+summarytype+'*'\
                          +output, 1, '', '', '', '', 1)

    def genericraster(self, input, bands, output, format, interleaving, header_info, \
                      header_size, trailer, data_size, swap_byte, out_reference):
        format_dict = {'BIL':'1', 'BIP':'2', 'BSQ':'3'}
        if str(format).isdigit() != True:
            format = format_dict[str(format)]
        #Add file prefix if there are multiple bands
        if bands > 1:
            output = output+input
        if str(format) != '2':
            interleaving = '0'
        if type(out_reference) == str:
            project = IdrisiExplorer()
            dirlist = project.getProjectDirs()
            file = findFile(out_reference, 'rst', dirlist)
            doc = Documentation(file)
            ref_list = [doc.Columns(), doc.Rows(), doc.RefSystem(), doc.RefUnits(), doc.MinX(),\
                        doc.MaxX(), doc.MinY(), doc.MaxY(), doc.UnitDist()]
        if type(out_reference) == list:
            ref_list = out_reference
        if data_size == 'B' or data_size == 'N':
            swap_byte = 'N'

        if header_info == '0':   
            api.RunModule("GENERICRASTER", '%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s'%(input, bands, output, format, interleaving, header_info, \
                                                                                                 data_size, swap_byte, ref_list[0], ref_list[1], ref_list[2], \
                                                                                                 ref_list[3], ref_list[4], ref_list[5], ref_list[6], \
                                                                                                 ref_list[7], ref_list[8]), 1, '', '', '', '', 1)
        elif header_info == '3':
            api.RunModule("GENERICRASTER", '%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s'%(input, bands, output, format, interleaving, header_info, header_size, \
                                                                                                       trailer, data_size, swap_byte, ref_list[0], ref_list[1], ref_list[2], \
                                                                                                       ref_list[3], ref_list[4], ref_list[5], ref_list[6], \
                                                                                                       ref_list[7], ref_list[8]), 1, '', '', '', '', 1)
        else:
            api.RunModule("GENERICRASTER", '%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s'%(input, bands, output, format, interleaving, header_info, \
                                                                                                    header_size, data_size, swap_byte, ref_list[0], ref_list[1], ref_list[2], \
                                                                                                    ref_list[3], ref_list[4], ref_list[5], ref_list[6], \
                                                                                                    ref_list[7], ref_list[8]), 1, '', '', '', '', 1)
        
    def geotiff(self, process, input, output=input, palette='greyscale'):
        process = str(process)
        if process == '1':
            api.RunModule("GEOTIFF", process+'*'+input+'*'+output, 1,\
                          '', '', '', '', 1)
        if process == '2':
            api.RunModule("GEOTIFF", process+'*'+input+'*'+output+'*'\
                          +palette, 1, '', '', '', '', 1)

    def extract(self, featinput, procinput, summarytype, outtype, output):
        summarytype = str(summarytype)
        outtype = str(outype)
        if outtype == '1':
            api.RunModule("EXTRACT", featinput+'*'+procinput+'*1*'+summarytype+'*'\
                          +output, 1, '', '', '', '', 1)
        if outtype == '2':
            api.RunModule("EXTRACT", featinput+'*'+procinput+'*3*'+summarytype+'*'\
                          +output, 1, '', '', '', '', 1)

    def initial(self, output, outtype, outfile, value, define, definition):
        output = fixFile(output, 'rst')
        if str(define) == '1':
            definition = fixFile(definition, 'rst')
            rdc = Documentation(definition)
            api.RunModule("INITIAL", '%s*%s*%s*%s*%s*%s*%s'%(output, outtype, outfile, value, define, definition, rdc.RefUnits),\
                          1, '', '', '', '', 1)
        elif str(define) == '2':
            api.RunModule("INITIAL", '%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s'%(output, outtype, outfile, value, define,\
                                                                                     definition[0], definition[1], definition[2], \
                                                                                     definition[3], definition[4], definition[5], \
                                                                                     definition[6], definition[7], definition[8],\
                                                                                     definition[9])\
                          , 1, '', '', '', '', 1)

    def metaupdate(self, intype, input, option, value):
        intype = str(intype)
        option = str(option)
        value = str(value)
        if type(input) == 'list':
            api.RunModule("METAUPDTE", intype +'*'+input+'*'+option+\
                          '*'+str(value), 1, '', '', '', '', 1)
        else:
            list = [input]
            rgfName = input+'.rgf'
            #Create filepath for the trash directory
            dumpfile = dirlist[0]+'dump\\'
            #Create trash directory
            try:
                os.mkdir(dumpfile[:-1])
            except OSError:
                pass
            if intype == '1':
                filetype = 'rst'
            elif intype == '2':
                filetype = 'vct'
            rgfPath = findfile(input, filetype, dirlist)
            writeRgf(rgfPath, list, rgfName)
            api.RunModule("METAUPDTE", intype+'*'+input+'*'+option+\
                          '*'+value, 1, '', '', '', '', 1)
            shutil.move(rgfPath+rgfName, dumpfile+rgfName)
            shutil.rmtree(dumpfile)

    def ortho(self, surface, output, resolution, drape=False, palette=default_palette[0], direction='#',\
              angle='#', exaggeration='#', newmin='#', newmax='#'):
        project = IdrisiExplorer()
        dirlist = project.getProjectDirs()
        surface = findFile(surface, 'rst', dirlist)
        resolution = str(resolution)
        direction = str(direction)
        exaggeration=str(exaggeration)
        newmin=str(newmin)
        newmax=str(newmax)
        if drape==False:
            api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                          '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax, 1, ''\
                          , '', '', '', 1)
        else:
            filename = findFile(drape, 'rst', dirlist)
            fileRdc = Documentation(filename)

            if fileRdc.DataType() == 'RGB24':
                api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                              '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax+'*'+\
                              drape+'*'+palette, 1, '', '', '', '', 1)
            else:
                api.RunModule("ORTHO", surface+'*'+output+'*'+resolution+'*'+direction+\
                              '*'+angle+'*'+exaggeration+'*'+newmin+'*'+newmax+'*'+\
                              drape+'*'+palette, 1, '', '', '', '', 1)



    def overlay(self, input1, input2, output, operation):
        operation = str(operation)
        api.RunModule("OVERLAY", '%s*%s*%s*%s'%\
                      (operation, input1, input2, output), \
                      1 , '', '', '', '', 1)

    def pyramid(self, process, inputType, input):
        process = str(process)
        inputType = str(inputType)
        if inputType == '1' or inputType == '2':
            if inputType == '1':
                fileType = 'rst'
            elif inputType == '2':
                fileType = 'rgf'
            directory = findfile(input, inputType, dirlist)
            if directory != None:
                api.RunModule("PYRAMID", process+'*'+inputType+'*'\
                              +directory+input, 1, '', '', '', '', 1)
            else:
                api.RunModule("PYRAMID", process+'*'+inputType+'*'\
                              +input, 1, '', '', '', '', 1)
        else:
            print "Input filetype must be a raster image (1) or a raster" \
                  +" group file (2)."



    def random(self, input, output, datatype, distribution, maxint_mean, stdev = None):
        datatype = str(datatype)
        distribution = str(distribution)
        maxint_mean = str(maxint_mean)
        stdev = str(stdev)
        if stdev != None:
            api.RunModule("RANDOM", output+'*1*'+datatype+'*'+input+'*'+\
                            distribution+'*'+maxint_mean+'*'+stdev, 1, '', ''\
                            , '', '', 1)
        else:
            api.RunModule("RANDOM", output+'*1*'+datatype+'*'+input+'*'+\
                            distribution+'*'+maxint_mean, 1, '', '', '', '',\
                            1)


    def reclass(self, filetype, input, output, outtype, classtype, rclist):
        if filetype == 'rst':
            intype = 'i'
        if filetype == 'vct':
            intype = 'v'
        if filetype == 'avl':
            intype = 'a'
        
        try:
            intype in 'iva'
        except:
            print "Error, %s is not an appropriate file type."%(filetype)
            exit()
        
        classtype = str(classtype)
        if classtype == '1':
            print "Sorry not available yet."
            '''
            api.RunModule("RECLASS", '%s*%s*%s*%s*%s*%s*%s*%s'%\
                          (intype, input, output, 1, rclist[0], rclist[1], rclist[2], outtype)\
                          , 1, '', '', '', '', 1)
            '''
        if str(classtype) == '2':
            tmprcl = IdrisiFiles.WriteRcl('tmprcl', getDirectories()[0], rclist)
            api.RunModule("RECLASS", intype+'*'+input+'*'+output+'*3*'+tmprcl+'*'+str(outtype), \
                          1, '', '', '', '', 1)
        if classtype == '3':
            api.RunModule("RECLASS", intype+'*'+input+'*'+output+'*1*'+rclist+'*'+outtype,\
                          1, '', '', '', '', 1)

    def scalar(self, input, output, operation, number):
        operation = str(operation)
        number = str(number)
        api.RunModule("SCALAR", '%s*%s*%s*%s'%\
                      (input, output, operation, number), \
                      1, '', '', '', '', 1)

    def standard(self, input, output, mask=None):
        if mask != None:
            api.RunModule("STANDARD", input+'*'+output+'*'+mask, 1, '', '', '', '', 1)
        else:
            api.RunModule("STANDARD", input+'*'+output, 1, '', '', '', '', 1)

    #Added 10/12/2013
    def surface(self, operation, input, output, output2='#', slope='degrees', azimuth='315', elevation='30'):
        slope_dict = {'degrees':'d', 'percent':'p'}

        try:
            slope_input = slope_dict[slope]
        except:
            print "Warning, must input 'degrees' or 'percent' as acceptable slope measurements."
            exit()
            
        if str(operation) == '1':
            api.RunModule("SURFACE", '%s*%s*%s*%s*%s'%(operation, input, output, output2, slope_input), 1, '', '', '', '', 1)
        elif str(operation) == '2':
            api.RunModule("SURFACE", '%s*%s*%s*%s'%(operation, input, output, output2), 1, '', '', '', '', 1)
        elif str(operation) == '3':
            api.RunModule("SURFACE", '%s*%s*%s*%s%s'%(operation, input, output, output2, slope_input), 1, '', '', '', '', 1)
        else:
            if int(azimuth) > 360 or int(azimuth) <= 0:
                print "Warning, azimuth angles must be between 0-360 degrees."
                exit()
            elif int(elevation) > 90 or int(elevation) >= 0:
                print "Warning, solar elevation angles must be between 0-90 degrees."
                exit()
            else:
                api.RunModule("SURFACE", '%s*%s*%s*%s*%s'%(operation, input, output, azimuth, elevation), 1, '', '', '', '', 1)
                
    def toprank(self, input, output, ranktype, n_percent, mask='none', reverse='2', revoutput='N/A'):
        reverse=str(reverse)
        ranktype=str(ranktype)
        n_percent=str(n_percent)
        if ranktype == '2' and (int(n_percent) > 100 or int(n_percent) < 0):
            print "Please insert a valid percentage value (0-100)"
        else:
            if reverse == '1':
                api.RunModule("TOPRANK", input+'*'+mask+'*'+ranktype+'*'+\
                              n_percent+'*'+output+'*'+reverse+'*'+revoutput,\
                              1, '', '', '', '', 1)
            else:
                api.RunModule("TOPRANK", input+'*'+mask+'*'+ranktype+'*'+\
                              n_percent+'*'+output+'*'+reverse, 1, '', '',\
                              '', '', 1)

    def transform(self, input, output, transformation):
        options = range(1, 16)

        try:
            options.index(transformation)
        except:
            print "Warning, input transformation identifier %s not found."%(transformation)
            exit()
            
        api.RunModule("TRANSFORM", '%s*%s*%s'%(input, output, transformation), 1, '', '', '', '', 1)

modules = modules()
