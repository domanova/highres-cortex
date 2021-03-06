#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright CEA (2014).
# Copyright Université Paris XI (2014).
#
# Contributor: Olga Domanova <olga.domanova@cea.fr>.
#
# This file is part of highres-cortex, a collection of software designed
# to process high-resolution magnetic resonance images of the cerebral
# cortex.
#
# This software is governed by the CeCILL licence under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/or redistribute the software under the terms of the CeCILL
# licence as circulated by CEA, CNRS and INRIA at the following URL:
# <http://www.cecill.info/>.
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the licence, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of scientific
# software, that may mean that it is complicated to manipulate, and that
# also therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL licence and that you accept its terms.


# an example how to run this script
#od_batchMainCorticalColumns_ExtrProfiles.py  

# this is the main script to run on a classified GW volume
# it launches scripts by Yann Leprince: dist, heat, isovolume, column-regions to compute 'cortical columns'

from soma import aims, aimsalgo
from scipy.stats import mode
import sys, glob, os, subprocess, sys, time, timeit
import numpy as np
from optparse import OptionParser
import highres_cortex.od_cutOutRois

#read in the path and the directory
brainvisa_raw_niftis = '/neurospin/lnao/dysbrain/raw_niftis/'
pathToTextures = '/neurospin/lnao/dysbrain/randomized_flipped_data/manual_work/'
patientID = None              # subject000
realSide = 'L'
hemisphere = 'left'

realPatientID = None  # ac140155
pathToClassifFile = None #'/volatile/od243208/brainvisa_manual/%s/GWNoInnerSulciSkel_%s_%s.nii.gz' %(realPatientID, realPatientID, realSide)
pathToT2File = None
data_directory = None
keyWord = None
eliminateSulci = False
pathToSulciFile = None
cutOut = False           # perform Voronoi on the seeds from the labelled texture and apply Yann's methods on the cut out region
toT2 = False           # transform volumes to T2 space or not. Recently decided to perform this transformation after Voronoi and subtracting sulci skeletons
workOnLaptop = False
workOnT1inT2Space = False
numberOfIt = 3   # number of iterations to extend (dilate) the selected regions

#listOfSubjects = ['ac140159']
#listOfSubjects = ['ad140157']
#listOfSubjects = ['ac140159', 'ad140157']

########################################## full list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###########################################
#listOfSubjects = ['md140208', 'at140353', 'js140266', 'lg140146', 'he140338', 'cb140330', 'ac140159', 'js140311', 'ad140157', 'ag140439', 'sg140335', 'fg140290', 'af140169', 'ml140175']
################################################################################################################################

# list of subjects where both hemispheres were completely processed
listOfSubjects = ['js140311', 'ad140157', 'ag140439', 'sg140335', 'fg140290', 'af140169', 'ml140175', 'at140353']


# subjects not fully processed (not both hemispheres, or...)    
#['md140208', 'js140266', 'lg140146', 'he140338', 'cb140330', 'ac140159']


#listOfSubjects = ['cb140330']
hemispheres = ['L', 'R']
#hemispheres = ['L']
#hemispheres = ['R']

# diameters of cortical columns to work with
#diams = [1, 3, 5, 7, 9]
diams = [3]

# file to monitor comparison of the old and of the new heat calculation method
#heatCompareFile = open('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/heatCompareFile.txt', 'w')

