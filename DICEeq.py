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
    gback -- rate of cost-improvement of backstop technology (fraction per year)
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
#import scipy as sp
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

MIDACO_KEY = b'Ken_Caldeira_(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'

########################################################################
################### FUNCTIONS & OPTIMIZATION PROBLEM ###################
########################################################################

#%%

# Note: In the following function these keyword arguments are allowed:

#  decisionType == 1 --> opt on miu (default), 
#                  2 --> opt on miu and savings rate, 
#                  3 --> opt on savings rate

# learningCurveOption == 0 --> DICE formulation (default),
#                        1 --> single technology learning curve
#                        2 --> two technology learning curves

# if learningCurve is True, then the following keywords must be applied:

# learningCurveInitAmount --> initial cumulative abatement, default = 1
# learningCurveInitCost --> initial cost on leaning curve, default = $550 / tonCO2
# learningCurveExponent --> exponent on learning curve, 20% per doubling = 0.3219280948873623
#                                                       15% per doubling = 0.23446525363702297
#                                                       10% per doubling = 0.15200309344504995 (default)
#                                                        5% per doubling = 0.07400058144377693
0.13750352375

def createGlobalVariables(timeEnd,dt,decisionTimes,**kwargs):
    # creates <initState> and <initParams>
    print('returning  variables <initState> and <initParams>')
    #print(initState)
    initParams = {}
    initState = {}
    
    if 'decisionType' in kwargs.keys():
        initParams['decisionType'] = kwargs['decisionType']
    else:
        initParams['decisionType'] = 1
        
    if 'learningCurveOption' in kwargs.keys():
        initParams['learningCurveOption'] = kwargs['learningCurveOption']
        
        # --- Single learning curve
        
        if initParams['learningCurveOption'] == 1:
            if 'learningCurveInitAmount' in kwargs.keys():
                initParams['learningCurveInitAmount'] = kwargs['learningCurveInitAmount']
            else:
                initParams['learningCurveInitAmount'] = 1e10
            if 'learningCurveInitCost' in kwargs.keys():
                initParams['learningCurveInitCost'] = kwargs['learningCurveInitCost']
            else:
                initParams['learningCurveInitCost'] = 550
            if 'learningCurveExponent' in kwargs.keys():
                initParams['learningCurveExponent'] = kwargs['learningCurveExponent']
            else:
                initParams['learningCurveExponent'] = 0.15200309344504995 # 10% per doubling
            initParams['learningCurveConstant'] = \
                initParams['learningCurveInitCost']/initParams['learningCurveInitAmount']**-initParams['learningCurveExponent']
        
        # --- Two abatement technologies with two learning curves
        
        if initParams['learningCurveOption'] >= 2:
            if 'learningCurveInitAmount' in kwargs.keys():
                initParams['learningCurveInitAmount'] = kwargs['learningCurveInitAmount'] # should be a length 2 list
            else:
                initParams['learningCurveInitAmount'] = [1e10, 1e10]
            if 'learningCurveInitCost' in kwargs.keys():
                initParams['learningCurveInitCost'] = kwargs['learningCurveInitCost'] # should be a length 2 list
            else:
                initParams['learningCurveInitCost'] = [550, 550]
            if 'learningCurveExponent' in kwargs.keys():
                initParams['learningCurveExponent'] = kwargs['learningCurveExponent'] # should be a length 2 list
            else:
                initParams['learningCurveExponent'] = [0.15200309344504995, 0.15200309344504995] # 10% per doubling
            initParams['learningCurveConstant'] = [
                initParams['learningCurveInitCost'][0]/initParams['learningCurveInitAmount'][0]**-initParams['learningCurveExponent'][0],
                initParams['learningCurveInitCost'][1]/initParams['learningCurveInitAmount'][1]**-initParams['learningCurveExponent'][1]
                ]
    else:
        
        # --- Original DICE formulation
        
        initParams['learningCurveOption'] = 0
    
    if initParams['learningCurveOption'] == 1:  # single tech learning curve
        initState['cumAbate'] = initParams['learningCurveInitAmount']
    elif  initParams['learningCurveOption'] >= 2:  #  dual tech learning curves
        initState['cumAbate0'] = initParams['learningCurveInitAmount'][0]
        initState['cumAbate1'] = initParams['learningCurveInitAmount'][1]
        
    initParams['decisionTimes'] = decisionTimes

    initParams['timeEnd'] = timeEnd
    initParams['dt'] = dt
    tlist = np.arange(0,timeEnd+dt,dt)
    initParams['tlist'] = tlist
    
    #** Preferences
    initParams['elasmu'] = 1.45 # Elasticity of marginal utility of consumption     /1.45 /
    initParams['prstp'] = 0.015 #   Initial rate of social time preference per year   /.015  /
    initParams['rr'] = np.exp(-initParams['prstp'] * tlist)
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
    miu0 = 0.03 #    Initial emissions control rate for base case 2015    /.03     /
    # q0 = 105.5 * 1.e12 # USD      Initial world gross output 2015 (trill 2010 USD) /105.5   /
    q0 = a0 * pop0**(1.-gama)*k0**gama     # q0 is ygross at time 0
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
    initParams['pback'] = 550. #    Cost of backstop 2010$ per tCO2 2015            / 550  /
    initParams['gback'] = 1.-(1.-0.025)**0.2  #   per year  Initial cost decline backstop cost per period   / .025 /
        
    initParams['pbacktime'] = initParams['pback'] * (1 - initParams['gback'])**tlist # DICE-2016
    
    initParams['limmiu'] = 1.2 #   Upper limit on control rate after 2150          / 1.2 /
    #initParams['tnopol'] =    Period before which no emissions controls base  / 45   /
    #initParams['cprice0'] =   Initial base carbon price (2010$ per tCO2)      / 2    /
    #initParams['gcprice'] =   Growth rate of base carbon price per year       /.02   /

    
    return initState,initParams


