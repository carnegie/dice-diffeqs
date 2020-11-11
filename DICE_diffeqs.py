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
 

The variable <initParams> contains all of the initParams and functions needed
to compute time derivatives.

<initParams> variables:
    gBack -- rate of cost-improvement of backstop technology (fraction per year)
    expcost2 -- exponent describing how abatement cost scales with abatement fraction
    t -- time in years from start of problem (not calendar year !)
    
<initParams> functions:
    L[t] -- population (people)
    sigma[t] -- carbon emissions per unit unabated economic output (tC/USD)
    miu[t] -- actions taken by the agent [actions are at specified times, this
              function step functions at each of the decision points
    al[t] -- total factor productivity, in units of amount of output in USD of 1 person
             with 1 USD of capital.
    etree[t] -- deforestation emissions
    
NOTE: If <initParams> is local in an environment, it is called <params>, but
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

def initStateParamsInfo(kwargs):
    # creates <initState> and <initParams>
    initState = {}  # state variables
    initParams = {} # driving variables
    initInfo = {} # diagnostic information
    
   #---------------------------------------------------------------------------
   #------- Unpack keyword arguments ------------------------------------------
   #---------------------------------------------------------------------------

    #-----> integration time step  
    
    if 'dt' in kwargs.keys():
        dt = kwargs['dt']
    else:
        dt = 1
    initParams['dt'] = dt 
    
   #-----> number of technolologies 
    
    if 'nTechs' in kwargs.keys():
        initParams['nTechs'] = kwargs['nTechs']
    else:
        initParams['nTechs'] = 1  # Default values always aimed to get as close as possible to default DICE   
    nTechs = initParams['nTechs']
   #-----> decisionTimes 
    
    if 'decisionTimes' in kwargs.keys():
        initParams['decisionTimes'] = kwargs['decisionTimes']
    else:
        initParams['decisionTimes'] = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]
    
       #-----> upper and lower bound on the sum of mius for each technology

    if 'limMiuLower' in kwargs.keys():
        initParams['limMiuLower'] = kwargs['limMiuLower']
    else:
        initParams['limMiuLower'] = len(initParams['decisionTimes'])*[0]  

    if 'limMiuUpper' in kwargs.keys():
        initParams['limMiuUpper'] = kwargs['limMiuUpper']
    else:
        initParams['limMiuUpper'] = len(initParams['decisionTimes'])*[1.2]  # DICE default
    
    # optimize on savings rate?

    if 'optSavings' in kwargs.keys():
        initParams['optSavings'] = kwargs['optSavings']
    else:
        initParams['optSavings'] = False

    # savings rate decision times?
      
    if 'savingDecisionTimes' in kwargs.keys():
        initParams['savingDecisionTimes'] = kwargs['savingDecisionTimes']
    else:
        initParams['savingDecisionTimes'] = decisionTimes

    #-----> techLearningCurve: Does the technology have a learning curve? 

    if 'techLearningCurve' in kwargs.keys():
        initParams['techLearningCurve'] = kwargs['techLearningCurve']
    else:
        initParams['techLearningCurve'] = nTechs*[False]

     #-----> techLearningSubsidy: Can this technology receive a learning subsidy? 
     # Note: Learning curve subsidies do not apply to technologies without learning curves
     # A False value for this option functions as expected only if there is at least one technology present without a learning curve.

    if 'techLearningSubsidy' in kwargs.keys():
        initParams['techLearningSubsidy'] = kwargs['techLearningSubsidy']
    else:
        initParams['techLearningSubsidy'] = nTechs*[True]

    #-----> number of technolology decisions per time step
    # basic concept is that learning curve with no special subsidy gets to match the lowest price.
    # only works if other things are in the market. 
    
    nDecisionTechs = 0
    for idxTech in list(range(nTechs)):
        if not ( not initParams['techLearningSubsidy'][idxTech] and initParams['techLearningCurve'][idxTech]):
            nDecisionTechs += 1
    initParams['nDecisionTechs'] = nDecisionTechs  # Default values always aimed to get as close as possible to default DICE   
  
     #-----> techInitCost

    if 'techInitCost' in kwargs.keys():
        initParams['techInitCost'] = kwargs['techInitCost']
    else:
        initParams['techInitCost'] = nTechs*[550.]
       
      
     #-----> techInitAmount

    if 'techInitAmount' in kwargs.keys():
        initParams['techInitAmount'] = kwargs['techInitAmount']
    else:
        initParams['techInitAmount'] = nTechs*[0.] # Note: techInitAmount must be specified if this technology has a learning curve.
    initState['cumAbateTech'] = initParams['techInitAmount']  

     #-----> techLearningRate:  Improvement per year if no learning rate, else exponent on power law

    if 'techLearningRate' in kwargs.keys():
        initParams['techLearningRate'] = kwargs['techLearningRate']
    else:
        initParams['techLearningRate'] = nTechs*[ 1.-(1.-0.025)**0.2] # Nominally 0.5% per year but slightly different to be more consistent with DICE
  
   #-----> firstUnitFractionalCost
 
    if 'firstUnitFractionalCost' in kwargs.keys():
        initParams['firstUnitFractionalCost'] = kwargs['firstUnitFractionalCost']
    else:
        initParams['firstUnitFractionalCost'] = nTechs*[0.]  # vanilla DICE

    #-----> utilityOption
 
    if 'utilityOption' in kwargs.keys():
        initParams['utilityOption'] = kwargs['utilityOption']
    else:
        initParams['utilityOption'] = 0  # vanilla DICE       
           
    #if 'innovationRatio' in kwargs.keys() and (initParams['learningCurveOption'] == 4 or   initParams['learningCurveOption'] == 4):
    #    initParams['innovationRatio'] = kwargs['innovationRatio']
  
   #----->       damageCostRatio = 1.0 by default (ratio of climate damage cost to default value).
 
    if 'damageCostRatio' in kwargs.keys():
        initParams['damageCostRatio'] = kwargs['damageCostRatio']
    else:
        initParams['damageCostRatio'] = 1.0  # default to DICE default
  
   #----->       abatementCostRatio = 1.0 by default (ratio of abatement cost to default value).
 
    if 'abatementCostRatio' in kwargs.keys():
        initParams['abatementCostRatio'] = kwargs['abatementCostRatio']
    else:
        initParams['abatementCostRatio'] = 1.0  # default to DICE default
       
 
   #----->       parallel =  # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
   # number of cores to use, 0 or 1 is single core,
 
    if 'parallel' in kwargs.keys():
        initParams['parallel'] = kwargs['parallel']
    else:
        initParams['parallel'] = 1  # default to 1 core

    #-----> maximumm number of iterations 

    if 'maxeval' in kwargs.keys():
        initParams['maxeval'] = kwargs['maxeval']
    else:
        initParams['maxeval'] = 1000
       
    #---------------------------------------------------------------------------
    #------- Process information about time -------- ---------------------------
    #---------------------------------------------------------------------------

       
    timeEnd = max(initParams['decisionTimes'] )
    initParams['timeEnd'] = timeEnd
    tlist = np.arange(0,timeEnd+dt,dt)
    initParams['tlist'] = tlist
    nTimeSteps = len(tlist)
    initParams['nTimeSteps'] = nTimeSteps
   
    #---------------------------------------------------------------------------
    #------- Get various DICE parameter values ---------------------------------
    #---------------------------------------------------------------------------

    
    #** Preferences
    initParams['elasmu'] = 1.45 # Elasticity of marginal utility of consumption     /1.45 /
    if 'prstp' in kwargs.keys():
        initParams['prstp'] = kwargs['prstp'] #   Initial rate of social time preference per year   /.015  /
    else:
        initParams['prstp'] = 0.015 #   Initial rate of social time preference per year   /.015  /
    initParams['rr'] = (1./(1.+initParams['prstp']))** tlist

    
    #** Population and technology
    gama = 0.3 #     Capital elasticity in production function    initParams['/.300    /
    initParams['gama'] = gama
    initParams['dk'] = 0.1 #      Depreciation rate on capital (per year)          /.100    /
    
    initParams['optlrsav'] = (initParams['dk'] + 0.004)/(initParams['dk'] + 0.004*initParams['elasmu'] + initParams['prstp'])*initParams['gama']
    
    pop0 = 7403 * 1.e6 #  in people, not millions    Initial world population 2015 (millions)         /7403    /
    initParams['pop0'] = pop0
    initParams['popadj'] = 1- (1-0.134)**0.2  #  Assumption is original is per 5 year period;  Growth rate to calibrate to 2050 pop projection  /0.134   /
    initParams['popasym'] =   11500 * 1.e6 # Asymptotic population (millions)                 /11500   /
    #popList = []
    #pop = pop0
    #for t in np.arange(0.0,timeEnd+dt,dt):
    #    popList.append(pop)
    #    pop = pop * (popasym / pop)** popadj
    #initParams['popList'] = popList
    initParams['L'] = initParams['popasym']*(initParams['popasym']/initParams['pop0'])**-((1-initParams['popadj'])**tlist )
    
    
    # initParams['q0'] =       Initial world gross output 2015 (trill 2010 USD) /105.5   /
    k0 = 223 * 1.e12 # in USD, not trillions USD      Initial capital value 2015 (trill 2010 USD)      /223     /
    initState['k'] = k0
     
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
    initParams['al'] = alList
    
    e0 =  35.85 * 1.e9  # in tCO2/yr     Industrial emissions 2015 (GtCO2 per year)           /35.85    /
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
    initParams['gsigList'] = gsigList
    initParams['sigma'] = sigList
    
    initParams['eland0'] = 2.6 * 1.e9  # tCO2/yr  Carbon emissions from land 2015 (GtCO2 per year)     / 2.6    /
    initParams['deland'] = 1.-(1.- 0.115)**0.2  #  Decline rate of land emissions (per year)          / .115   /
    initParams['etree'] =  initParams['eland0']*(1-initParams['deland'])**tlist

    #** Carbon cycle

    #* Initial Conditions
    initState['mat'] = 851 * 1e9 * 44/12. # tCO2 equivalent  Initial carbon content of atmosphere 2015 (GtC)        /851    /
    initState['mu'] =  460 * 1e9 * 44/12. # tCO2 equivalent    Initial carbon content of upper strata 2015 (GtC)      /460    /
    initState['ml'] =  1740 * 1e9 * 44/12. # tCO2 equivalent    Initial carbon content of lower strata 2015 (GtC)      /1740   /
    
    initParams['mateq'] = 588 * 1e9 * 44/12. # tCO2 equivalent   Equilibrium concentration atmosphere  (GtC)           /588    /
    initParams['mueq'] =   360 * 1e9 * 44/12. # tCO2 equivalent  Equilibrium carbon content of upper strata (GtC)       /360    /
    initParams['mleq'] =  1720 * 1e9 * 44/12. # tCO2 equivalent   Equilibrium carbon content of lower strata (GtC)       /1720   /

    #* Flow initParamsaters
    initParams['b12'] = 1.- (1.-0.12)**0.2  
    # b12   Carbon cycle transition matrix in units of change per 5 year period                     /.12   /
    initParams['b23'] = 1.- (1.-0.007)**0.2  #   Carbon cycle transition matrix                      /0.007 /

    #** Climate model initParams
    initParams['t2xco2'] = 3.1 #  Equilibrium temp impact (oC per doubling CO2)    / 3.1  /
    initParams['fex0'] =  0.5 #   2015 forcings of non-CO2 GHG (Wm-2)              / 0.5  /
    initParams['fex1'] =  1.0 #   2100 forcings of non-CO2 GHG (Wm-2)              / 1.0  /
    
    initState['tocean'] = 0.0068 #  Initial lower stratum temp change (C from 1900)  /.0068 /
    initState['tatm'] =  0.85 #  Initial atmospheric temp change (C from 1900)    /0.85  /
    
    initParams['c1'] =   1. - (1.-0.1005)**0.2  #
    # c1 is heat capacity in strange units
    # Nordhaus's units are temperature change per 5 years per 1 W/m2 radiative imbalance.
    # Climate equation coefficient for upper level     /0.1005  /
    # We will multiply by 0.2 to make it in units of per year instead of 5 years.
    
    initParams['c3'] =  1.-(1.-0.088)**0.2  # equilibrartion per year of atmosphere to ocean
    # Transfer coefficient upper to lower stratum      /0.088   /
    initParams['c4'] =   1.-(1.-0.025)**0.2  # equilibrartion per year of ocean temperature to atmosphere            /0.025   /
    initParams['fco22x'] = 3.6813 #  Forcings of equilibrium CO2 doubling (Wm-2)      /3.6813  /
    initParams['forcoth']=  np.interp(tlist,[0.,85.],[0.5,1.0])
    #** Climate damage initParams

    initParams['a1'] = 0. #       Damage intercept                                 /0       /
    initParams['a2'] = 0.00236  #       Damage quadratic term                            /0.00236 /
    initParams['a3'] = 2.00  #       Damage exponent                                  /2.00    /
    
    #** Abatement cost
    initParams['expcost2'] = 2.6 #  Exponent of control cost function               / 2.6  /

    #initParams['tnopol'] =    Period before which no emissions controls base  / 45   /
    #initParams['cprice0'] =   Initial base carbon price (2010$ per tCO2)      / 2    /
    #initParams['gcprice'] =   Growth rate of base carbon price per year       /.02   /

    # -----------------------------------------------------------------
    # create dictionary for diagnostic output.
    # All items are numpy arrays with first dimension as time, and second dimension as tech if available

    timeShape = np.zeros(nTimeSteps)
    timeTechShape = np.zeros((nTimeSteps,nTechs))

    # state variables

    initInfo['tatm'] = timeShape.copy()
    initInfo['tocean'] = timeShape.copy()
    initInfo['mat'] = timeShape.copy()
    initInfo['mu'] = timeShape.copy()
    initInfo['ml'] = timeShape.copy()
    initInfo['k'] = timeShape.copy()
    initInfo['cumAbateTech'] = timeTechShape.copy().copy() # not always a state variable

    # dstate variables

    initInfo['dtatm'] = timeShape.copy()
    initInfo['dtocean'] = timeShape.copy()
    initInfo['dmat'] = timeShape.copy()
    initInfo['dmu'] = timeShape.copy()
    initInfo['dml'] = timeShape.copy()
    initInfo['dk'] = timeShape.copy()
    initInfo['dcumAbateTech'] = timeTechShape.copy().copy() # not always a state variable

    # informational

    initInfo['yGross'] = timeShape.copy()
    initInfo['damageFrac'] = timeShape.copy()
    initInfo['damages'] = timeShape.copy()
    initInfo['y'] = timeShape.copy()
    initInfo['c'] = timeShape.copy()
    
    initInfo['rsav'] = timeShape.copy()
    initInfo['inv'] = timeShape.copy()
    initInfo['cpc'] = timeShape.copy()
    initInfo['periodu'] = timeShape.copy()
    initInfo['cemutotper'] = timeShape.copy()
    
    initInfo['eGross'] = timeShape.copy()
    initInfo['eTot'] = timeShape.copy()
    initInfo['eInd'] = timeShape.copy()
    initInfo['abateAmount'] = timeShape.copy() 
    initInfo['abateAmountTech']  =  timeTechShape.copy().copy()
    initInfo['abateFrac'] = timeShape.copy()
    
    initInfo['abateCost'] = timeShape.copy()
    initInfo['abateCostTech']  =  timeTechShape.copy().copy()
    
    initInfo['pBackTime']  =  timeTechShape.copy().copy()  
    
    initInfo['mcAbate'] = timeShape.copy()
    initInfo['mcAbateTech'] = timeTechShape.copy()
    
    initInfo['miu'] = timeShape.copy() 
    # initInfo['miuTech'] = timeTechShape.copy() -- in params
        
    initInfo['force'] = timeShape.copy()
    initInfo['outgoingLW'] = timeShape.copy() 
    initInfo['sigma'] = timeShape.copy() 
    
    return initState,initParams,initInfo


