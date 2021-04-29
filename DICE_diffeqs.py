#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:09:41 2020

@author: kcaldeira and Candise Henry
"""

"""
This is the main set of routines for the DICEeq model.

The name DICEeq was meant to evoke the idea of differential equations (diffeqs)
and also DICE-equivalent, because the goal here is to make a version of DICE
that is based on differential equations rather than difference equations.

Further, this version separates these time intervals:
    time step
    decision time points
    driving data
    
"""

"""
Important differences from DICE model.

The original DICE model had numbers in units of GtC, GtCO2, USD, trillions USD,
millions of people, per capita, per 5-year period, per year.

One of the first things done is to normalize units.

Somewhat aritrarily, we will choose to use tC (tons of carbon), USD, people,
years.
 

The variable <info> contains all of the info and functions needed
to compute time derivatives.

<info> variables:
    gBack -- rate of cost-improvement of backstop technology (fraction per year)
    expcost2 -- exponent describing how abatement cost scales with abatement fraction
    t -- time in years from start of problem (not calendar year !)
    
<info> functions:
    L[t] -- population (people)
    sigma[t] -- carbon emissions per unit unabated economic output (tC/USD)
    miu[t] -- actions taken by the agent [actions are at specified times, this
              function step functions at each of the decision points
    al[t] -- total factor productivity, in units of amount of output in USD of 1 person
             with 1 USD of capital.
    abateAmountFree[t] -- deforestation emissions
    
NOTE: If <info> is local in an environment, it is called <info>, but
      we try to keep it global to avoid shadowing issues with 
    
The variable <state> contains all of the information that defines the state.

<state> variables:
    k -- capital stock
    
"""
    
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:35:42 2019
Code for non-cooperative Nash equilibrium optimization of dual actor DICE model 
with resource transfer.
Similar to Nordhaus RICE method.
Optimize x action vector: (1) % CO2 reduction, (2) % allocation, as both dollar
transfer amount (TRANSFER) and % of mitigation (ALLOC), from actor A to actor B.
Only 1 econ function (instead of 2, one for each actor).
Use with Process_Inputs_Nash.py.
@author: candise henry
"""

import numpy as np
import itertools as it
import utils
import copy
from plot_utilities import *
from scipy import interpolate
import random
#import copy
import os
import sys
# Specify path where MIDACO files are stored depending on OS
if (os.name != "nt"):
    sys.path.insert(0, '/mnt/c/Users/clh19/Documents/Carnegie/Energy_Access/DICE_Code/MIDACO6.0') # Linux (Candise Henry)
else:
    sys.path.insert(0, 'C:/Users/kcaldeira/Documents/MIDACO/Windows') # Windows
import midaco_key as midaco
from io_utilities import pickle_results,filter_dic 
import datetime

########################################################################
################### FUNCTIONS & OPTIMIZATION PROBLEM ###################
########################################################################

#%%

# see below for list of variables

def initStateInfo(kwargs):
    # creates <state> and <info>
    state = {}  # state variables
    info = {} # driving variables and diagnostic info
    
   #---------------------------------------------------------------------------
   #------- Unpack keyword arguments ------------------------------------------
   #---------------------------------------------------------------------------

      #------- Process information about time -------- ---------------------------
      #-----> integration time step  
    
    if 'dt' in kwargs.keys():
        dt = kwargs['dt']
    else:
        dt = 1
    info['dt'] = dt 
  
    #-----> decisionTimes 
    
    if 'decisionTimes' in kwargs.keys():
        info['decisionTimes'] = kwargs['decisionTimes']
    else:
        info['decisionTimes'] = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]
    nDecisionTimes = len(info['decisionTimes'])

    timeEnd = info['decisionTimes'][-1] # assume last decision time is end of problem
    info['timeEnd'] = timeEnd
    tlist = np.arange(0,timeEnd+dt,dt)
    nTimeSteps = len(tlist)
    info['nTimeSteps'] = nTimeSteps
    
   #-----> COIN mode 
    
    if 'COINmode' in kwargs.keys():
        info['COINmode'] = kwargs['COINmode']
    else:
        info['COINmode'] = False  # Default values always aimed to get as close as possible to default DICE   
    COINmode = info['COINmode']

   #-----> number of technolologies 
    
    if 'nTechs' in kwargs.keys():
        info['nTechs'] = kwargs['nTechs']
    else:
        info['nTechs'] = 1  # Default values always aimed to get as close as possible to default DICE   
    nTechs = info['nTechs']

   #-----> allowable emissions 

    if 'freeAbateAmount' in kwargs.keys():
        state['cumEInd'] = -kwargs['freeAbateAmount'] # units of init emission equivalents 
    else:
        state['cumEInd'] = 0.0  # cumulative emissions (tCO2)

    if 'carbonBudget' in kwargs.keys():
        info['carbonBudget'] = kwargs['carbonBudget']
    else:
        info['carbonBudget'] = -999.  # Negative value means unlimited budget   

           
       #-----> upper and lower bound on the sum of mius for each technology

    if 'limMiuLower' in kwargs.keys():
        if isinstance(kwargs['limMiuLower'], list):
            info['limMiuLower'] = kwargs['limMiuLower']
        else:
            info['limMiuLower'] = len(info['decisionTimes'])*[kwargs['limMiuLower']]
    else:
        info['limMiuLower'] = len(info['decisionTimes'])*[0]
    info['limMiuLower'] = np.array(info['limMiuLower'] , dtype = float) 

    if 'limMiuUpper' in kwargs.keys():
        if isinstance(kwargs['limMiuUpper'], list):
            info['limMiuUpper'] = kwargs['limMiuUpper']
        else:
            info['limMiuUpper'] = len(info['decisionTimes'])*[kwargs['limMiuUpper']]
    else:
        info['limMiuUpper'] = len(info['decisionTimes'])*[1.2]  # DICE default
    info['limMiuUpper'] = np.array(info['limMiuUpper'] , dtype = float) 

    # optimize on savings rate?

    if 'optSavings' in kwargs.keys():
        info['optSavings'] = kwargs['optSavings']
    else:
        info['optSavings'] = True

    #----------------------------------------------------------------------------------------------
    # savings rate decision times?

    if 'savingDecisionTimes' in kwargs.keys():
        info['savingDecisionTimes'] = kwargs['savingDecisionTimes']
    else:
        info['savingDecisionTimes'] = decisionTimes    # savings rate decision times?
      
    if 'decisionInterpSwitch' in kwargs.keys():
        info['decisionInterpSwitch'] = kwargs['decisionInterpSwitch']
    else:
        info['decisionInterpSwitch'] = 1 # right now, default is linear interpolation

    #---------------------------------------------------------------------------------------------
    #-----> techLearningCurve: Does the technology have a learning curve? 

    if 'techLearningCurve' in kwargs.keys():
        info['techLearningCurve'] = kwargs['techLearningCurve']
    else:
        info['techLearningCurve'] = nTechs*[False]


     #-----> techInitCost

    if 'techInitCost' in kwargs.keys():
        info['techInitCost'] = kwargs['techInitCost']
    else:
        init['techInitCost'] = nTechs*[1.] #@@@@@@@@@@ COINmode @@@@@@@@@@@@       
      
     #-----> techInitAmount

    if 'techInitAmount' in kwargs.keys():
        info['techInitAmount'] = kwargs['techInitAmount']
    else:
        info['techInitAmount'] = nTechs*[0.] # Note: techInitAmount must be specified if this technology has a learning curve.
    state['cumAbateTech'] = info['techInitAmount']  

     #-----> techLearningRate:  Improvement per year if no learning rate, else exponent on power law

    if 'techLearningRate' in kwargs.keys():
        info['techLearningRate'] = kwargs['techLearningRate']
    else:
        info['techLearningRate'] = nTechs*[ 1.-(1.-0.025)**0.2] # Nominally 0.5% per year but slightly different to be more consistent with DICE
  
   #-----> firstUnitFractionalCost
 
    if 'firstUnitFractionalCost' in kwargs.keys():
        info['firstUnitFractionalCost'] = kwargs['firstUnitFractionalCost']
    else:
        info['firstUnitFractionalCost'] = nTechs*[0.]  # vanilla DICE

    #-----> utilityOption
 
    if 'utilityOption' in kwargs.keys():
        info['utilityOption'] = kwargs['utilityOption']
    else:
        info['utilityOption'] = 0  # vanilla DICE       
           
    #if 'innovationRatio' in kwargs.keys() and (info['learningCurveOption'] == 4 or   info['learningCurveOption'] == 4):
    #    info['innovationRatio'] = kwargs['innovationRatio']
  
   #----->       damageCostRatio = 1.0 by default (ratio of climate damage cost to default value).
 
    if 'damageCostRatio' in kwargs.keys():
        info['damageCostRatio'] = kwargs['damageCostRatio']
    else:
        info['damageCostRatio'] = 1.0  # default to DICE default
  
   #----->       abatementCostRatio = 1.0 by default (ratio of abatement cost to default value).
 
    if 'abatementCostRatio' in kwargs.keys():
        info['abatementCostRatio'] = kwargs['abatementCostRatio']
    else:
        info['abatementCostRatio'] = 1.0  # default to DICE default
       
 
   #----->       parallel =  # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
   # number of cores to use, 0 or 1 is single core,
 
    if 'parallel' in kwargs.keys():
        info['parallel'] = kwargs['parallel']
    else:
        info['parallel'] = 1  # default to 1 core

    #-----> maximumm number of iterations 

    if 'maxeval' in kwargs.keys():
        info['maxeval'] = kwargs['maxeval']
    else:
        info['maxeval'] = 1000    
        
    #-----> SEED midaco options 

    if 'SEED' in kwargs.keys():
        info['SEED'] = kwargs['SEED']
    else:
        info['SEED'] = 0
 
    #-----> FOCUS midaco options 

    if 'FOCUS' in kwargs.keys():
        info['FOCUS'] = kwargs['FOCUS']
    else:
        info['FOCUS'] = 0

    #-----> ANTS midaco options 

    if 'ANTS' in kwargs.keys():
        info['ANTS'] = kwargs['ANTS']
    else:
        info['ANTS'] = 0

    #-----> KERNEL midaco options 

    if 'KERNEL' in kwargs.keys():
        info['KERNEL'] = kwargs['KERNEL']
    else:
        info['KERNEL'] = 0
       
    #-----> ANTS midaco options 

    if 'EVALSTOPint' in kwargs.keys():
        info['EVALSTOPint'] = kwargs['EVALSTOPint']
    else:
        info['EVALSTOPint'] = 20000. # Interval for testing evaluation stop

    #-----> KERNEL midaco options 

    if 'EVALSTOPtol' in kwargs.keys():
        info['EVALSTOPtol'] = kwargs['EVALSTOPtol']
    else:
        info['EVALSTOPtol'] = 1.e-10
       

   
    #---------------------------------------------------------------------------
    #------- Get various DICE parameter values ---------------------------------
    #---------------------------------------------------------------------------
    info['tlist'] = tlist
    
    #** Preferences
    info['elasmu'] = 1

    # DICE:    info['elasmu'] = 1.45 # Elasticity of marginal utility of consumption     /1.45 /

    if 'prstp' in kwargs.keys():
        info['prstp'] = kwargs['prstp'] #   Initial rate of social time preference per year   /.015  /
    else:
        info['prstp'] = 0.03

        # DICE:     info['prstp'] = 0.015 #   Initial rate of social time preference per year   /.015  /
        
    info['rr'] = np.exp( -info['prstp'] * tlist)

    # DICE: info['rr'] = (1./(1.+info['prstp']))** tlist
    
    #** Population and technology
    gama = 0.3 #     Capital elasticity in production function    info['/.300    /
    info['gama'] = gama
    info['depk'] = 0.1 #      Depreciation rate on capital (per year)          /.100    /
     


    info['L']= [1.0]*nTimeSteps

    state['k']=1.0
    #info['sigma'] = 1.01**-tlist # the units on sigma are relative to base case emissions
    #                              assumption is base case if sustained would warm 2 C in 100 years.
    info['sigma'] =np.exp(- 0.01 * tlist)
    info['abateAmountFree'] = np.zeros(len(tlist))
    
    dela = 0.01
    #info['al'] = (1.+dela)**tlist  # total factor productivity improving 1% per
    info['al'] =np.exp( dela * tlist)
    
    info['expcost2'] = 2 #  Exponent of control cost function               / 2.6  /

    info['alpha'] = 0.02 #   Assume 0.02 C warming per year initial condition emissions 
    #                        based on concept of 2 C warming in 100 years if sustained initial condition emissions

    info['a1'] = 0. #       Damage intercept                                 /0       /
    info['a2'] = 0.005 #    Fraction of GDP per degree of warming squared 2 % damages at 2 C temp increase
    info['a3'] = 2  #       Damage exponent                                  /2.00    /

    info['K0'] = 300.e12 # USD$ capital
    info['Y0'] = 100.e12 # USD$/yr gross production
        # q0 in vanilla DICE is 105.177 trillion USD.

    info['optlrsav'] = info['gama'] * ( info['depk'] + dela ) / ( info['depk'] + info['prstp'] )

    info['tau'] = info['gama']  / ( info['depk'] + info['prstp'] ) #  = info['K0']/info['Y0'] # time constant relating reference state gross production 
    #print (info['optlrsav'],info['tau'])


    #info['tnopol'] =    Period before which no emissions controls base  / 45   /
    #info['cprice0'] =   Initial base carbon price (2010$ per tCO2)      / 2    /
    #info['gcprice'] =   Growth rate of base carbon price per year       /.02   /

    # -----------------------------------------------------------------
    # create dictionary for diagnostic output.
    # All items are numpy arrays with first dimension as time, and second dimension as tech if available

    timeShape = np.zeros(nTimeSteps)
    timeTechShape = np.zeros((nTimeSteps,nTechs))

    # state variables

    info['tatm'] = timeShape.copy()

    info['k'] = timeShape.copy()
    info['cumAbateTech'] = timeTechShape.copy() # not always a state variable

    # dstate variables

    info['dk'] = timeShape.copy()

    # informational

    info['yGross'] = timeShape.copy()
    info['damageFrac'] = timeShape.copy()
    info['damages'] = timeShape.copy()
    info['y'] = timeShape.copy()
    info['c'] = timeShape.copy()
    
    info['rsav'] = timeShape.copy()
    info['inv'] = timeShape.copy()
    info['cpc'] = timeShape.copy()
    info['periodu'] = timeShape.copy()
    info['cemutotper'] = timeShape.copy()
    
    info['eGross'] = timeShape.copy()
    info['eInd'] = timeShape.copy()
    info['abateAmount'] = timeShape.copy() 
    info['abateAmountTech']  =  timeTechShape.copy()
    info['abateFrac'] = timeShape.copy()
    
    info['abateCost'] = timeShape.copy()
    info['abateCostTech']  =  timeTechShape.copy()
    
    info['pBackTime']  =  timeTechShape.copy()  
    
    info['mcAbate'] = timeShape.copy()
    info['mcAbateTech'] = timeTechShape.copy()

    info['miu'] = timeShape.copy() 
    info['miuTech'] = timeTechShape.copy()
    
    return state,info