#%%

def wrapper(act):
  #relies on globals <initState>, <initParams>
  global initState, initParams
  welfare, discard = DICE_fun(act,initState,initParams)
  
  dummy = 0.0
  # "Without loss of generality, all objectives are subject to minimization."
  # http://www.midaco-solver.com/data/other/MIDACO_User_Manual.pdf
  
  return [[-welfare],[dummy]]

#%%


def DICE_fun(decisions,initState,initParams):
    # Initially we are going to assume that the only decision are the abatement
    # level MIU.
    # relies on globals <initState> and <initParams>

    state0 = copy.deepcopy(initState)
    params = copy.deepcopy(initParams)
    nTimes = len(initParams['decisionTimes'])
            
    tlist = params['tlist']
    #print(decisions)
    params['decisions'] = decisions
    # <decision> is first miu, then savings rate if present and then miuRatio if present
    if params['decisionType'] == 1: # optimize on miu only
        params['miu'] = np.interp(tlist,params['decisionTimes'],decisions[:nTimes])
    elif params['decisionType'] == 2:

        params['miu'] = np.interp(tlist,params['decisionTimes'],decisions[:nTimes])
        params['savings'] = np.interp(tlist,params['decisionTimes'],decisions[nTimes:2*nTimes])
    else: # decisionType = 0 (specify abatement, compute savings rate)
        params['miu'] = np.interp(tlist,[0,5,35,300],[0,0,1,1]) # 30 year ramp
        params['savings'] = np.interp(tlist,params['decisionTimes'],decisions[:nTimes])
        
    if params['learningCurveOption'] >= 2:
        params['miuRatio'] = np.interp(tlist,params['decisionTimes'],decisions[-nTimes:])
    
    info = timeEvolve(state0,params)  # uses globals initState and initParams
    
    #print (1.e-9*float(np.sum(info['cemutotper'])))
    
    
    return float(np.sum(info['cemutotper'])),info
"""
    params['decisions'] = decisions
    if params['decisionType'] == 1:
        params['miu'] = lambda t,params : interpStep(t,params['decisionTimes'],decisions)
    else:
        nTimes = len(initParams['decisionTimes'])
        params['miu'] = lambda t,params : interpStep(t,params['decisionTimes'],decisions[:nTimes])
        params['savings'] = lambda t,params : interpStep(t,params['decisionTimes'],decisions[nTimes:])
"""

#%%