def dstatedt(state, params, info):

    # note: state is a dictionary of scalars of current state of the system
    #       everything else is either a vector of length time, or an array of time x nTechs
    
    dstate = {}
    epsilon = 1.e-20 # small number (almost zero)
    bignum = 1.e20 # big number (almost infinity)
    
    # these three get created just because they get used alot
    idxTime = params['idxTime']
    nTechs = params['nTechs']
    expcost2 = params['expcost2']
    firstUnitFractionalCost = params['firstUnitFractionalCost']  

    # these get created because they get updated
    miu = info['miu']
    miuTech = params['miuTech']
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

    #-------------------------------------------------------------------------
    # Gross domestic product GROSS of damage and abatement costs at t ($ 2005 per year)
    yGross[idxTime] = (params['al'][idxTime]  * params['L'][idxTime] **(1 - params['gama'])) * (max(state['k'],epsilon)**params['gama'])

    eGross[idxTime] = yGross[idxTime] * params['sigma'][idxTime] # what industrial emissions would be in the absence of abatement

    #-------------------------------------------------------------------------------------------------
    #-------  Stuff related to abatement cost comes next  --------------------------------------------
    #-------------------------------------------------------------------------------------------------
    # compute pBackTime

    for idxTech in list(range(nTechs)):
        if params['techLearningCurve'][idxTech]:
            #Learning curve
            pBackTime[idxTime,idxTech] =  (
                params['abatementCostRatio'] * params['techInitCost'][idxTech]*
                (state['cumAbateTech'][idxTech]/params['techInitAmount'][idxTech]) ** -params['techLearningRate'][idxTech]
            )
        else:
            # DICE-like representation
            pBackTime[idxTime,idxTech] = (
                params['abatementCostRatio'] * params['techInitCost'][idxTech] * 
                (1 - params['techLearningRate'][idxTech])**(idxTime*params['dt']) 
            )

    # marginal cost of abatement is assumed to be the minimum of the above values    for idxTech in list(range(nTechs)):

    mcAbate[idxTime] = 1.e20
    for idxTech in list(range(nTechs)):
        if params['techLearningSubsidy'][idxTech] or not params['techLearningCurve'][idxTech]:
            mcAbateTech[idxTime,idxTech] =   pBackTime[idxTime,idxTech] *(firstUnitFractionalCost[idxTech] + (1.0 - firstUnitFractionalCost[idxTech])* miuTech[idxTime,idxTech]**(expcost2 - 1.0))
            mcAbate[idxTime] = min(mcAbate[idxTime],mcAbateTech[idxTime,idxTech]) 

    # --------- handle learning curve with no learning subsidy as a special case after these cases are done
    #------------ now handle no subsidy learning curve case
    for idxTech in list(range(nTechs)):
        if  not params['techLearningSubsidy'][idxTech] and params['techLearningCurve'][idxTech]:

            if mcAbate[idxTime] < pBackTime[idxTime,idxTech] * firstUnitFractionalCost[idxTech] and pBackTime[idxTime,idxTech] > 0:
                miuTech[idxTime,idxTech] = (
                    ((-mcAbate[idxTime] + pBackTime[idxTime,idxTech]*firstUnitFractionalCost[idxTech])/
                    (pBackTime[idxTime,idxTech]*(-1. + firstUnitFractionalCost[idxTech])))**(1/(expcost2 - 1.0))
                )
                mcAbateTech[idxTime,idxTech] = mcAbate[idxTime]
            else:
                miuTech[idxTime,idxTech] =  0.0 # This case doesn't really make sense. If pBackTime == 0 , it can't hope to equal marginal cost of pBackTime0   
                mcAbateTech[idxTime,idxTech] =  pBackTime[idxTime,idxTech]*firstUnitFractionalCost[idxTech]  


    miu[idxTime] = 0.0

    abateCost[idxTime] = 0.0
    for idxTech in list(range(nTechs)):
        miu[idxTime] += miuTech[idxTime,idxTech] 
            
        abateCostTech[idxTime,idxTech] = (
            eGross[idxTime] *  pBackTime[idxTime,idxTech] * 
            ( firstUnitFractionalCost[idxTech] * miuTech[idxTime,idxTech]  + (1.0 - firstUnitFractionalCost[idxTech] ) *  miuTech[idxTime,idxTech]**expcost2 / expcost2) 
        )
        abateCost[idxTime] += abateCostTech[idxTime,idxTech]

        abateAmountTech[idxTime,idxTech] = eGross[idxTime]  * miuTech[idxTime,idxTech]
        abateAmount[idxTime] += abateAmountTech[idxTime,idxTech] 

    # Industrial CO2 emission at t (tCO2)
    eInd[idxTime] =  eGross[idxTime]  - abateAmount[idxTime] # industrial emissions

    # Forest-related CO2 emissions
    # Total CO2 emission at t (tCO2)
    eTot[idxTime] = eInd[idxTime] + params['etree'][idxTime] 
                
    abateFrac[idxTime] = abateCost[idxTime] / yGross[idxTime]    # <abateCost> is total of abatement this time step 

    # Climate damage cost at t
    damageFrac[idxTime] = params['damageCostRatio'] * ( params['a1'] * state['tatm'] + params['a2'] * state['tatm']**params['a3'] )
    damages[idxTime] = yGross[idxTime] * damageFrac[idxTime]

    # Gross domestic product NET of damage and abatement costs at t ($ 2005 per year)
    y[idxTime] = yGross[idxTime] - damages[idxTime] - abateCost[idxTime]

    # Investment at time t
    if params['optSavings']:
        rsav[idxTime] = params['savings'][idxTime] 
    else:
        rsav[idxTime] = params['optlrsav']
    inv[idxTime] = rsav[idxTime] * y[idxTime]

    # Consumption ($ 2005)
    c[idxTime] = y[idxTime] - inv[idxTime]

    # Consumption per capita ($ per person per year)
    cpc[idxTime] = c[idxTime] / params['L'][idxTime] 

    # Utility per capita (one period utility function)
    if params['utilityOption'] == 0:
        periodu[idxTime] = (max(0.001* cpc[idxTime],epsilon)**(1 - params['elasmu']) - 1)/(1 - params['elasmu']) - 1 # Vanilla Dice
        # This ugly scaling by 0.001 is intended to keep utility numbers the same as what Nordhaus had
    else:  # utilityOption == 1 --> optimize on consumption
        periodu[idxTime] = max(cpc[idxTime],epsilon)

    # Period utility
    cemutotper[idxTime] = periodu[idxTime] *params['L'][idxTime]  * params['rr'][idxTime] 

    # ----------- create tendencies

    # Time rate of change of capital
    dstate['k'] = inv[idxTime] - params['dk']* state['k'] 
   
    
    #--------------------------------------------------------------------------
    # Next climate

    force = params['fco22x'] * np.log2(max(state['mat'],epsilon)/params['mateq']) + params['forcoth'][idxTime]
    outgoingLW = params['fco22x'] * state['tatm'] / params['t2xco2']
    
    # Atmospheric temperature at t+1
    dstate['tatm'] =  params['c1'] * (force - outgoingLW) + params['c3'] * (state['tocean'] - state['tatm'])
        
    # Deep ocean temperature at t+1
    dstate['tocean'] =  params['c4'] * (state['tatm'] - state['tocean'])
    
    #--------------------------------------------------------------------------
    # Next do carbon
    #b11 = 1. - params['b12']
    #b21 = params['b12']*params['mateq']/params['mueq']
    #b22 = 1 - b21 - params['b23'];
    #b32 = params['b23']*params['mueq']/params['mleq'] 
    #b33 = 1 - b32 

    # Atmospheric C carbon content ofcrease at t+1 (tC from 1750)
    dstate['mat'] = eTot[idxTime] + params['b12'] * (state['mu']*params['mateq']/params['mueq'] - state['mat'] )
    
    # Shallow ocean C carbon content ofcrease at t+1 (tC from 1750)
    dstate['mu'] = params['b12'] * ( state['mat'] - state['mu']*params['mateq']/params['mueq']) + \
                   params['b23']*  ( state['ml']*params['mueq']/params['mleq'] - state['mu'])
    
    # Deep ocean C carbon content crease at t+1 (tC from 1750)
    dstate['ml'] = params['b23']*( state['mu'] - state['ml']*params['mueq']/params['mleq'])

    dstate['cumAbateTech'] = abateAmountTech[idxTime]
        
    #-------------------------------------------------------------------------

    # note only need to add things here that are not 
    # tendencies for recording
    k[idxTime] = state['k']
    dk[idxTime] = dstate['k']
    tatm[idxTime] = state['tatm']
    dtatm[idxTime] = dstate['tatm']
    tocean[idxTime] = state['tocean']
    dtocean[idxTime] = dstate['tocean']
    mat[idxTime] = state['mat']
    dmat[idxTime] = dstate['mat']
    mu[idxTime] = state['mu']
    dmu[idxTime] = dstate['mu']
    ml[idxTime] = state['ml']
    dml[idxTime] = dstate['ml']
    cumAbateTech[idxTime] = state['cumAbateTech']

    return dstate