#%%

def dstatedt(state, info):

    # note: state is a dictionary of scalars of current state of the system
    #       everything else is either a vector of length time, or an array of time x nTechs
    
    dstate = {}
    epsilon = 1.e-20 # small number (almost zero)
    bignum = 1.e20 # big number (almost infinity)
    
    # these three get created just because they get used alot
    COINmode = info['COINmode']
    idxTime = info['idxTime']
    nTechs = info['nTechs']
    firstUnitFractionalCost = info['firstUnitFractionalCost']  
    techLearningCurve =  info['techLearningCurve']

    tAtmState = info['alpha']*state['cumEInd']
     
    expcost2 = info['expcost2'] 
     

    # these get created because they get updated
    miu = info['miu']
    miuTech = info['miuTech'] # These are each technologies (including non decision technologies), summing to miu
    miuRatios = info['miuRatios']  # This is ratio of decision technologies to each other, summing to one
    yGross = info['yGross']
    eGross = info['eGross']
    pBackTime = info['pBackTime']
    mcAbate = info['mcAbate']
    mcAbateTech = info['mcAbateTech']
    abateCost = info['abateCost']
    abateCostTech = info['abateCostTech']
    abateAmount = info['abateAmount']
    abateAmountTech = info['abateAmountTech']
    abateFrac = info['abateFrac']

    damages = info['damages']
    damageFrac = info['damageFrac']

    rsav = info['rsav']
    inv = info['inv']

    c = info['c']
    cpc = info['cpc']
    y = info['y']

    periodu = info['periodu']
    cemutotper = info['cemutotper']

    eInd = info['eInd']


    # tendencies for recording
    k = info['k']
    dk = info['dk']
    tatm = info['tatm']


    cumAbateTech = info['cumAbateTech']

    #-------------------------------------------------------------------------------------------------
    # compute pBackTime

    for idxTech in list(range(nTechs)):
        if techLearningCurve[idxTech]:
            #Learning curve
            pBackTime[idxTime,idxTech] =  (
                info['abatementCostRatio'] * info['techInitCost'][idxTech]*
                (state['cumAbateTech'][idxTech]/info['techInitAmount'][idxTech]) ** -info['techLearningRate'][idxTech]
            )
        else:
            # DICE-like representation
            pBackTime[idxTime,idxTech] = (
                info['abatementCostRatio'] * info['techInitCost'][idxTech] * 
                np.exp(-info['techLearningRate'][idxTech]*idxTime*info['dt']) 
            )

    #-------------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------

    # Climate damage cost at t
    tAtmDamage = max(0.0, tAtmState)  # do not consider damage function for temperatures < 0.

    damageFrac[idxTime] = info['damageCostRatio'] * ( info['a1'] * tAtmDamage + info['a2'] * tAtmDamage**info['a3'] )

    yGrossPotential =  (info['al'][idxTime]  * info['L'][idxTime] **(1 - info['gama'])) * (max(state['k'],epsilon)**info['gama'])

    damages[idxTime] =  damageFrac[idxTime] * yGrossPotential
    
    yGross[idxTime] = (1 - damageFrac[idxTime]) * yGrossPotential

    # Gross domestic product GROSS of damage and abatement costs at t ($ 2005 per year)
    # DICE:  yGross[idxTime] = yGrossPotential

    # Industrial CO2 emission at t (tCO2)
    eGross[idxTime] = yGross[idxTime] * info['sigma'][idxTime] # what industrial emissions would be in the absence of abatement
        

    # When there is a limited carbon budget, to get the optimizer to optimizer we will charge the optimizer for
    # abatement and then not give it for 

    miuEff = miu[idxTime]

    if (info['carbonBudget'] >= 0):

        remainingBudget = info['carbonBudget'] - state['cumEInd']

        if eGross[idxTime] * (1 - miu[idxTime]) > remainingBudget:
            miuEff = 1.0 -  remainingBudget / eGross[idxTime]

    mcAbate[idxTime] = 1.e20

    for idxTech in list(range(nTechs)):
        miuTech[idxTime,idxTech] = miuEff * miuRatios[idxTime,idxTech]
        mcAbateTech[idxTime,idxTech] =   pBackTime[idxTime,idxTech] *(firstUnitFractionalCost[idxTech] + (1.0 - firstUnitFractionalCost[idxTech])* max(epsilon,miuTech[idxTime,idxTech])**(expcost2 - 1.0))
        mcAbate[idxTime] = min(mcAbate[idxTime],mcAbateTech[idxTime,idxTech]) 

    abateCost[idxTime] = 0.0
    for idxTech in list(range(nTechs)):
            
        abateCostTech[idxTime,idxTech] = (
            eGross[idxTime] *  pBackTime[idxTime,idxTech] * 
            ( firstUnitFractionalCost[idxTech] * miuTech[idxTime,idxTech]  + (1.0 - firstUnitFractionalCost[idxTech] ) *   max(epsilon,miuTech[idxTime,idxTech]) **expcost2 / expcost2) 
        )
        abateCost[idxTime] += abateCostTech[idxTime,idxTech]

        abateAmountTech[idxTime,idxTech] = eGross[idxTime]  * miuTech[idxTime,idxTech]
        abateAmount[idxTime] += abateAmountTech[idxTime,idxTech] 

    # this next thing is a try to get convergence (this is hocus pocus superstition)

    dstate['cumAbateTech'] = abateAmountTech[idxTime]

    eInd[idxTime] =  eGross[idxTime]  * (1 -  miu[idxTime]) # industrial emissions

    # Forest-related CO2 emissions
    # Total CO2 emission at t (tCO2)

    dstate['cumEInd'] = eInd[idxTime]

    abateFrac[idxTime] = abateCost[idxTime] / yGross[idxTime]    # <abateCost> is total of abatement this time step 

    # Gross domestic product NET of damage and abatement costs at t ($ 2005 per year)
    y[idxTime] = yGrossPotential - damages[idxTime] - abateCost[idxTime]

    # Investment at time t
    if info['optSavings']:
        rsav[idxTime] = info['savings'][idxTime] 
    else:
        rsav[idxTime] = info['optlrsav']
    inv[idxTime] = rsav[idxTime] * y[idxTime]

    # Consumption ($ 2005)
    c[idxTime] = y[idxTime] - inv[idxTime]

    # Consumption per capita ($ per person per year)
    cpc[idxTime] = c[idxTime] / info['L'][idxTime] 

    # Utility per capita (one period utility function)
    if info['utilityOption'] == 0:
        periodu[idxTime] = (max(0.001* cpc[idxTime],epsilon)**(1 - info['elasmu']) - 1)/(1 - info['elasmu']) - 1 # Vanilla Dice
        # This ugly scaling by 0.001 is intended to keep utility numbers the same as what Nordhaus had
    else:  # utilityOption == 1 --> optimize on consumption
        periodu[idxTime] = max(c[idxTime],epsilon)

    # Period utility
    cemutotper[idxTime] = periodu[idxTime] *info['L'][idxTime]  * info['rr'][idxTime] 

    # ----------- create tendencies

       # Time rate of change of capital

    dstate['k'] = inv[idxTime]/info['tau'] - info['depk']* state['k'] 
  
    
         
    #-------------------------------------------------------------------------

    # note only need to add things here that are not 
    # tendencies for recording
    k[idxTime] = state['k']
    dk[idxTime] = dstate['k']
    cumAbateTech[idxTime] = state['cumAbateTech']

    tatm[idxTime] = tAtmDamage
 
    return dstate

