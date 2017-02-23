# -*- coding: utf-8 -*-
"""This module contains the implementation of the static methods of WP6 module

.. module:: poissonProcess
   :platform: Windows
   :synopsis: implementation of the static methods of WP6 module
   
.. moduleauthor:: Bahram Panahandeh <bahram.panahandeh@iwes.fraunhofer.de>
"""

import math
import random
import numpy as np
import datetime

# External module import
# Do not write *.pyc on my PC
import sys
sys.dont_write_bytecode = True


           
'''poissonProcess function: Estimation of random failure occurence of components
                                              
Args:              
    startOperationDate (timedate) : start date of operation
    simulationtime (float)        : simulation time [day]
    failureRate (float)           : failure rate [1/day]

Attributes:         
    no attributes                      

Returns:
    randomList [list] : random failure occurence of a component [1/day]
  
''' 
# poisson process computational code for dtocean-operations-and-maintenance
def poissonProcess(startOperationDate, simulationTime, failureRate):
    
    # result of poisson process
    randomList = []  
    
    # intermediate results
    timeStep = []
    
    # intermediate results
    timeStepAll = 0
    number      = 0
    
    # poison parameter
    loopNumber       = 2000
    lowerPercentile  = 40
    upperPercentile  = 70
    timeStepLoop     = []
    numberLoop       = []
    numberLoopFilt   = []
    timeStepLoopFilt = []
    
    dummyStartOperationDate = datetime.datetime(startOperationDate.year,
                                                startOperationDate.month,
                                                startOperationDate.day,
                                                startOperationDate.hour)
        
    endOperationDate = dummyStartOperationDate + datetime.timedelta(days = simulationTime)
     
    # poisson trial loop   
    for lCnt in range(0,loopNumber):  
        timeStepAll = 0 
        timeStep = [] 
        number = 0     
        # calculation loop         
        while timeStepAll < simulationTime:
            
            # time dt
            dt = -math.log(1.0 - random.random()) / failureRate
            timeStepAll = timeStepAll + dt       
            number = number + 1
            timeStep.append(dt)
        
        #delete last entries
        number = number-1
        del timeStep[-1]
        #save loop results
        numberLoop.append(number)
        timeStepLoop.append(timeStep)
    
    upperPercentileValue = np.percentile(numberLoop,upperPercentile)
    lowerPercentileValue = np.percentile(numberLoop,lowerPercentile)
    
    #AllValidTrials = [x for x in numberLoop if ((x>lowerPercentileValue)&(x<upperPercentileValue))]
    for lCnt in range(0,loopNumber):
        if ((numberLoop[lCnt]>=lowerPercentileValue)&(numberLoop[lCnt]<=upperPercentileValue)):
            numberLoopFilt.append(numberLoop[lCnt])
            timeStepLoopFilt.append(timeStepLoop[lCnt])
    
    if len(numberLoopFilt)>0:       
        loopIndex = random.randint(0,len(numberLoopFilt)-1)    
        timeStep = timeStepLoopFilt[loopIndex]
        number = numberLoopFilt[loopIndex] 
    else:
        timeStep = []
        number = 0
          
    TimeStamp = dummyStartOperationDate
    
    for iCnt in range(0,len(timeStep)):
        AddTime = int(np.round(timeStep[iCnt]))
        TimeStamp = TimeStamp + datetime.timedelta(days = AddTime)
        
        # take only the events less than endOperationDate
        
        #if TimeStamp <= endOperationDate and iCnt < maxNrOfEvents:
        if TimeStamp <= endOperationDate:
            randomList.append(TimeStamp)
        else:
            break
            
    # return randomList     
    return randomList   
   