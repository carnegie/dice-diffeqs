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
    etree[t] -- deforestation emissions
    
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
import utils
import copy
from plot_utilities import *
from scipy import interpolate
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
       
    timeEnd = max(info['decisionTimes'] )
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
        if COINmode:
            info['optSavings'] = True
        else:         
            info['optSavings'] = False

    #----------------------------------------------------------------------------------------------
    # savings rate decision times?

    if 'optSavingTimes' in kwargs.keys():
        info['optSavingTimes'] = kwargs['optSavingTimes'] 
    else:
        info['optSavingTimes'] = False
      
    if 'savingDecisionTimes' in kwargs.keys():
        info['savingDecisionTimes'] = kwargs['savingDecisionTimes']
    else:
        info['savingDecisionTimes'] = decisionTimes    # savings rate decision times?
      
    if 'splineDecisionTimes' in kwargs.keys():
        info['splineDecisionTimes'] = kwargs['splineDecisionTimes']
    else:
        info['splineDecisionTimes'] = False

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
        if COINmode:
            init['techInitCost'] = nTechs*[1.] #@@@@@@@@@@ COINmode @@@@@@@@@@@@
        else:
            info['techInitCost'] = nTechs*[550.]
       
      
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
        
    #-----> FOCUS midaco option 

    if 'FOCUS' in kwargs.keys():
        info['FOCUS'] = kwargs['FOCUS']
    else:
        info['FOCUS'] = 0
       

   
    #---------------------------------------------------------------------------
    #------- Get various DICE parameter values ---------------------------------
    #---------------------------------------------------------------------------
    info['tlist'] = tlist
    
    #** Preferences
    if COINmode:
        info['elasmu'] = 1
    else:
        info['elasmu'] = 1.45 # Elasticity of marginal utility of consumption     /1.45 /

    if 'prstp' in kwargs.keys():
        info['prstp'] = kwargs['prstp'] #   Initial rate of social time preference per year   /.015  /
    else:
        if COINmode:
            info['prstp'] = 0.03
        else:
            info['prstp'] = 0.015 #   Initial rate of social time preference per year   /.015  /
    info['rr'] = (1./(1.+info['prstp']))** tlist
    
    #** Population and technology
    gama = 0.3 #     Capital elasticity in production function    info['/.300    /
    info['gama'] = gama
    info['depk'] = 0.1 #      Depreciation rate on capital (per year)          /.100    /
     
    if 'cumETotInit' in kwargs.keys():
        state['cumETot'] = kwargs['cumETotInit'] # units of init emission equivalents 
    else:
        state['cumETot'] = 0.0  # cumulative emissions (tCO2)


    if COINmode:
        info['L']= [1]*nTimeSteps

        state['k']=1.0
        info['sigma'] = 1.01**-tlist # the units on sigma are relative to base case emissions
        #                              assumption is base case if sustained would warm 2 C in 100 years.
        info['etree'] = np.zeros(len(tlist))
        
        dela = 0.01
        info['al'] = (1.+dela)**tlist  # total factor productivity improving 1% per
        
        info['expcost2'] = 2 #  Exponent of control cost function               / 2.6  /

        info['alpha'] = 0.02 #   Assume 0.02 C warming per year initial condition emissions 
        #                        based on concept of 2 C warming in 100 years if sustained initial condition emissions

        info['a1'] = 0. #       Damage intercept                                 /0       /
        info['a2'] = 0.005 #    Fraction of GDP per degree of warming squared 9@% damages at 2 C temp increase
        info['a3'] = 2  #       Damage exponent                                  /2.00    /

        info['K0'] = 300.e12 # USD$ capital
        info['Y0'] = 100.e12 # USD$/yr gross production
         # q0 in vanilla DICE is 105.177 trillion USD.

        info['optlrsav'] = info['gama'] * ( info['depk'] + dela ) / ( info['depk'] + info['prstp'] )

        info['tau'] = info['gama']  / ( info['depk'] + info['prstp'] ) #  = info['K0']/info['Y0'] # time constant relating reference state gross production 
        print (info['optlrsav'],info['tau'])
    else:

        pop0 = 7403 * 1.e6 #  in people, not millions    Initial world population 2015 (millions)         /7403    /
        info['pop0'] = pop0
        info['popadj'] = 1- (1-0.134)**0.2  #  Assumption is original is per 5 year period;  Growth rate to calibrate to 2050 pop projection  /0.134   /
        info['popasym'] =   11500 * 1.e6 # Asymptotic population (millions)                 /11500   /
        #popList = []
        #pop = pop0
        #for t in np.arange(0.0,timeEnd+dt,dt):
        #    popList.append(pop)
        #    pop = pop * (popasym / pop)** popadj
        #info['popList'] = popList
        info['L'] = info['popasym']*(info['popasym']/info['pop0'])**-((1-info['popadj'])**tlist )

        k0 = 223 * 1.e12 # in USD, not trillions USD      Initial capital value 2015 (trill 2010 USD)      /223     /
        state['k'] = k0
    
        e0 =  35.85 * 1.e9  # in tCO2/yr     Industrial emissions 2015 (GtCO2 per year)           /35.85    /

        # info['q0'] =       Initial world gross output 2015 (trill 2010 USD) /105.5   /
        
        # al: Total factor productivity
        # Note that Nordhaus gave a value of 5.115 for total factor productivity.
        # This was in units of trillions of USD per population in millions raised 
        # to the 0.7 power times capital in trillions raised to the 0.3 power.
        
        # Since we are going to work in USD and people consistently, we need to convert
        # Nordhauses units into equivalents with 1 person with 1 USD of capital.
        # for this we need the factor
        
        cvt = 1.e12 * 1.e-9**(1-gama)*1.e-12**gama
        
        a0 = 5.115 *cvt #       Initial level of total factor productivity in $ for 1 person with 1 USD       /5.115    /
        ga0 =1.-(1.- 0.076)**0.2 #  per year    per year Initial growth rate for TFP per 5 years          /0.076   /
        dela = 0.005 #    Decline rate of TFP per year (not 5 as stated !!!)                  /0.005   /
        ga = ga0 * np.exp(-dela * tlist)
        
        #     ga(t)=ga0*exp(-dela*5*((t.val-1)));
        #     al("1") = a0; loop(t, al(t+1)=al(t)/((1-ga(t))););
        
        alList = []
        a = a0
        idx = 0
        for t in tlist:
            alList.append(a)
            a = a / (1. - ga[idx])**dt
            idx += 1
        info['al'] = alList
        
        
        miu0 = 0.03 #    Initial emissions control rate for base case 2015    /.03     /  # This is used only for getting initial value of sigma
        # q0 = 105.5 * 1.e12 # USD      Initial world gross output 2015 (trill 2010 USD) /105.5   /
        q0 = a0 * pop0**(1.-gama)*k0**gama     # q0 is yGross at time 0
        # q0 in vanilla DICE is 105.177 trillion USD.

        sig = e0/(q0*(1-miu0))    # <sig> and <sigma> have units of tCO2 per USD ouput.
        # This contrasts with the original DICE which is GtCO2/trillion-USD
        # Therefore this sigma should be 10**-9 / 10**-12 = 1000 times bigger.
        # sig = 6508.5


        #    gsig("1")=gsigma1; loop(t,gsig(t+1)=gsig(t)*((1+dsig)**tstep) ;);
        #    sigma("1")=sig0;   loop(t,sigma(t+1)=(sigma(t)*exp(gsig(t)*tstep)););

        # sigma: ratio of emissions to unabated GDP (carbon intensity on unabated economy)
        gsigma1 = -0.0152 # Initial growth of sigma (per year)                   /-0.0152 /
        dsig =  -0.001    # Decline rate of decarbonizationper period       /-0.001  /
        gsig = gsigma1
        gsigList = []
        sigList = []

        for t in tlist:
            gsig = gsigma1 * (1 + dsig)**t
            gsigList.append(gsig) # This has to come after updating of gsig
            sigList.append(sig)  # This has to come before updating of sig
            sig = sig *np.exp(gsig * dt)

        info['gsigList'] = gsigList
        info['sigma'] = sigList

        info['eland0'] = 2.6 * 1.e9  # tCO2/yr  Carbon emissions from land 2015 (GtCO2 per year)     / 2.6    /
        info['deland'] = 1.-(1.- 0.115)**0.2  #  Decline rate of land emissions (per year)          / .115   /
        info['etree'] =  info['eland0']*(1-info['deland'])**tlist

        #** Carbon cycle

        #* Initial Conditions
        state['mat'] = 851 * 1e9 * 44/12. # tCO2 equivalent  Initial carbon content of atmosphere 2015 (GtC)        /851    /
        state['mu'] =  460 * 1e9 * 44/12. # tCO2 equivalent    Initial carbon content of upper strata 2015 (GtC)      /460    /
        state['ml'] =  1740 * 1e9 * 44/12. # tCO2 equivalent    Initial carbon content of lower strata 2015 (GtC)      /1740   /

        info['mateq'] = 588 * 1e9 * 44/12. # tCO2 equivalent   Equilibrium concentration atmosphere  (GtC)           /588    /
        info['mueq'] =   360 * 1e9 * 44/12. # tCO2 equivalent  Equilibrium carbon content of upper strata (GtC)       /360    /
        info['mleq'] =  1720 * 1e9 * 44/12. # tCO2 equivalent   Equilibrium carbon content of lower strata (GtC)       /1720   /

        #* Flow initParamsaters
        info['b12'] = 1.- (1.-0.12)**0.2  
        # b12   Carbon cycle transition matrix in units of change per 5 year period                     /.12   /
        info['b23'] = 1.- (1.-0.007)**0.2  #   Carbon cycle transition matrix                      /0.007 /

        #** Climate model info
        info['t2xco2'] = 3.1 #  Equilibrium temp impact (oC per doubling CO2)    / 3.1  /
        info['fex0'] =  0.5 #   2015 forcings of non-CO2 GHG (Wm-2)              / 0.5  /
        info['fex1'] =  1.0 #   2100 forcings of non-CO2 GHG (Wm-2)              / 1.0  /

        state['tocean'] = 0.0068 #  Initial lower stratum temp change (C from 1900)  /.0068 /
        state['tatm'] =  0.85 #  Initial atmospheric temp change (C from 1900)    /0.85  /

        info['c1'] =   1. - (1.-0.1005)**0.2  #
        # c1 is heat capacity in strange units
        # Nordhaus's units are temperature change per 5 years per 1 W/m2 radiative imbalance.
        # Climate equation coefficient for upper level     /0.1005  /
        # We will multiply by 0.2 to make it in units of per year instead of 5 years.

        info['c3'] =  1.-(1.-0.088)**0.2  # equilibrartion per year of atmosphere to ocean
        # Transfer coefficient upper to lower stratum      /0.088   /
        info['c4'] =   1.-(1.-0.025)**0.2  # equilibrartion per year of ocean temperature to atmosphere            /0.025   /
        info['fco22x'] = 3.6813 #  Forcings of equilibrium CO2 doubling (Wm-2)      /3.6813  /
        info['forcoth']=  np.interp(tlist,[0.,85.],[0.5,1.0])
        #** Climate damage info

        info['a1'] = 0. #       Damage intercept                                 /0       /
        info['a2'] = 0.00236  #       Damage quadratic term                            /0.00236 /
        info['a3'] = 2.00  #       Damage exponent                                  /2.00    /

        #** Abatement cost
        info['expcost2'] = 2.6 #  Exponent of control cost function               / 2.6  /

        info['optlrsav'] = (info['depk'] + 0.004)/(info['depk'] + 0.004*info['elasmu'] + info['prstp'])*info['gama']
    

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
    info['tocean'] = timeShape.copy()
    info['mat'] = timeShape.copy()
    info['mu'] = timeShape.copy()
    info['ml'] = timeShape.copy()
    info['k'] = timeShape.copy()
    info['cumAbateTech'] = timeTechShape.copy() # not always a state variable

    # dstate variables

    info['dtatm'] = timeShape.copy()
    info['dtocean'] = timeShape.copy()
    info['dmat'] = timeShape.copy()
    info['dmu'] = timeShape.copy()
    info['dml'] = timeShape.copy()
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
    info['eTot'] = timeShape.copy()
    info['eInd'] = timeShape.copy()
    info['abateAmount'] = timeShape.copy() 
    info['abateAmountTech']  =  timeTechShape.copy()
    info['abateFrac'] = timeShape.copy()
    
    info['abateCost'] = timeShape.copy()
    info['abateCostTech']  =  timeTechShape.copy()
    
    info['pBackTime']  =  timeTechShape.copy()  
    
    info['mcAbate'] = timeShape.copy()
    info['mcAbateTech'] = timeTechShape.copy()
        
    info['force'] = timeShape.copy()
    info['outgoingLW'] = timeShape.copy() 

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

    if COINmode:
        tAtmState = info['alpha']*state['cumETot']
    else:
        tAtmState = state['tatm']
        tOceanState = state['tocean']
        mUState = state['mu']
        mLState = state['ml']
        mAtState = state['mat']
        mateq = info['mateq']
        mueq = info['mueq']
        mleq = info['mleq']
    
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
    eTot = info['eTot']

    force = info['force']
    outgoingLW = info['outgoingLW']

    # tendencies for recording
    k = info['k']
    dk = info['dk']
    tatm = info['tatm']
    dtatm = info['dtatm']
    tocean = info['tocean']
    dtocean = info['dtocean']
    mat = info['mat']
    dmat = info['dmat']
    mu = info['mu']
    dmu = info['dmu']
    ml = info['ml']
    dml = info['dml']
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
                (1 - info['techLearningRate'][idxTech])**(idxTime*info['dt']) 
            )

    #-------------------------------------------------------------------------------------------------
    #-------  Now we go through the logic of distributing miu values ----------------------------------

    #-------------------------------------------------------------------------

    # Climate damage cost at t
    tAtmDamage = max(0.0, tAtmState)  # do not consider damage function for temperatures < 0.

    damageFrac[idxTime] = info['damageCostRatio'] * ( info['a1'] * tAtmDamage + info['a2'] * tAtmDamage**info['a3'] )
    yGrossDICE =  (info['al'][idxTime]  * info['L'][idxTime] **(1 - info['gama'])) * (max(state['k'],epsilon)**info['gama'])
    if COINmode:
        yGross[idxTime] = (1 - damageFrac[idxTime]) 
    else:
        # Gross domestic product GROSS of damage and abatement costs at t ($ 2005 per year)
        yGross[idxTime] = yGrossDICE
    damages[idxTime] =  damageFrac[idxTime] * yGrossDICE

    eGross[idxTime] = yGross[idxTime] * info['sigma'][idxTime] # what industrial emissions would be in the absence of abatement


    mcAbate[idxTime] = 1.e20

    for idxTech in list(range(nTechs)):
        miuTech[idxTime,idxTech] = miu[idxTime] * miuRatios[idxTime,idxTech]
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

    dstate['cumAbateTech'] = abateAmountTech[idxTime]

    # Industrial CO2 emission at t (tCO2)
    eInd[idxTime] =  eGross[idxTime]  - abateAmount[idxTime] # industrial emissions

    # Forest-related CO2 emissions
    # Total CO2 emission at t (tCO2)
    eTot[idxTime] = eInd[idxTime] + info['etree'][idxTime] 
    dstate['cumETot'] = eTot[idxTime]

    abateFrac[idxTime] = abateCost[idxTime] / yGross[idxTime]    # <abateCost> is total of abatement this time step 

    # Gross domestic product NET of damage and abatement costs at t ($ 2005 per year)
    y[idxTime] = yGrossDICE - damages[idxTime] - abateCost[idxTime]

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

    if COINmode:
        dstate['k'] = inv[idxTime]/info['tau'] - info['depk']* state['k'] 
    else:
        dstate['k'] = inv[idxTime] - info['depk']* state['k'] 
   
    
    #--------------------------------------------------------------------------
    # Next climate

    if not COINmode:

        # Atmospheric temperature at t+1
        dstate['tatm'] =  info['c1'] * (force[idxTime] - outgoingLW[idxTime]) + info['c3'] * (tOceanState - tAtmState)
            
        force[idxTime] = info['fco22x'] * np.log2(max(mAtState,epsilon)/mateq) + info['forcoth'][idxTime]
        outgoingLW[idxTime] = info['fco22x'] * tAtmState / info['t2xco2']
        
        # Deep ocean temperature at t+1
        dstate['tocean'] =  info['c4'] * (tAtmState - tOceanState)
        
        #--------------------------------------------------------------------------
        # Next do carbon
        #b11 = 1. - info['b12']
        #b21 = info['b12']*mateq/mueq
        #b22 = 1 - b21 - info['b23'];
        #b32 = info['b23']*mueq/mleq 
        #b33 = 1 - b32 

        # Atmospheric C carbon content ofcrease at t+1 (tC from 1750)
        dstate['mat'] = eTot[idxTime] + info['b12'] * (mUState*mateq/mueq - mAtState )
        
        # Shallow ocean C carbon content ofcrease at t+1 (tC from 1750)
        dstate['mu'] = info['b12'] * ( mAtState - mUState*mateq/mueq) +  info['b23']*  ( mLState*mueq/mleq - mUState)
        
        # Deep ocean C carbon content crease at t+1 (tC from 1750)
        dstate['ml'] = info['b23']*( mUState - mLState*mueq/mleq)


        
    #-------------------------------------------------------------------------

    # note only need to add things here that are not 
    # tendencies for recording
    k[idxTime] = state['k']
    dk[idxTime] = dstate['k']
    cumAbateTech[idxTime] = state['cumAbateTech']

    if  COINmode:
        tatm[idxTime] = info['alpha']*state['cumETot']
    else:
        dtatm[idxTime] = dstate['tatm']
        tocean[idxTime] = tOceanState
        dtocean[idxTime] = dstate['tocean']
        mat[idxTime] = mAtState
        dmat[idxTime] = dstate['mat']
        mu[idxTime] = mUState
        dmu[idxTime] = dstate['mu']
        ml[idxTime] = mLState
        dml[idxTime] = dstate['ml']

    return dstate