#%%
# step function interpolation

def interpStep(t, timePoints, dataPoints):
    # returns the value of the dataPoint with a time value 
    # timePoints is assumed to be sorted in ascending order
    # returns dataPoints[0] if t < timePoints[0]
    if t >= max(timePoints):
        res = dataPoints[-1]
    else:
        idx = next(ii for ii,vv in enumerate(timePoints) if vv > t)
        idx = max(0,idx-1)
        res = dataPoints[idx]
    return res

#%%

# interpolates to list with zero derivatives at data points

def interpToListZeroDeriv(xList,xDataVals,yDataVals, dt):
    # Interpolates with all joins having a slope of zero !!
    # we assume that time periods are at least dt apart
    xData = copy.copy(xDataVals)
    yData = copy.copy(yDataVals)
    order = np.argsort(xData)
    xData = xData[order]
    yData = yData[order]

    idxRight = np.minimum(np.searchsorted(xData,xList),len(xData)-1)
    idxLeft = idxRight - 1
    yResult = []
    for idx in range(len(xList)):
        x = xList[idx]
        x0 = xData[idxLeft[idx]]
        y0 = yData[idxLeft[idx]]
        x1 = xData[idxRight[idx]]
        y1 = yData[idxRight[idx]]
        if abs(x0-x1) >= dt :
            y = (3.*x0*x1**2*y0 - x1**3*y0 - 2.*x**3*(y0 - y1) + 3.*x**2*(x0 + x1)*(y0 - y1) + 
                    x0**3*y1 - 3.*x0**2*x1*y1 + 6.*x*x0*x1*(-y0 + y1))/(x0 - x1)**3
        else:
            y = (y0+y1)/2. # if x values differ by less than dt, return mean of y values
        yResult.append(y)
    return yResult