def dictAddEach(x, x0):
    for key in x0:
        if key in x:
            x[key] = x[key] + x0[key]
        else:
            x[key]= x0[key]
     

def dictAddEachMultiply(x, x0, x1):
    for key in x0:
        if key in x:
            x[key] = x[key] + x1 * x0[key]
        else:
            x[key]= x0[key]

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



def DICE_fun(decisions,initState,initParams,initInfo):
    # Initially we are going to assume that the only decision are the abatement
    # level MIU.
    # relies on globals <initState> and <initParams>

    # NOTE: decisions is first the various miu values, then rsav if present

    state = copy.deepcopy(initState)  # seems like this could be made more efficient by only making copies of the parts that need copies
    params = copy.deepcopy(initParams)  # seems like this could be made more efficient by only making copies of the parts that need copies
    info = copy.deepcopy(initInfo)  # seems like this could be made more efficient by only making copies of the parts that need copies

    nDecisionTimes = len(params['decisionTimes'])
    nSavingDecisionTimes = len(params['savingDecisionTimes'])
    nTechs = params['nTechs']   
    tlist = params['tlist']
    dt = params['dt']
    nTimeSteps = params['nTimeSteps']
    params['decisions'] = decisions
  

    miuTech = np.zeros((nTimeSteps,nTechs))
    idxTechDecision = 0
    for idxTech in list(range(nTechs)):
        if not ( not params['techLearningSubsidy'][idxTech] and params['techLearningCurve'][idxTech] ):
            miuTech[:,idxTech] = np.interp(tlist,params['decisionTimes'],decisions[idxTechDecision*nDecisionTimes:(idxTechDecision+1)*nDecisionTimes])
            idxTechDecision += 1
        else:
            miuTech[:,idxTech] = 0
    params['miuTech'] = miuTech

    if params['optSavings']:
        params['savings'] = np.interp(tlist,params['savingDecisionTimes'],decisions[-nSavingDecisionTimes:])
    
    for idxTime in list(range(params['nTimeSteps'])):
        params['idxTime'] = idxTime
         
        dstate = dstatedt(state, params, info)  # params is a global used by dstatedt
        
        # eulers method (1 is OK, 0.5 seems fine)
        for key in state:
            state[key] +=  dt * dstate[key]

    #print (1.e-9*float(np.sum(info['cemutotper'])))
    #print('decisions')
    #print(decisions) 
    #print('params[miuTech]')
    #print(params['miuTech']) 

    return float(np.sum(info['cemutotper'])),info