def timeEvolve(state0,params):
    # relies on globals <initState> and <initParams>
    
    timeEnd = params['timeEnd']
    dt = params['dt']
    
    state = state0
    info = {}
    info['cemutotper']=[] 
    tdic = {}
    timeIndex = 0
    
    for t in np.arange(0.0,timeEnd+dt,dt):
        params['t']=t
        params['timeIndex'] = timeIndex
        tdic['t']=t
         
        dstate, infoSub = dstatedt(state,params)  # params is a global used by dstatedt
        
        dictAppendEach(info,infoSub)
        
        if params['saveOutput']:
            dictAppendEach(info,state)
            dictAppendEachPrefix(info,dstate,'d')
            dictAppendEach(info,tdic)  # adds time to info sheet

        dictAddEachMultiply(state, dstate, dt)
        timeIndex += 1
    return info
    

#%%

"""
def econ_fun( region, t, act, k, cumabate, tatm, 
             alloc, alloc_other, ygross_other, act_other, 
             cumabate_actor_A, learning_curve_on, params ):
"""   

def dstatedt(state,params):
    
    dstate = {}
    info = {}
    epsilon = 1.e-20 # small number (almost zero)
    
    t = params['t']
    timeIndex = params['timeIndex']
    
    #--------------------------------------------------------------------------

    # Adjusted cost for backstop technology 
    if params['learningCurveOption'] == 0:
        # Vanilla DICE
        pbacktime = params['pbacktime'][timeIndex]
    elif params['learningCurveOption'] == 1:
        # Single learning curve
        cumAbate = state['cumAbate']
        pbacktime =  params['learningCurveConstant'] * cumAbate ** -params['learningCurveExponent']
    elif params['learningCurveOption'] >= 2:
        # Two learning curves 
        cumAbate0 = state['cumAbate0']
        cumAbate1 = state['cumAbate1']
        pbacktime0 =  params['learningCurveConstant'][0] * cumAbate0 ** -params['learningCurveExponent'][0]
        pbacktime1 =  params['learningCurveConstant'][1] * cumAbate1 ** -params['learningCurveExponent'][1]
        pbacktime =  params['miuRatio'][timeIndex] * pbacktime0 + (1.-params['miuRatio'][timeIndex] ) * pbacktime1
    else:
        print ('error in learningCurveOption = ', params['learningCFUrveOption'])

        
    #cost = pbacktime/1000 * sigma[t]/params['expcost2'] 
    cost = pbacktime * params['sigma'][timeIndex]/params['expcost2']  # Cost of backstop; note 1000 constant is lost due to units change
    
    # Gross domestic product GROSS of damage and abatement costs at t ($ 2005 per year)
    ygross = (params['al'][timeIndex]  * params['L'][timeIndex] **(1 - params['gama'])) * (max(state['k'],epsilon)**params['gama'])


    # Industrial CO2 emission at t (tCO2)
    eind = params['sigma'][timeIndex]  * ygross * (1 - params['miu'][timeIndex] ) # industrial emissions
    
    # Forest-related CO2 emissions
    # Total CO2 emission at t (tCO2)
    etot = eind + params['etree'][timeIndex] 

    # Emissions abated locally (tCO2)
    abateamount = params['sigma'][timeIndex]  * ygross * params['miu'][timeIndex] 

    # Abatement cost at t [This is now the total cost of abatement in each region, including resources from both regions]
    # All of the following variables are in <miu> units = fraction of emissions abated
    # <act> is this actor's action for its own abatement
    # <act_other> is the other actor's action for its own abatement
    # <alloc> is this actor's action for the abatement of other actor's emissions
    # <alloc_other> is the other actor's action for the abatement of this actor's emissions
    if params['learningCurveOption'] != 3:
       abatefrac = cost * params['miu'][timeIndex] **params['expcost2']
    
        # Marginal cost of abatement at t ($ 2005 per tCO2). Replace pbacktime with endogenous learning curve.
       mcabate = params['pbacktime'][timeIndex]  * params['miu'][timeIndex] **(params['expcost2'] - 1.0) 
    else: # learningCurveOption == 3
        cost0 = cost * pbacktime0 / pbacktime 
        cost1 = cost * pbacktime1 / pbacktime 
        if params['miuRatio'][timeIndex] == 0.0:
            abatefrac = cost1 * params['miu'][timeIndex] **params['expcost2'] 
            mcabate = pbacktime1* params['miu'][timeIndex] **(params['expcost2'] - 1.0) 
        elif params['miuRatio'][timeIndex] == 1.0:
            abatefrac = cost0 * params['miu'][timeIndex]**params['expcost2'] 
            mcabate = pbacktime0 * params['miu'][timeIndex] **(params['expcost2'] - 1.0)
        else:
            abatefrac = cost0 * (params['miu'][timeIndex]*       params['miuRatio'][timeIndex]  )**params['expcost2'] + \
                        cost1 * (params['miu'][timeIndex]*(1.0 - params['miuRatio'][timeIndex]) )**params['expcost2']
                        
            mcabate = max(pbacktime0 * ( params['miu'][timeIndex] *       params['miuRatio'][timeIndex] )**(params['expcost2'] - 1.0) ,
                          pbacktime1 * ( params['miu'][timeIndex] *(1.0 - params['miuRatio'][timeIndex]))**(params['expcost2'] - 1.0))
       
    abatecost = ygross * abatefrac    # <abatecost> is total of abatement this time step 
    
    # Climate damage cost at t
    damfrac = params['a1'] * state['tatm'] + params['a2'] * state['tatm']**params['a3']
    damages = ygross * damfrac


    # Gross domestic product NET of damage and abatement costs at t ($ 2005 per year)
    y = ygross - damages - abatecost
 
    # Investment at time t
    if params['decisionType'] == 1:
        rsav = params['optlrsav']
    else:
        rsav = params['savings'][timeIndex] 
    inv = rsav * y

    # Consumption ($ 2005)
    c = y - inv
    
    # Consumption per capita ($ per person per year)
    cpc = c / params['L'][timeIndex] 
  
    # Utility per capita (one period utility function)
    periodu = (max(0.001* cpc,epsilon)**(1 - params['elasmu']) - 1)/(1 - params['elasmu']) - 1
    # This ugly scaling by 0.001 is intended to keep utility numbers the same as what Nordhaus had
    
    # Period utility
    cemutotper = periodu *params['L'][timeIndex]  * params['rr'][timeIndex] 

    # Time rate of change of capital
    dstate['k'] = inv - params['dk']* state['k'] 
   
    
    #--------------------------------------------------------------------------
    # Next climate

    force = params['fco22x'] * np.log2(state['mat']/params['mateq']) + params['forcoth'][timeIndex]
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
    dstate['mat'] = etot + params['b12'] * (state['mu']*params['mateq']/params['mueq'] - state['mat'] )
    
    # Shallow ocean C carbon content ofcrease at t+1 (tC from 1750)
    dstate['mu'] = params['b12'] * ( state['mat'] - state['mu']*params['mateq']/params['mueq']) + \
                   params['b23']*  ( state['ml']*params['mueq']/params['mleq'] - state['mu'])
    
    # Deep ocean C carbon content crease at t+1 (tC from 1750)
    dstate['ml'] = params['b23']*( state['mu'] - state['ml']*params['mueq']/params['mleq'])

    #-------------------------------------------------------------------------
    if params['learningCurveOption'] == 1:
        dstate['cumAbate'] = abateamount
    elif params['learningCurveOption'] >= 2:
        abateamount0 = params['miuRatio'][timeIndex] *  abateamount 
        abateamount1 = (1.-params['miuRatio'][timeIndex] ) *  abateamount 
        dstate['cumAbate0'] = abateamount0
        dstate['cumAbate1'] = abateamount1
        
    #-------------------------------------------------------------------------
    info['cemutotper']=cemutotper

    if params['saveOutput']:
        info['ygross']=ygross
        info['etot']=etot
        info['eind']=eind
        info['abateamount']=abateamount 
        info['pbacktime'] = pbacktime 
        if params['learningCurveOption'] >= 2:
            info['abateamount0'] = abateamount0
            info['abateamount1'] = abateamount1
            info['pbacktime0'] = pbacktime0
            info['pbacktime1'] = pbacktime1
            info['miuRatio'] = params['miuRatio'][timeIndex]
        info['abatecost']=abatecost
        info['damfrac']=damfrac
        info['damages']=damages
        info['y']=y
        info['mcabate']=mcabate
        info['c']=c
        info['rsav']=rsav
        info['inv']=inv
        info['cpc']=cpc
        info['periodu']=periodu
        info['cemutotper']=cemutotper
        info['force'] = force
        info['outgoingLW'] = outgoingLW
        
        info['pbacktime'] = pbacktime 
        info['sigma'] = params['sigma'][timeIndex] 
        info['al'] = params['al'][timeIndex] 
        info['L'] = params['L'][timeIndex] 
        info['miu'] = params['miu'][timeIndex] 
        info['etree'] = params['etree'][timeIndex] 
        info['forcoth'] = params['forcoth'][timeIndex] 
        info['rr'] = params['rr'][timeIndex] 

    return dstate, info