#%%

def DICE_fun(act,state,info):
    #  This is the function called by <wrapper>, called by the midaco solver

    # It contains the actions that the solver is solving for, the initial state of the system, and general system info.
    # (Initial state of the system could also be stored in info [as a future modification].)

    # This function does two different things:

    # It takes the decision variables in a form that is convenient for the solver (i.e., lists for real decisions only), and converts it
    # into a form that is convenient for the differential equations (i.e., lists by time steps)

    # The steps of this function are:

    # 1. Expand <act> for decisions to decision times made implicit by constraints or specification.

    # 2. Interpolate decision times to time steps.
    # #     (This was brought outside the time loop, because repeated interpolation was causing things to run slowly.)

    # 3. Time step through differential equations.


    # Initially we are going to assume that the only decision are the abatement
    # level MIU.
    # relies on globals <state> and <info>
    savingDecisionTimes = info['savingDecisionTimes']
    nDecisionTimes = len(info['decisionTimes'])
    nSavingDecisions  = len(savingDecisionTimes)
    # double negatives mean find both time and value
    nSavingValues = int( nSavingDecisions - 
        len([num for num in savingDecisionTimes if num < 0])/2)
    nTechs = info['nTechs']  
    COINmode = info['COINmode'] 
    tlist = info['tlist']
    dt = info['dt']
    nTimeSteps = info['nTimeSteps']

    limMiuUpper = info['limMiuUpper']
    limMiuLower = info['limMiuLower']

    # ------------------------------------------------------------------------
    # 1. unpack act
    # ------------------------------------------------------------------------

    # -----> initialize miu decisions

    nMiuDecisions = np.count_nonzero(limMiuUpper - limMiuLower)  # This expression counts the number of different values

    miuDecisions = (np.array(limMiuUpper) + np.array(limMiuLower))/2. # if limMiuUpper == limMiuLower, set action to this value      
    icount = 0
    for idx in range(nDecisionTimes):
        if limMiuUpper[idx] > limMiuLower[idx]:
            miuDecisions[idx] = act[icount]
            icount += 1
    info['miuDecisions'] = miuDecisions

    # -----> initialize miuRatio decisions

    start = nMiuDecisions

    sequentialDecisions = np.reshape(act[ start : start + nDecisionTimes * (nTechs-1) ],(nTechs-1,nDecisionTimes)) 
    miuRatioDecisions = -np.ones(((nDecisionTimes,nTechs)))
    remaining = np.ones(nDecisionTimes)
    idxTechDecision = 0
    for idxTech in list(range(nTechs)):
        if idxTechDecision < len(sequentialDecisions):
            miuRatioDecisions[:,idxTech] = remaining * sequentialDecisions[idxTechDecision]
            remaining = remaining * (1.0 - sequentialDecisions[idxTechDecision])
            idxTechDecision += 1
        else: # last one gets remaining
            miuRatioDecisions[:,idxTech] = remaining

    # -----> initialize savings decisions


    if info['optSavings']:
        start = nMiuDecisions + nDecisionTimes * (nTechs - 1)
        savings = np.array(act[start:start + nSavingDecisions]) #
        startFreeAbate = nMiuDecisions + nDecisionTimes * (nTechs-1) + nSavingDecisions
    else: # specified savings
        savings = np.array([info['optlrsav'] for item in info['savingDecisionTimes']])
        startFreeAbate = nMiuDecisions + nDecisionTimes * (nTechs-1)         

    # ------------------------------------------------------------------------
    # 2. now interpolate across time steps
    # ------------------------------------------------------------------------   

    #  for miuratios, change from cumulative to actual ratios.
    #  i.e., on input if miu  = 0.8, and miuRatio = [0.25, 0.333333, 0.5]
    # we would have on cumulative (0.25 x 0.8) = 0.2; 0.8 - 0.2 = 0.6; (0.3333 * 0.6 ) = 0.2; ... 
    # or in terms of 
    # This would be converted to, miu = 0.8 and miuRatios = [0.25, 0.25, 0.25, 0.25]

    if 10 == info['decisionInterpSwitch']:  # zzero derivatives at data points
        miu = miuDecisions[list(map(lambda t0:len([v for v in info['decisionTimes'] if v <= t0])-1,tlist))]
    else:
        miu =  np.interp(tlist,info['decisionTimes'],miuDecisions)
    info['miu'] = miu

    miuRatios = np.zeros((nTimeSteps,nTechs))
    miuRemaining = np.ones(nTimeSteps)
    timeNull = -np.ones(nTimeSteps)
    for idxTech in list(range(nTechs)):
        miuRatios[:,idxTech] = np.interp(tlist,info['decisionTimes'],miuRatioDecisions[:,idxTech])
    info['miuRatios'] = miuRatios

    # -----------interpolate decisions to other times

    if nSavingDecisions == nSavingValues:
        x = savingDecisionTimes
        y = savings
    else:
        x = np.zeros(nSavingValues)
        y = np.zeros(nSavingValues)
        idxPair = 0
        iOdd = False

        for idx in range(nSavingDecisions):
            if savingDecisionTimes[idx] < 0:
                iOdd = not(iOdd)
                if iOdd: # first of pair of negative numbers indicates time value
                    if idxPair == 0:
                        previous = savingDecisionTimes[0]
                    else:
                        previous = x[idxPair -1]
                    following = savingDecisionTimes[-1]
                    for v in savingDecisionTimes:
                        if v > previous:
                            following = v
                            break
                    #x[idxPair] =  (previous + dt) + savings[idx] * ((following-dt)-(previous + dt))
                    x[idxPair] =   savings[idx] * (savingDecisionTimes[-1]-savingDecisionTimes[0])
                else:
                    y[idxPair] = savings[idx]
                    idxPair += 1
            else: #regular
                x[idxPair] = savingDecisionTimes[idx]
                y[idxPair] = savings[idx]
                idxPair += 1
            
        order = np.argsort(x)
        x = x[order]
        #y = y[order]

    if 3 == info['decisionInterpSwitch']:  # zzero derivatives at data points
        info['savings'] = interpToListZeroDeriv(tlist,x,y,0.1*dt) # last number is tolerance for equality
    elif 2 == info['decisionInterpSwitch']:  # spline
        #intCoeff = interpolate.splrep(x,y)
        #info['savings']= interpolate.splev(tlist, intCoeff)
        intPchip = interpolate.pchip(x,y)
        info['savings']= intPchip (tlist)
    elif 1 == info['decisionInterpSwitch']: #linear
        #print(info['savingDecisionTimes'])
        #print(savings)
        info['savings'] = np.interp(tlist,x,y)
    elif 0 == info['decisionInterpSwitch'] or 10 == info['decisionInterpSwitch']: #0 == decisionInterpSwitch; step function
        info['savings'] = y[list(map(lambda t0:len([v for v in x if v <= t0])-1,tlist))]
    else:
        info['savings']  = 0


    # ------------------------------------------------------------------------
    # 3. now time step the action
    # ------------------------------------------------------------------------  

    for idxTime in list(range(info['nTimeSteps'])):
        info['idxTime'] = idxTime
         
        dstate = dstatedt(state, info)  # info is a global used by dstatedt
        
        # eulers method (1 is OK, 0.5 seems fine)
        for key in state:
            state[key] +=  dt * dstate[key]

    #obj = dt*np.sum(info['cemutotper'])+((state['k']-dt*dstate['k'])*(1+info['prstp'])**(-nTimeSteps*dt)-1)/info['tau']
    obj = dt*np.sum(info['cemutotper'])
    info['npvUtility'] = obj

    return float(obj),info