#############################################################################
#####    Main DICE Function                              ####################
#####    Class is used to transfer data among functions  ####################
#############################################################################

class DICE_instance:

    def __init__(self, **kwargs):

        initState, initParams, initInfo = initStateParamsInfo(kwargs)

        self.initState = initState
        self.initParams = initParams
        self.initInfo = initInfo       
        self.out = self.runDICEeq() 
    
    def wrapper(self, act):

        initState = self.initState
        initParams = self.initParams
        initInfo = self.initInfo

        welfare, info = DICE_fun(act,initState,initParams,initInfo)

        # keep the sum of the mius of all of the technologies within the time dependent bounds.
        # #  Inequality constraints G(X) >= 0 
        miuDecisions = info['miu'][initParams['decisionTimes']]
        gConstraints = list(miuDecisions - initParams['limMiuLower']) + list(initParams['limMiuUpper'] - miuDecisions)

        # "Without loss of generality, all objectives are subject to minimization."
        # http://www.midaco-solver.com/data/other/MIDACO_User_Manual.pdf

        #print( 'info[miu]')
        #print( info['miu']  )
        ##print( 'miuDecisions')
        #print( miuDecisions  )
        #print( 'act')
        #print( act)
        #print('result')
        #print ( [[-welfare],list(gConstraints)])

        return [[-welfare],gConstraints]

    def runDICEeq(self):

        initState = self.initState
        initParams = self.initParams
        initInfo = self.initInfo
        
        decisionTimes = initParams['decisionTimes']
        savingDecisionTimes = initParams['savingDecisionTimes']

        nDecisionTimes = len(initParams['decisionTimes'])
        nSavingDecisionTimes = len(initParams['savingDecisionTimes'])

        nTechs =  initParams['nTechs'] # total number of technologies in resuls
        nDecisionTechs = initParams['nDecisionTechs']

        if initParams['optSavings']:
            nDecisions = nDecisionTimes * nDecisionTechs + nSavingDecisionTimes
        else:
            nDecisions = nDecisionTimes * nDecisionTechs
    
        ########################################################################
        ### Step 1: Problem definition     #####################################
        ########################################################################
        
        actUpper = [1.0] * nDecisions
        actUpper[:nDecisionTimes*nDecisionTechs] = [initParams['limMiuUpper'][np.mod(i,nDecisionTimes)] for i in list(range(nDecisionTimes*nDecisionTechs))]

        actLower = [0] * nDecisions

        act0 = np.array(actUpper)*0.5/nTechs # Start assuming each technology contributes equally to half of max

        if initParams['optSavings']:
            actUpper[-nSavingDecisionTimes:] =  [1.0] * nSavingDecisionTimes
            act0[-nSavingDecisionTimes:] = [initParams['optlrsav'] for i in initParams['savingDecisionTimes']]
            act0[-1] = 0.0 # assume last time period is zero

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

    
        problem['x'] = list(act0)  # initial guess for control variable, convert to list

        #actupper[30:] = [initParams['limmiu']] * (nDecisions-30)
    
        problem['xl'] = list(actLower) # initial guess for control variable, convert to list
        problem['xu'] = list(actUpper) # initial guess for control variable, convert to list
    
        # STEP 1.A: Problem dimensions
        ##############################
        problem['o']  = 1                       # Number of objectives 
        problem['n']  = int(nDecisions) # Number of variables (in total)
        problem['ni'] = 0                       # Number of integer variables (0 <= ni <= n) 
        problem['m']  = 2 * nDecisionTimes      # Number of constraints (in total)  [max and min on miu for each time step]
        problem['me'] = 0                       # Number of equality constraints (0 <= me <= m)
        
        ########################################################################
        ### Step 2: Choose stopping criteria and printing options    ###########
        ########################################################################
    
        # STEP 2.A: Stopping criteria 
        #############################
        #option['maxeval'] = 100000   # Maximum number of function evaluation (e.g. 1000000) 
        option['maxeval'] = initParams['maxeval']   # Maximum number of function evaluation (e.g. 1000000) 
        #option['maxeval'] = 1    # Maximum number of function evaluation TEST
        option['maxtime'] = 60*60*24 # Maximum time limit in seconds (e.g. 1 Day = 60*60*24) 
    
        # STEP 2.B: Printing options  
        ############################ 
        option['printeval'] = 10000   # Print-Frequency for current best solution (e.g. 1000) 
        option['save2file'] = 1     # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]

        ########################################################################
        ### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
        ########################################################################
    
        option['param1']  = 1.0e-6  # ACCURACY  
        option['param2']  = 1       # SEED (integer)
        option['param3']  = 0       # FSTOP (integer)
        option['param4']  = 100     # ALGOSTOP (integer) 
        option['param5']  = 0.0     # EVALSTOP  
        option['param6']  = 1e5     # FOCUS  
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
        option['parallel'] = initParams['parallel'] # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
    
        ########################################################################
        ############################ Run MIDACO ################################
        ########################################################################
   
        startdate = datetime.datetime.now()
        print(startdate.strftime("%d/%m/%Y %H:%M:%S"))
    
        initParams["saveOutput"] = False
    
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

        initParams["saveOutput"] = True
    
        utility,info = DICE_fun(solution['x'],initState,initParams,initInfo)
        print(utility*1.e-12)
        root_dir = "."

        return [problem,option,solution,initParams,info]
