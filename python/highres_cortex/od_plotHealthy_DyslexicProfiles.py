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
#
#
#
# this function will plot already extracted profiles from 2 hemispheres on one plot


# example how to run this file:
#python /volatile/od243208/brainvisa_sources/highres-cortex/python/highres_cortex/od_plotHealthy_DyslexicProfiles.py -c 5 -t 314 -d /neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles_NewDB/
import random
from soma import aims, aimsalgo
import subprocess
from optparse import OptionParser
from scipy.stats import mode
import sys, glob, os, os.path, subprocess, sys, time, timeit
import numpy as np
import highres_cortex.od_cutOutRois
from soma.aims import volumetools
import matplotlib.pyplot as plt    
    
if __name__ == '__main__':
    
    healthyList = ['fg140290', 'af140169', 'ml140175', 'ac140159', 'md140208', 'at140353'] #, 'js140266', 'lg140146', 'he140338', 'cb140330']
    dyslexicList = ['js140311', 'ad140157', 'ag140439', 'sg140335']
    realPatientID = None
    directory = None
    threshold = None
    #realSide = 'L'
    columnDiameter = None

    parser = OptionParser('Extract profiles from T2 nobias data using cortex-density-coordinates in ROIs')    
    #parser.add_option('-p', dest='realPatientID', help='realPatientID')
    parser.add_option('-c', dest='columnDiameter', help='columnDiameter to work with')
    parser.add_option('-t', dest='threshold', help='threshold to work with')
    #parser.add_option('-s', dest='realSide', help='Hemisphere to be processed: L or R. L is default')   
    parser.add_option('-d', dest='directory', help='directory')
    options, args = parser.parse_args(sys.argv)
    print options
    print args   
    
    if options.directory is None:
        print >> sys.stderr, 'New: exit. no directory given'
        sys.exit(1)
    else:
        directory = options.directory           

    #if options.realPatientID is None:
        #print >> sys.stderr, 'New: exit. no patient ID given'
        #sys.exit(1)
    #else:
        #realPatientID = options.realPatientID     
        
    if options.columnDiameter is not None:
        columnDiameter = int(options.columnDiameter)
        
    if options.threshold is None:
        print >> sys.stderr, 'New: exit. no threshold given'
        sys.exit(1)
    else:
        threshold = options.threshold  
        
        
    # write out plots for healthy subjects
    # for various mask ROIs
    maskROIs = ['11', '21']
    colours = ['b', 'g'] # , 'r', 'c', 'm', 'y', 'b']
    for m, col in zip(maskROIs, colours):
        # for R and L 
        for realSide in ['L', 'R']:
            healthyL_ROI11 = plt.figure(figsize=(28, 18)) #, dpi=80, facecolor='w', edgecolor='k')
            #healthyR_ROI11 = plt.figure(figsize=(28, 18)) #, dpi=80, facecolor='w', edgecolor='k')
            num = 1
            for realPatientID in healthyList:
                print '----------------- subject  ', realPatientID
                pathToProfL11 = glob.glob(directory + '%s/diam%s/%s_%s_MaskROI%s_profiles_diam%s_over_%s.txt' %(realPatientID, str(columnDiameter), realPatientID, realSide, m, (columnDiameter), str(threshold)))            
                #read in these files
                numbROIsL, coordROIsL, valueROIsL = np.loadtxt(pathToProfL11[0], skiprows = 1, unpack = True)
                # L
                ax1 = healthyL_ROI11.add_subplot(3,3,num)
                ax1.set_title('Profile in all %s mask ROI %s - %s' %(realPatientID, m, realSide))   # subplot 211 title
                ax1.set_xlabel('Cortical depth')
                ax1.set_ylabel('T2-nobias intensity')
                ax1.plot(coordROIsL, valueROIsL, '.', c = col, label = realSide)
                #ax1.legend(loc='upper right', numpoints = 1)
                num += 1        
            plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/Data_diam%s_over%s/healthy_%s_maskROI%s.png' %(str(columnDiameter), str(threshold), realSide, m), bbox_inches='tight')    
            plt.clf()
            plt.close()
    
            # the same for dyslexics
            healthyL_ROI11 = plt.figure(figsize=(28, 18)) #, dpi=80, facecolor='w', edgecolor='k')
            #healthyR_ROI11 = plt.figure(figsize=(28, 18)) #, dpi=80, facecolor='w', edgecolor='k')
            num = 1
            for realPatientID in dyslexicList:
                print '----------------- subject  ', realPatientID
                pathToProfL11 = glob.glob(directory + '%s/diam%s/%s_%s_MaskROI%s_profiles_diam%s_over_%s.txt' %(realPatientID, str(columnDiameter), realPatientID, realSide, m, (columnDiameter), str(threshold)))            
                #read in these files
                numbROIsL, coordROIsL, valueROIsL = np.loadtxt(pathToProfL11[0], skiprows = 1, unpack = True)
                # L
                ax1 = healthyL_ROI11.add_subplot(3,3,num)
                ax1.set_title('Profile in all %s mask ROI %s - %s' %(realPatientID, m, realSide))   # subplot 211 title
                ax1.set_xlabel('Cortical depth')
                ax1.set_ylabel('T2-nobias intensity')
                ax1.plot(coordROIsL, valueROIsL, '.', c = col, label = realSide)
                #ax1.legend(loc='upper right', numpoints = 1)
                num += 1        
            plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/Data_diam%s_over%s/dyslexic_%s_maskROI%s.png' %(str(columnDiameter), str(threshold), realSide, m), bbox_inches='tight')    
            plt.clf()
            plt.close()
    

    
    ##### try to change the order!!
    # write out plots for healthy subjects
    # for various mask ROIs
    maskROIs = ['11', '21']
    patientsLists = [healthyList, dyslexicList]
    keywords = ['healthy', 'dyslexic']
    
    colours = ['b', 'g'] # , 'r', 'c', 'm', 'y', 'b']    
    # for R and L 
    for realSide in ['L', 'R']:
        for listt, keyword in zip(patientsLists, keywords):            
            healthyL_allROIs = plt.figure(figsize=(28, 18)) #, dpi=80, facecolor='w', edgecolor='k')
            num = 1
            for realPatientID in listt:
                print '----------------- subject  ', realPatientID
                ax1 = healthyL_allROIs.add_subplot(3,3,num)
                ax1.set_title('Profile in %s all mask ROIs - %s' %(realPatientID, realSide))   # subplot 211 title
                ax1.set_xlabel('Cortical depth')
                ax1.set_ylabel('T2-nobias intensity')
                for m, col in zip(maskROIs, colours):
                    pathToProfL11 = glob.glob(directory + '%s/diam%s/%s_%s_MaskROI%s_profiles_diam%s_over_%s.txt' %(realPatientID, str(columnDiameter), realPatientID, realSide, m, (columnDiameter), str(threshold)))            
                    #read in these files
                    numbROIsL, coordROIsL, valueROIsL = np.loadtxt(pathToProfL11[0], skiprows = 1, unpack = True)                    
                    ax1.plot(coordROIsL, valueROIsL, '.', c = col, label = realSide)
                    #ax1.legend(loc='upper right', numpoints = 1)
                num += 1        
            plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/Data_diam%s_over%s/%s_%s_allMaskROIs.png' %(str(columnDiameter), str(threshold), keyword, realSide), bbox_inches='tight')    
            plt.clf()
            plt.close()
                
         
         
         



                             
        
        
        
        
        
        
    #pathToProfL = directory + '%s_L_profiles2.txt' %(realPatientID)
    #pathToProfR = directory + '%s_R_profiles2.txt' %(realPatientID)
    
    ## check if both these profiles exist
    #profL = glob.glob(pathToProfL)
    #profR = glob.glob(pathToProfR)
    
    #if len(profL) != 1 or len(profR) != 1:
        ## abort the calculation, as too many or not a single texture file was found
        #f = open(directory + '%s_compareProfilesStat.txt' %(realPatientID), "w")
        #print 'abort the calculation, as too many or not a single profL or R file was found'
        #f.write('abort the calculation, as ' + str(len(profL)) + ' profL and ' + str(len(profR)) + ' profR profile files were found' + '\n')
        #f.close()
        #sys.exit(0) 
    
    
    #numbL, coordL, valueL = np.loadtxt(pathToProfL, skiprows = 1, unpack = True)
    #numbR, coordR, valueR = np.loadtxt(pathToProfR, skiprows = 1, unpack = True)
       
    ## plot the data
    #plt.plot(coordL, valueL, '.', c = 'b', label = 'L')
    #plt.title('Profile in all ROIs')   # subplot 211 title
    #plt.xlabel('Cortical depth')
    #plt.ylabel('T2-nobias intensity')
    #plt.plot(coordR, valueR, '.', c = 'r', label = 'R')
    #plt.legend(loc='upper right', numpoints = 1)
    #plt.savefig(directory + '%s_LvsR_2nobiasT2.png' %(realPatientID))    
    
    ## save profiles also to the outer folder!
    ##plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/' + '%s_LvsR_2nobiasT2.png' %(realPatientID))    
    #plt.clf()
    #plt.close()
    
    ## now plot L vs R in various ROIs
    ## af140169_R_profiles2_ROI_21.txt, af140169_R_profiles2_ROI_11.txt and the same with L
    #pathToROIsProfL = directory + '%s_L_profiles2_ROI_[0-9]*.txt' %(realPatientID)
    ##print 'pathToROIsProfL'
    ##print pathToROIsProfL

    #pathToROIsProfR = directory + '%s_R_profiles2_ROI_[0-9]*.txt' %(realPatientID)
    
    ## check if both these profiles exist. and how many are there
    #profROIsL = glob.glob(pathToROIsProfL)
    #profROIsR = glob.glob(pathToROIsProfR)
    
    #print 'profROIsL'
    #print profROIsL
    #print 'profROIsR'
    #print profROIsR
    #numOfCommonRLregions = 0
    
    #for i in range(len(profROIsL)):
        ## check if this L profile is from the same mask ROI as the right one:
        ## check if the corresponding R - file exists
        #profROIsRcorrespond = glob.glob(profROIsL[i].replace('_L_', '_R_'))
        #if len(profROIsRcorrespond) == 1:      
            #numOfCommonRLregions += 1
            #print 'corresponding files ', profROIsL[i], ' and ', profROIsRcorrespond[0]
            ## read in the respective files
            #numbROIsL, coordROIsL, valueROIsL = np.loadtxt(profROIsL[i], skiprows = 1, unpack = True)
            #numbROIsR, coordROIsR, valueROIsR = np.loadtxt(profROIsRcorrespond[0], skiprows = 1, unpack = True)
            
            ## get the ROI ID
            #iD = (profROIsL[i].split('_L_profiles2_ROI_')[1]).split('.txt')[0] # '/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/ml140175/ml140175_R_profiles2_ROI_11.txt'
            ## plot the data
            #plt.plot(coordROIsL, valueROIsL, '.', c = 'b', label = 'L')
            #plt.title('Profile in ROI %s ' %(iD))   # subplot 211 title
            #plt.xlabel('Cortical depth')
            #plt.ylabel('T2-nobias intensity')
            #plt.plot(coordROIsR, valueROIsR, '.', c = 'r', label = 'R')
            #plt.legend(loc='upper right', numpoints = 1)
            #plt.savefig(directory + '%s_LvsR_2nobiasT2_ROI_%s.png' %(realPatientID, iD))   
            
            ## save profiles also to the outer folder!
            ##plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/' + '%s_LvsR_2nobiasT2_ROI_%s.png' %(realPatientID, iD))    
            #plt.clf()
            #plt.close() 
    #print 'found ', numOfCommonRLregions, ' numOfCommonRLregions '       
            
       
    ## plot these plots into 1 image
    #fig = plt.figure(figsize=(21, 6)) #, dpi=80, facecolor='w', edgecolor='k')
    #numOfCommonRLregions += 1
    #ax1 = fig.add_subplot(1,numOfCommonRLregions,1)
    #ax1.plot(coordL, valueL, '.', c = 'b', label = 'L')
    #ax1.set_title('Profile in all ROIs')   # subplot 211 title
    #ax1.set_xlabel('Cortical depth')
    #ax1.set_ylabel('T2-nobias intensity')
    #ax1.plot(coordR, valueR, '.', c = 'r', label = 'R')
    #ax1.legend(loc='upper right', numpoints = 1)
   
    #for i in range(len(profROIsL)):
        #profROIsRcorrespond = glob.glob(profROIsL[i].replace('_L_', '_R_'))
        #if len(profROIsRcorrespond) == 1: 
            ## read in the respective files
            #numbROIsL, coordROIsL, valueROIsL = np.loadtxt(profROIsL[i], skiprows = 1, unpack = True)
            #numbROIsR, coordROIsR, valueROIsR = np.loadtxt(profROIsRcorrespond[0], skiprows = 1, unpack = True)
            
            ## get the ROI ID
            #iD = (profROIsL[i].split('_L_profiles2_ROI_')[1]).split('.txt')[0]
            #ax2 = fig.add_subplot(1,numOfCommonRLregions, 2 + i)
            #ax2.plot(coordROIsL, valueROIsL, '.', c = 'b', label = 'L')
            #ax2.set_title('Profile in ROI %s' %(iD))   # subplot 211 title
            #ax2.set_xlabel('Cortical depth')
            #ax2.set_ylabel('T2-nobias intensity')
            #ax2.plot(coordROIsR, valueROIsR, '.', c = 'r', label = 'R')
            #ax2.legend(loc='upper right', numpoints = 1)

    ##plt.show()
    #print 'save the image /neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/%s_LvsR_allVsROIs.png' %(realPatientID)
    #plt.savefig('/neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/' + '%s_LvsR_allVsROIs.png' %(realPatientID), bbox_inches='tight')    
    #plt.clf()
    #plt.close()
    #print 'saved the image /neurospin/lnao/dysbrain/testBatchColumnsExtrProfiles/%s_LvsR_allVsROIs.png' %(realPatientID)
    
    
    # plot it for sufficiently large testBatchColumnsExtrProfiles
    # for a given diameter
    # find all thresholds
    # plot e.g. ROI 21 LvsR for diam = 5 size > 392
    
    ## find those thresholds where non zero number of columns is available. for left
    ##largeL = glob.glob(directory + '/diam%s/%s_L_IDs_diam%s_over_[0-9]*.txt' %(columnDiameter, realPatientID, columnDiameter))
    #largeL = glob.glob(directory + '%s_L_nobiasT2_ROIs_11_21_diam%s_over[0-9]*_exclCommun.png' %(realPatientID, columnDiameter))
    ##ag140439_R_nobiasT2_ROIs_11_21_diam3_over197_exclCommun.png
    #print 'found largeL'
    #print largeL
    ## and for right realSide
    ##largeR = glob.glob(directory + '/diam%s/%s_R_IDs_diam%s_over_[0-9]*.txt' %(columnDiameter, realPatientID, columnDiameter))
    #largeR = glob.glob(directory + '%s_R_nobiasT2_ROIs_11_21_diam%s_over[0-9]*_exclCommun.png' %(realPatientID, columnDiameter))
    #print 'found largeR'
    #print largeR
    ## find common elements
    ##largeLnum = [int((x.split('_over_')[1]).split('.txt')[0]) for x in largeL]
    #largeLnum = [int((x.split('_over')[1]).split('_exclCommun.png')[0]) for x in largeL]
    #print largeLnum
    ##largeRnum = [int((x.split('_over_')[1]).split('.txt')[0]) for x in largeR]
    #largeRnum = [int((x.split('_over')[1]).split('_exclCommun.png')[0]) for x in largeR]
    #print largeRnum
    
    ## find common elelemnts
    #common = set(largeLnum) & set(largeRnum)
    #print common
    
    ## plot LvsR for various ROIs for these thresholds
    #for i in common:
        #print i
        ## find all points from the L hemisphere in ROI 11 that are in columns larger i
        ## open file _L_ColumnInfo.txt - see which columns to take into which ROIs
        
    
    
    

    

      
  
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    