#%%

def dictAppendEach(x, x0):
    for key in x0:
        if key in x:
            x[key].append(x0[key])
        else:
            x[key]=[x0[key]]
     
def dictAppendEachPrefix(x, x0,prefix):
    for key in x0:
        if prefix + key in x:
            x[prefix + key].append(x0[key])
        else:
            x[prefix + key]=[x0[key]]
     

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
     

  

#%%
            
# NOTE: It is important to the optimization that current decisions do not affect the
#       amount of capital stock in in the current period.

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
# Note: linear interpolation is accomplished with: np.interp(t,timePoints,dataPoints)


#%%

## SAMPLE RUN SCRIPTS

#st0,pa = defineParameters(3,1,[0.,1.])
#evaluateDecisions([0.1,0.05],st0,pa)
    
#decisionTimes03 = [0,150,300]
#decisionTimes05 = [0,31,150,269,300]
#decisionTimes10 = [0,3,23,63,119,181,237,277,297,300]
#decisionTimes15 = [0,1,7,21,43,74,110,150,190,226,257,279,293,299,300]

"""
EXAMPLE:
    
decisionTimes03 = [0.,100.,200.]
    
st0,pa = defineParameters(315,1.,decisionTimes03)

ut,inf = evaluateDecisions([0.1,0.1,0.1],st0,pa)

utils.csvWriteVector('test10.csv',inf)

utils.csvWriteScalar('test10s.csv',pa)

"""