for p in listOfSubjects:
    print '---------------------------------------------------------------------------------------------- '
    print 'start with subject ', p
    
    for s in hemispheres:
        
        print 'start with hemisphere ', s
        
        # 1. run the main cortical columns script for CUT volumes, 
        #print 'run the main cortical columns script for CUT volumes for NEW DB using old heat equation!!!'
        #subprocess.check_call(['/volatile/od243208/brainvisa_sources/highres-cortex/bin/od_mainCorticalColumns_newDB.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It_NewDB/' %(p, p), '-e', '-r', '-c', '-g', 'old'])


        #print 'run the main cortical columns script for CUT volumes for NEW DB using NEW heat equation!!!'
        #subprocess.check_call(['/volatile/od243208/brainvisa_sources/highres-cortex/bin/od_mainCorticalColumns_newDB.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It_NewDB/' %(p, p), '-e', '-r', '-c', '-g', 'new'])


        #############################################################################################################################################################
        ## TODO! delete it after the validation of the new heat calculation method!
        #volsHeatOld = glob.glob('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It_NewDB/heat/heat_%s_%s_cut_noSulci_extended.nii.gz' %(p, p, p, s))
        #volsHeatNew = glob.glob('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It_NewDB_NewHeat/heat/heat_%s_%s_cut_noSulci_extended.nii.gz' %(p, p, p, s))
        #if ((len(volsHeatOld) == 1) & (len(volsHeatNew) == 1)):
            #volHeatOld = aims.read(volsHeatOld[0])        
            #volHeatNew = aims.read(volsHeatNew[0])     
            #arrHeatOld = np.array(volHeatOld, copy = False)
            #arrHeatNew = np.array(volHeatNew, copy = False)
            #diffM = np.max(np.abs(arrHeatOld - arrHeatNew * 200))
            #print diffM
            #heatCompareFile.write('Subject %s, side %s, maxDiff between heat methods %s \n' %(p, s, str("%.4f" % diffM)))
        #else:
            #print 'len(volsHeatOld) = ', len(volsHeatOld), ' , len(volsHeatNew) = ', len(volsHeatNew)
        #############################################################################################################################################################

        
        ## 2. run the main cortical columns script for FULL volumes, 
        #print 'run the main cortical columns script for FULL volumes'
        #subprocess.check_call(['od_mainCorticalColumns.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsNew/' %(p, p), '-e', '-r'])
        
        # TODO! delete it later!! added to re-calculate cortical columns of various diameter. After Yann's correction
        #subprocess.check_call(['python', 'od_column-regionsMain.py', '-i',  '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It/dist/classif_with_outer_boundaries_%s_%s_cut_noSulci_extended.nii.gz' % (p, p, p, s), '-d',  '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It/' %(p, p), '-k', '%s_%s_cut_noSulci_extended' % (p,s), '-j', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/%s_T1inT2_ColumnsCutNew20It/GWsegm_%s_%s_cut_noSulci_extended.nii.gz %' (p, p, p, s)])
        
        ## 3. test whether the selected region growing was enough
        #print 'test whether the selected region growing was enough'
        #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_testExtendVoronoiParams.py', '-p', p, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/', '-s', s])
                
        
        # 4. extract profiles and plot them
        #print 'extract profiles and plot them'    
    
        #### without cortical columns - old heat
        #print 'start extract profiles and plot them with directory : ', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p)
        #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_extractProfiles.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-j', 'old'])
        
        #### without cortical columns - new heat
        #print 'start extract profiles and plot them with directory : ', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p)
        #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_extractProfiles.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-j', 'new'])
 
        
        ## with cortical columns
        #for diam in diams:      ## with cortical columns
            #print 'extract profiles, diam %s', str(diam)
            #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_extractProfiles.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-c', str(diam), '-j', 'old'])         # - old heat
            
            ## new heat
            #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_extractProfiles.py', '-p', p, '-s', s, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-c', str(diam), '-j', 'new'])         # - new heat
        print ''
        
        # 5. analyze profiles
        
        subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_analyseProfiles.py', '-p', p, '-s', s, '-c', str(3), '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-j', 'new'])  # - new heat 
        
        subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_analyseProfiles.py', '-p', p, '-s', s, '-c', str(3), '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-j', 'old'])  # - old heat
              
        
    ### 6. plot LvsR data for the listOfSubjects
    #for diam in diams:
        #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_plotRightLeftProfiles.py', '-p', p, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-c', str(diam), '-j', 'old'])  # - old heat
        
        #subprocess.check_call(['python', '/volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_plotRightLeftProfiles.py', '-p', p, '-d', '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/%s/' % (p), '-c', str(diam), '-j', 'new'])  # - new heat
            
        
        
        
#heatCompareFile.close()        
        
        