#############################################################################
#####    Main DICE Function                              ####################
#####    Class is used to transfer data among functions  ####################
#############################################################################

class DICE_instance:

    def __init__(self, **kwargs):

        state, info = initStateInfo(kwargs)

        self.state = state
        self.info = info
        self.out = self.runDICEeq() 
    
    def wrapper(self, act):

        state = self.state
        info = self.info

        welfare, info = DICE_fun(act,state,info)

        # "Without loss of generality, all objectives are subject to minimization."
        # http://www.midaco-solver.com/data/other/MIDACO_User_Manual.pdf

        ret = -welfare

        return [[ret],[0.0]]

    def runDICEeq(self):

        state = self.state
        info = self.info
        
        # There are three types of actions:

        # miu[reducedDecisionTimeSteps] -- actions to decide on overall abatement level (miu)
        
        # miuRatio[idx, decisionTimeSteps] (for idx all but last technology with a decision)

        # savings rate

        decisionTimes = info['decisionTimes']
        savingDecisionTimes = info['savingDecisionTimes']

        nDecisionTimes = len(info['decisionTimes'])
        nSavingDecisions = len(savingDecisionTimes)
        # double negatives mean find both time and value
        nSavingValues = nSavingDecisions - \
            len([num for num in savingDecisionTimes if num < 0])/2
        nTechs =  info['nTechs'] # total number of technologies in resuls

        limMiuUpper = info['limMiuUpper']
        limMiuLower = info['limMiuLower']

        # -----> initialize miu decisions

        nMiuDecisions = np.count_nonzero(limMiuUpper - limMiuLower) # This expression counts the number of different values

        miuDecisions = np.zeros(nMiuDecisions) # start off assuming complete abatement 
        miuLower = np.zeros(nMiuDecisions) # create empty vector        
        miuUpper = np.zeros(nMiuDecisions) # create empty vector        
        icount = 0
        for idx in range(nDecisionTimes):
            if limMiuUpper[idx] > limMiuLower[idx]:
                miuLower[icount] = limMiuLower[idx]
                miuUpper[icount] = limMiuUpper[idx]
                miuDecisions[icount] = (miuUpper[icount] -miuLower[icount]) * (1.-np.exp(-decisionTimes[icount]/30.))
                #                            start by guessing exponential to 1 with 30-yr efolding
                icount += 1

        # -----> initialize miuRatio decisions

        miuRatioDecisions = np.zeros((nDecisionTimes,nTechs-1))/nTechs # start at zero except first  
        miuRatioDecisions[:,0] = 1.0    
        miuRatioLower = np.zeros((nDecisionTimes,nTechs-1)) # create array of zeros        
        miuRatioUpper = np.ones((nDecisionTimes,nTechs-1)) # create array of ones 

        # -----> initialize savings decisions

        if info['optSavings']:


            savingsUpper = np.ones( nSavingDecisions )
            savingsLower = np.zeros(nSavingDecisions)
            savings = np.array([info['optlrsav'] for i in savingDecisionTimes])
            
            if nSavingDecisions != nSavingValues: # some are search for times
                
                decisionIndices = np.zeros( int(nSavingDecisions - nSavingValues ))
                
                iOdd = False
                icount = 0

                for idx in range(nSavingDecisions):
                    if savingDecisionTimes[idx] < 0:
                        iOdd = not(iOdd)
                        if iOdd:
                            savings[idx] = -savingDecisionTimes[idx]/(savingDecisionTimes[-1]-savingDecisionTimes[0])

            savings[-1] = 0.0 # assume last time period is zero as starting for optimizer
            
        else: # no savings
            savingsUpper = np.zeros(0)
            savingsLower = np.zeros(0)
            savings = np.zeros(0)


        # ----> put together actions

        #print (optTimes)
        #print(optTimesUpper)
        #print(optTimesLower)
        act = np.concatenate((miuDecisions,np.ravel(miuRatioDecisions),savings))
        actUpper = np.concatenate((miuUpper,np.ravel(miuRatioUpper),savingsUpper))
        actLower = np.concatenate((miuLower,np.ravel(miuRatioLower),savingsLower))

        ########################################################################
        ### Step 1: Problem definition     #####################################
        ########################################################################

        # Note that in this version, for computational reasons, the variables used for optimization differ 
        # from those used internally by the differential equation code.

        # In the code it makes sense to have miu[idxTech] for each tech. But numerically, it is better to have the sum of all miu's as the first variable
        # and then the fraction of the sum of miu's used by the first, second, nth technology.
        # the last technology with a decision gets the remainder.

        ########################################################################
        ### Step 1: Problem definition     #####################################
        ########################################################################

        problem = {} # Initialize dictionary containing problem specifications
        option  = {} # Initialize dictionary containing MIDACO options
    
        problem['@'] = self.wrapper # Handle for problem function name
    

        # STEP 1.B: Lower and upper bounds 'xl' & 'xu'
        #############################################
        #    # STEP 1.C: Starting point 'x'
        ##############################

    
        problem['x'] = list(act)  # initial guess for control variable, convert to list

        #actupper[30:] = [info['limmiu']] * (nDecisions-30)
    
        problem['xl'] = list(actLower) # initial guess for control variable, convert to list
        problem['xu'] = list(actUpper) # initial guess for control variable, convert to list
    
        # STEP 1.A: Problem dimensions
        ##############################
        problem['o']  = 1                       # Number of objectives 
        problem['n']  = len(act) # Number of variables (in total)
        problem['ni'] = 0                       # Number of integer variables (0 <= ni <= n) 
        problem['m']  = 0      # Number of constraints (in total)  [max and min on miu for each time step]
        problem['me'] = 0                       # Number of equality constraints (0 <= me <= m)
        
        ########################################################################
        ### Step 2: Choose stopping criteria and printing options    ###########
        ########################################################################
    
        # STEP 2.A: Stopping criteria 
        #############################
        #option['maxeval'] = 100000   # Maximum number of function evaluation (e.g. 1000000) 
        option['maxeval'] = info['maxeval']   # Maximum number of function evaluation (e.g. 1000000) 
        #option['maxeval'] = 1    # Maximum number of function evaluation TEST
        option['maxtime'] = 60*60*24 # Maximum time limit in seconds (e.g. 1 Day = 60*60*24) 
    
        # STEP 2.B: Printing options  
        ############################ 
        option['printeval'] = 10000   # Print-Frequency for current best solution (e.g. 1000) 
        option['save2file'] = 1     # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]

        ########################################################################
        ### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
        ########################################################################
    
        option['param1']  = 0       # ACCURACY  (only affects constrained problems)
        option['param2']  = info['SEED']       # SEED (integer)
        option['param3']  = 0       # FSTOP (integer)
        option['param4']  = 0     # ALGOSTOP (integer) 
        option['param5']  = info['EVALSTOPint'] + info['EVALSTOPtol'] # EVALSTOP  
        option['param6']  = info['FOCUS']     # FOCUS  
        option['param7']  = info['ANTS']    # ANTS  
        option['param8']  = info['KERNEL']      # KERNEL -- default zero  
        option['param9']  = 0.0     # ORACLE  
        option['param10'] = 0.0     # PARETOMAX
        option['param11'] = 0.0     # EPSILON  
        option['param12'] = 0.0     # BALANCE
        option['param13'] = 0.0     # CHARACTER
    
        ########################################################################
        ### Step 4: Choose Parallelization Factor   ############################
        ########################################################################
    
        #option['parallel'] = 1 # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
        option['parallel'] = info['parallel'] # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
    
        ########################################################################
        ############################ Run MIDACO ################################
        ########################################################################
   
        startdate = datetime.datetime.now()
        print(startdate.strftime("%d/%m/%Y %H:%M:%S"))
    
        info["saveOutput"] = False
    
        if os.getlogin()=='kcaldeira':
            MIDACO_KEY = b'Ken_Caldeira_(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        elif os.getlogin()=='CandiseHenry':
            MIDACO_KEY = b'Candise_Henry(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        else:
            MIDACO_KEY = b'Lei_Duan_____(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        
        solution = midaco.run( problem, option, MIDACO_KEY )
        print(solution['x'])
    
        enddate = datetime.datetime.now()
        print(enddate.strftime("%d/%m/%Y %H:%M:%S"))
        minutes_diff = (enddate - startdate).total_seconds() / 60.0
        print ('elapsed time = ',str(minutes_diff),' minutes')
    
        todayString = str(enddate.year) + str(enddate.month).zfill(2) + str(enddate.day).zfill(2) + '_' + \
        str(enddate.hour).zfill(2) + str(enddate.minute).zfill(2) + str(enddate.second).zfill(2)

        info["saveOutput"] = True
    
        utility,info = DICE_fun(solution['x'],state,info)

        info['utility'] = utility
        print(utility)
        root_dir = "."

        return [problem,option,solution,info]

# 
# %%