#%%



"""
########################################################################
########### Main optimization code #####################################
########################################################################
"""
########################################################################
#########################   MAIN PROGRAM   #############################
########################################################################
  
def optDICEeq(maxeval,initState,initParams):
    #relies on globals <initState>, <params>
    #global initState,initParams
    
    decisionTimes = initParams['decisionTimes']
    nDecisionTimes = len(initParams['decisionTimes'])
    decisionType =  initParams['decisionType']
    learningCurveOption = initParams['learningCurveOption'] 
    
    nDecisions = nDecisionTimes
    if decisionType == 2: # optimize for both abatement and savings rate
        nDecisions +=   nDecisionTimes # add decisions for savings rate
    if learningCurveOption == 2:
        nDecisions += nDecisionTimes # add decisions for miuRatio

    problem = {} # Initialize dictionary containing problem specifications
    option  = {} # Initialize dictionary containing MIDACO options
    
    problem['@'] = wrapper # Handle for problem function name
    
    ########################################################################
    ### Step 1: Problem definition     #####################################
    ########################################################################
    
    # STEP 1.A: Problem dimensions
    ##############################
    problem['o']  = 1                       # Number of objectives 
    problem['n']  = int(nDecisions) # Number of variables (in total)
    problem['ni'] = 0                       # Number of integer variables (0 <= ni <= n) 
    problem['m']  = 0                       # Number of constraints (in total) 
    problem['me'] = 0                       # Number of equality constraints (0 <= me <= m)
    
    
    # STEP 1.B: Lower and upper bounds 'xl' & 'xu'
    #############################################
    #    # STEP 1.C: Starting point 'x'
    ##############################
    
    # miu == abatement fraction
    act0 = [1.0 for i in decisionTimes] # start assuming you will not mitigate at all
    #act0 = [0.570765 for i in range(nDecisions)] # miu in DICE-2016
    actupper = [initParams['limmiu'] for i in decisionTimes] # range(30)]

    if decisionType == 2:
        # savings rate
        act0 +=  [initParams['optlrsav'] for i in decisionTimes]
        actupper += [1.0 for i in decisionTimes] # range(30)]
        # initialize abatement to 1 and savings rate to "optimal"
        
    if learningCurveOption >= 2:
        act0 +=  [0.5 for i in decisionTimes] # split evenly between two technologies
        actupper += [1.0 for i in decisionTimes] # range(30)]
    
    problem['x'] = act0  # initial guess for control variable
    nDecisions = len(act0)
    

    actlower = [0.0 for i in act0]

    #actupper[30:] = [initParams['limmiu']] * (nDecisions-30)
    
    problem['xl'] = actlower
    problem['xu'] = actupper
    
    # STEP 1.A: Problem dimensions
    ##############################
    problem['o']  = 1                       # Number of objectives 
    problem['n']  = int(nDecisions) # Number of variables (in total)
    problem['ni'] = 0                       # Number of integer variables (0 <= ni <= n) 
    problem['m']  = 0                       # Number of constraints (in total) 
    problem['me'] = 0                       # Number of equality constraints (0 <= me <= m)
        
    ########################################################################
    ### Step 2: Choose stopping criteria and printing options    ###########
    ########################################################################
    
    # STEP 2.A: Stopping criteria 
    #############################
    #option['maxeval'] = 100000   # Maximum number of function evaluation (e.g. 1000000) 
    option['maxeval'] = maxeval   # Maximum number of function evaluation (e.g. 1000000) 
    #option['maxeval'] = 1    # Maximum number of function evaluation TEST
    option['maxtime'] = 60*60*24 # Maximum time limit in seconds (e.g. 1 Day = 60*60*24) 
    
    # STEP 2.B: Printing options  
    ############################ 
    option['printeval'] = 10   # Print-Frequency for current best solution (e.g. 1000) 
    option['save2file'] = 1     # Save SCREEN and SOLUTION to TXT-files [0=NO/1=YES]
    
    ########################################################################
    ### Step 3: Choose MIDACO parameters (FOR ADVANCED USERS)    ###########
    ########################################################################
    
    option['param1']  = 1.0e-6  # ACCURACY  
    option['param2']  = 1       # SEED (integer)
    option['param3']  = 0       # FSTOP (integer)
    option['param4']  = 100     # ALGOSTOP (integer) 
    option['param5']  = 0.0     # EVALSTOP  
    option['param6']  = 0.0     # FOCUS  
    option['param7']  = 100     # ANTS  
    option['param8']  = 10      # KERNEL  
    option['param9']  = 0.0     # ORACLE  
    option['param10'] = 0.0     # PARETOMAX
    option['param11'] = 0.0     # EPSILON  
    option['param12'] = 0.0     # BALANCE
    option['param13'] = 0.0     # CHARACTER
    
    ########################################################################
    ### Step 4: Choose Parallelization Factor   ############################
    ########################################################################
    
    option['parallel'] = 1 # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
    
    ########################################################################
    ############################ Run MIDACO ################################
    ########################################################################
   
    startdate = datetime.datetime.now()
    
    initParams["saveOutput"] = False
    
    if os.getlogin()=='kcaldeira':
        MIDACO_KEY = b'Ken_Caldeira_(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
    else:
        MIDACO_KEY = b'Candise_Henry(Carnegie_InSc_Stanford)_[ACADEMIC-SINGLE-USER]'
        
    solution = midaco.run( problem, option, MIDACO_KEY )
    print(solution['x'])
    
    enddate = datetime.datetime.now()
    minutes_diff = (enddate - startdate).total_seconds() / 60.0
    print ('elapsed time = ',str(minutes_diff),' minutes')
    
    todayString = str(enddate.year) + str(enddate.month).zfill(2) + str(enddate.day).zfill(2) + '_' + \
        str(enddate.hour).zfill(2) + str(enddate.minute).zfill(2) + str(enddate.second).zfill(2)

    initParams["saveOutput"] = True
    
    utility,info = DICE_fun(solution['x'],initState,initParams)
    print(utility*1.e-9)
    root_dir = "."

    return [problem,option,solution,initParams,info]
############################ END OF FILE ###############################
    #pickle_results(root_dir,'DICEeq_'+todayString,[problem,option,solution,initParams,info])
    

########################################################################
########################################################################
    
#iState,iParams = createGlobalVariables(300,1,[0,2.5,5,10,20,40,80,120,160,200,240,280,290,295,297.5]); res = optDICEeq(iState, iParams)
#from plot_utilities import *