#%%

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

    nDecisionTimes = len(info['decisionTimes'])
    nSavingDecisionTimes = len(info['savingDecisionTimes'])
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

    sequentialDecisions = np.reshape(act[icount:icount+nDecisionTimes * (nTechs-1)],(nTechs-1,nDecisionTimes)) 
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
        if info['optSavingTimes']:
            nOptSavingTimes = nSavingDecisionTimes - 2
            savingDecisionTimes = info['savingDecisionTimes']
            for idx in range(nOptSavingTimes):
                savingDecisionTimes[1+idx] = act[-nOptSavingTimes + idx]
            info['savingDecisionTimes'] = savingDecisionTimes
        else:
            nOptSavingTimes = 0
 
        savings = np.array(act[-(nSavingDecisionTimes+nOptSavingTimes):][:nSavingDecisionTimes]) # this works when nOptSavingsTimes == 0
        #print(savings)
        #print(act)
    else: # specified savings
        savings = np.array([info['optlrsav'] for item in info['savingDecisionTimes']])



    # ------------------------------------------------------------------------
    # 2. now interpolate across time steps
    # ------------------------------------------------------------------------   

    #  for miuratios, change from cumulative to actual ratios.
    #  i.e., on input if miu  = 0.8, and miuRatio = [0.25, 0.333333, 0.5]
    # we would have on cumulative (0.25 x 0.8) = 0.2; 0.8 - 0.2 = 0.6; (0.3333 * 0.6 ) = 0.2; ... 
    # or in terms of 
    # This would be converted to, miu = 0.8 and miuRatios = [0.25, 0.25, 0.25, 0.25]

    miu =  np.interp(tlist,info['decisionTimes'],miuDecisions)
    info['miu'] = miu

    miuRatios = np.zeros((nTimeSteps,nTechs))
    miuRemaining = np.ones(nTimeSteps)
    timeNull = -np.ones(nTimeSteps)
    for idxTech in list(range(nTechs)):
        miuRatios[:,idxTech] = np.interp(tlist,info['decisionTimes'],miuRatioDecisions[:,idxTech])
    info['miuRatios'] = miuRatios

    # -----------interpolate decision times; note decision times may not be monotonic if decision times are optimized
    if info['optSavingTimes']:
        xy = np.transpose((info['savingDecisionTimes'],savings))
        xy = xy[xy[:,0].argsort()]
        x = xy[:,0]
        y = xy[:,1]
        #print (xy,x,y)
    else:
        x = info['savingDecisionTimes']
        y = savings
    if info['splineDecisionTimes']:
        intCoeff = interpolate.splrep(x,y)
        info['savings']= interpolate.splev(tlist, intCoeff)
    else:
        #print(info['savingDecisionTimes'])
        #print(savings)
        info['savings'] = np.interp(tlist,x,y)
    
    # ------------------------------------------------------------------------
    # 3. now time step the action
    # ------------------------------------------------------------------------  

    for idxTime in list(range(info['nTimeSteps'])):
        info['idxTime'] = idxTime
         
        dstate = dstatedt(state, info)  # info is a global used by dstatedt
        
        # eulers method (1 is OK, 0.5 seems fine)
        for key in state:
            state[key] +=  dt * dstate[key]

    if COINmode:
        #obj = dt*np.sum(info['cemutotper'])+((state['k']-dt*dstate['k'])*(1+info['prstp'])**(-nTimeSteps*dt)-1)/info['tau']
        obj = dt*np.sum(info['cemutotper'])
    else:
        obj = np.sum(info['cemutotper'])

    return float(np.sum(info['cemutotper'])),info

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

        if info['COINmode']:
            ret = -welfare
        else:
            ret = -welfare*1.e-24
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
        nSavingDecisionTimes = len(info['savingDecisionTimes'])

        nTechs =  info['nTechs'] # total number of technologies in resuls
        COINmode = info['COINmode']

        limMiuUpper = info['limMiuUpper']
        limMiuLower = info['limMiuLower']

        # -----> initialize miu decisions

        nMiuDecisions = np.count_nonzero(limMiuUpper - limMiuLower) # This expression counts the number of different values

        miuDecisions = np.zeros(nMiuDecisions) # create empty vector        
        miuLower = np.zeros(nMiuDecisions) # create empty vector        
        miuUpper = np.zeros(nMiuDecisions) # create empty vector        
        icount = 0
        for idx in range(nDecisionTimes):
            if limMiuUpper[idx] > limMiuLower[idx]:
                miuLower[icount] = limMiuLower[idx]
                miuUpper[icount] = limMiuUpper[idx]
                miuDecisions[icount] = ( miuLower[icount] + miuUpper[icount] )/2.
                miuLower[icount]
                icount += 1

        # -----> initialize miuRatio decisions

        miuRatioDecisions = np.ones((nDecisionTimes,nTechs-1))/nTechs # start of assume all techs are created equal      
        miuRatioLower = np.zeros((nDecisionTimes,nTechs-1)) # create array of zeros        
        miuRatioUpper = np.ones((nDecisionTimes,nTechs-1)) # create array of ones 

        # -----> initialize savings decisions

        if info['optSavings']:
            savingsUpper = np.ones( nSavingDecisionTimes )
            savingsLower = np.zeros(nSavingDecisionTimes)
            savings = np.array([info['optlrsav'] for i in info['savingDecisionTimes']])
            savings[-1] = 0.0 # assume last time period is zero as starting for optimizer
        else: # no savings
            savingsUpper = np.zeros(0)
            savingsLower = np.zeros(0)
            savings = np.zeros(0)

        if info['optSavings'] and info['optSavingTimes']:
            optTimes = info['savingDecisionTimes'][1:-1] # first and last are fixed
            optTimesLower = np.array(optTimes)
            optTimesUpper = np.array(optTimes)
            optTimesLower[:] = info['savingDecisionTimes'][0]
            optTimesUpper[:] = info['savingDecisionTimes'][-1]
        else:
            optTimes = np.zeros(0)
            optTimesLower = np.zeros(0)
            optTimesUpper = np.zeros(0)

        # ----> put together actions

        #print (optTimes)
        #print(optTimesUpper)
        #print(optTimesLower)
        act = np.concatenate((miuDecisions,np.ravel(miuRatioDecisions),savings,optTimes))
        actUpper = np.concatenate((miuUpper,np.ravel(miuRatioUpper),savingsUpper,optTimesUpper))
        actLower = np.concatenate((miuLower,np.ravel(miuRatioLower),savingsLower,optTimesLower))

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
        option['param2']  = 1       # SEED (integer)
        option['param3']  = 0       # FSTOP (integer)
        option['param4']  = 100     # ALGOSTOP (integer) 
        option['param5']  = 0.0     # EVALSTOP  
        option['param6']  = info['FOCUS']     # FOCUS  
        option['param7']  = 0     # ANTS  
        option['param8']  = 0      # KERNEL  
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
        print(utility)
        root_dir = "."

        return [problem,option,solution,info]

# %%
