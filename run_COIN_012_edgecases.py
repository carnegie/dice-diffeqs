# -*- coding: utf-8 -*-

"""

Created on Sun Jul 12 14:53:40 2020

@author: kcaldeira

"""

from plot_utilities import *

from io_utilities import *

import numpy as np

import cProfile

from DICE_diffeqs import DICE_instance

#==============================================================================
#  For COIN011, this code performs the following cases:
#
#  -- no-abate (no abatement)
#  -- free-abate (no climate change in budgeting and balancing cases)
#
#==============================================================================

#%%
if __name__ == "__main__":

    #==============================================================================
    # no-abate 
    #==============================================================================

    for seedVal in [101,102,103]:
        shiftOpts = ['shift']
        maxEval = 200000

        initCostList = [10]
        #initCostList = np.insert(np.round(10.**-np.arange(0,2.05,0.25),6),0,10)
        #initCostList = np.insert(np.round(10.**-np.arange(0.05,2.05,0.1),6),0,10)
        #initCostList = np.round(10.**-np.arange(1.6,2.05,0.05),6)
        #initCostList = [1.]

        initCostRef = 1.0                                                      
        rampOpts = ['ramping']

        rateOptDic = {"10pct":0.13750352374993496}

        initAmounts = [1e-6]

        prefix = "COIN_012a_no-abate_" #  model_version_suite_
        
        dt0 = 1.
        sdt =  [0,dt0,-30,-1,-60,-2,-90,-3,-120,-6,-150,-4,-200,-5,-280,-7,300]

        for rampOpt in rampOpts:
            cBudget = -999 # flag for unlimited

            if rampOpt == 'ramping':

                # assumes years 0, 1, 5, 10, 15, 20 ,25, 39
                limLower = [0.,0.03333333333333333333,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,   
                            1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
                limLower = len(limLower)*[0.0] # set to zero-s for this case
                limUpper = limLower
                rampOpt = 'no-abate' # reset rampOpt
            elif rampOpt == 'max':
                limLower = 1.0
                limUpper = limLower
            elif rampOpt == 'budgeting':
                limLower = 0.0
                limUpper = 1.0
                cBudget = 50.
            elif rampOpt == 'balancing':
                limLower = 0.0
                limUpper = 1.0

            for initCost in initCostList:
                for shiftOpt in shiftOpts:

                    for initAmt in initAmounts:
                        for rateOpt in rateOptDic.keys():

                            if shiftOpt == 'shift':
                                initAmount = initAmt
                            else:
                                if initCost > 0:
                                    initAmount = initAmt*(initCost/initCostRef)**(-1./rateOptDic[rateOpt])
                                else:
                                    initAmount = 1.e80

                            caseName = (prefix + rampOpt + '_i' + str(initCost)
                                        + '_s' + str(seedVal)
                                        + '_m' + str(maxEval)
                                        )


                            # If no arg is given, run vanilla DICE

                            print()
                            print("=============================================================")
                            print (caseName)
                            resultCentral = DICE_instance(

                                COINmode = True, # simple version
                                
                                dt = dt0, # dt time step for integration

                                nTechs = 2, # number of technologies considered

                                decisionTimes =[0,dt0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,170,200,240,260,280,300], # times for miu decisions
                                # NOTE: <decisionTimes> are also the times assumed for specified limits on miu

                                freeAbateAmount = 0., # Number of years worth of free abatement
                                carbonBudget = cBudget, # number of years worth of unabated carbon

                                #limMiuLower = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # lower limit on miu values (= sum across all techs)
                                limMiuLower = limLower,
                                #limMiuLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,
                                #                        1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],
                                #limMiuLower = 0, # can be scalar or vector of len(decisionTimes)
                                limMiuUpper = limUpper, # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2], # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = 1.0, # can be scalar or vector of len(decisionTimes)

                                optSavings = True, # True means to optimize on savings rate, False means to use default value (different for COINmode)

                                #savingDecisionTimes =[0,20,40,60,80,100,140,200,260,280,300], # times for savings rate decisions
                                #savingDecisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,170,200,240,260,280,300], # times for miu decisions
                                #savingDecisionTimes =[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,200,240,260,280,300], # times for miu decisions
                                #savingDecisionTimes =[0,dt0,10,20,30,45,60,90,120,150,200,240,260,280,290,300], # times for miu decisions
                                #savingDecisionTimes =[0,30,60,90,120,150,200,260,280,300], # times for miu decisions

                                savingDecisionTimes = sdt, # times for miu decisions
                                decisionInterpSwitch = 3, # 0 = step function, 1 = linear, 2 = spline savings only

                                techLearningCurve = [False,True], # does this technology have a learning curve (True) or a specified cost function (False)
                                # NOTE: <learningCurveTech> must have a length of <nTechs>

                                techInitCost = [0.2,initCost], # Initial cost for learning curve. Must be same shape as nTechs.
                                #techInitCost = [550, 1e4], # Initial cost for learning curve. Must be same shape as nTechs.
                                                                    # If no learning curve, then this value is the initial backstop cost (pback)

                                techInitAmount = [0,initAmount], # Initial cost for learning curve. Must be same shape as nTechs, but value if no learning curve is unimportant 

                                techLearningRate = [0.005,rateOptDic[rateOpt]], # 10% per doubling (1 + 0.10)**-1. Must be same shape as nTechs.
                                #techLearningRate = [0.005050763379468082, 0.23446525363702297], # 15% per doubling. Must be same shape as nTechs.
                                # techLearningRate = [0.005050763379468082, 0.18442457113742744], # 12% per doubling. Must be same shape as nTechs.
                                                                    # If no learning curve, then value is fractional cost improvement per year

                                firstUnitFractionalCost = [0.0,0.5], # Marginal cost at miuX = 0 compared to marginal cost at miuX = 1.

                                utilityOption = 1, # utilityOption == 0 --> DICE utility function; 1 --> assume consumption == utility

                                prstp = 0.03, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                                    
                                parallel = 15, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                                #parallel = 1, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                                
                                maxeval = maxEval,  # maxeval maximum number of iterations for solver
                                #maxeval =  100,  # maxeval maximum number of iterations for solver

                                SEED = seedVal,
                                
                                FOCUS  = 100, # FOCUS parameter for midaco solver
                                ANTS = 81,
                                KERNEL = 27,

                                damageCostRatio = 1.0, # scaling on climate damage

                                abatementCostRatio = 1.0 # scaling on abatement costs (multiplies costs above for all techs)

                            )


                                
                            pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultCentral.out))

                            write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        #==============================================================================
        # no-cost
        #==============================================================================


        shiftOpts = ['shift']

        maxEval = 200000
        initCostList = [10]

        #initCostList = np.insert(np.round(10.**-np.arange(0.05,2.05,0.1),6),0,10)
        #initCostList = np.round(10.**-np.arange(1.6,2.05,0.05),6)
        #initCostList = [1.]

        initCostRef = 1.0                                                      
        rampOpts = ['budgeting','balancing','ramping']

        rateOptDic = {"10pct":0.13750352374993496}

        initAmounts = [1e-6]

        prefix = "COIN_012a_no-cost_" #  model_version_suite_
        
        dt0 = 1.
        
        sdt =  [0,dt0,-30,-1,-60,-2,-90,-3,-120,-6,-150,-4,-200,-5,-280,-7,300]

        for rampOpt in rampOpts:
            cBudget = -999 # flag for unlimited

            if rampOpt == 'ramping':

                # assumes years 0, 1, 5, 10, 15, 20 ,25, 39
                limLower = [0.,0.03333333333333333333,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,   
                            1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
                limUpper = limLower
            elif rampOpt == 'max':
                limLower = 1.0
                limUpper = limLower
            elif rampOpt == 'budgeting':
                limLower = 0.0
                limUpper = 1.0
                cBudget = 50.
            elif rampOpt == 'balancing':
                limLower = 0.0
                limUpper = 1.0

            for initCost in initCostList:
                for shiftOpt in shiftOpts:

                    for initAmt in initAmounts:
                        for rateOpt in rateOptDic.keys():

                            if shiftOpt == 'shift':
                                initAmount = initAmt
                            else:
                                if initCost > 0:
                                    initAmount = initAmt*(initCost/initCostRef)**(-1./rateOptDic[rateOpt])
                                else:
                                    initAmount = 1.e80

                            caseName = (prefix + rampOpt + '_i' + str(initCost)
                                        + '_s' + str(seedVal)
                                        + '_m' + str(maxEval)
                                        )


                            # If no arg is given, run vanilla DICE

                            print()
                            print("=============================================================")
                            print (caseName)
                            resultCentral = DICE_instance(

                                COINmode = True, # simple version
                                
                                dt = dt0, # dt time step for integration

                                nTechs = 2, # number of technologies considered

                                decisionTimes =[0,dt0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,170,200,240,260,280,300], # times for miu decisions
                                # NOTE: <decisionTimes> are also the times assumed for specified limits on miu

                                freeAbateAmount = 0., # Number of years worth of free abatement
                                carbonBudget = cBudget, # number of years worth of unabated carbon

                                #limMiuLower = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # lower limit on miu values (= sum across all techs)
                                limMiuLower = limLower,
                                #limMiuLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,
                                #                        1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],
                                #limMiuLower = 0, # can be scalar or vector of len(decisionTimes)
                                limMiuUpper = limUpper, # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2], # upper limit on miu values (= sum across all techs)
                                #limMiuUpper = 1.0, # can be scalar or vector of len(decisionTimes)

                                optSavings = True, # True means to optimize on savings rate, False means to use default value (different for COINmode)

                                #savingDecisionTimes =[0,20,40,60,80,100,140,200,260,280,300], # times for savings rate decisions
                                #savingDecisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,170,200,240,260,280,300], # times for miu decisions
                                #savingDecisionTimes =[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,200,240,260,280,300], # times for miu decisions
                                #savingDecisionTimes =[0,dt0,10,20,30,45,60,90,120,150,200,240,260,280,290,300], # times for miu decisions
                                #savingDecisionTimes =[0,30,60,90,120,150,200,260,280,300], # times for miu decisions

                                savingDecisionTimes = sdt, # times for miu decisions
                                decisionInterpSwitch = 3, # 0 = step function, 1 = linear, 2 = spline savings only

                                techLearningCurve = [False,True], # does this technology have a learning curve (True) or a specified cost function (False)
                                # NOTE: <learningCurveTech> must have a length of <nTechs>

                                techInitCost = [0.0,initCost], # Initial cost for learning curve. Must be same shape as nTechs.
                                #techInitCost = [550, 1e4], # Initial cost for learning curve. Must be same shape as nTechs.
                                                                    # If no learning curve, then this value is the initial backstop cost (pback)

                                techInitAmount = [0,initAmount], # Initial cost for learning curve. Must be same shape as nTechs, but value if no learning curve is unimportant 

                                techLearningRate = [0.005,rateOptDic[rateOpt]], # 10% per doubling (1 + 0.10)**-1. Must be same shape as nTechs.
                                #techLearningRate = [0.005050763379468082, 0.23446525363702297], # 15% per doubling. Must be same shape as nTechs.
                                # techLearningRate = [0.005050763379468082, 0.18442457113742744], # 12% per doubling. Must be same shape as nTechs.
                                                                    # If no learning curve, then value is fractional cost improvement per year

                                firstUnitFractionalCost = [0.0,0.5], # Marginal cost at miuX = 0 compared to marginal cost at miuX = 1.

                                utilityOption = 1, # utilityOption == 0 --> DICE utility function; 1 --> assume consumption == utility

                                prstp = 0.03, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                                    
                                parallel = 15, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                                #parallel = 1, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                                
                                maxeval = maxEval,  # maxeval maximum number of iterations for solver
                                #maxeval =  100,  # maxeval maximum number of iterations for solver

                                SEED = seedVal,
                                FOCUS  = 100, # FOCUS parameter for midaco solver
                                ANTS = 81,
                                KERNEL = 27,

                                damageCostRatio = 1.0, # scaling on climate damage

                                abatementCostRatio = 1.0 # scaling on abatement costs (multiplies costs above for all techs)

                            )


                                
                            pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultCentral.out))

                            write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



    # %%
