# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:15:46 2020

@author: kcaldeira

Computer ROI on ramp down to 50 as function of abatement cost and 
"""


from DICEeq import *
from plot_utilities import *
from io_utilities import *
import cProfile
import numpy as np

variationVec = 10**np.arange(-1,1.1,0.1)

tlist = [0,5, 35, 300]
tmax = 300

resList = []

for damageScale in variationVec:
    
    initState, initParams =  createGlobalVariables(tmax,1,tlist,1)
    
    initParams['a1'] = initParams['a1'] * damageScale
    initParams['a2'] = initParams['a2'] * damageScale
    
    initParams['saveOutput'] = True
    
    baseResults = DICE_fun([0,0,0,0],initState,initParams)
    baseConsumption = np.array(baseResults[1]['c'])
    
    for abateScale in variationVec:
        
        initState, initParams =  createGlobalVariables(tmax,1,tlist,1)
        
        initParams['a1'] = initParams['a1'] * damageScale
        initParams['a2'] = initParams['a2'] * damageScale
        
        initParams['pbacktime'] = initParams['pbacktime'] * abateScale
         
        initParams['saveOutput'] = True
        
        results = DICE_fun([0,0,1,1],initState,initParams)
        consumption = np.array(results[1]['c'])
        
        deltaConsumption = consumption - baseConsumption
        resList = np.append(resList, [damageScale, abateScale, np.irr(deltaConsumption),[i for i, x in enumerate(deltaConsumption) if x > 0][0]] )
        
        
        
        
        
        
    
    
