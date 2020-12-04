# -*- coding: utf-8 -*-

"""

Created on Sun Jul 12 14:53:40 2020

@author: kcaldeira

"""

from plot_utilities import *

from io_utilities import *

import cProfile

from DICE_diffeqs import DICE_instance


#%%

# starting point has learning curve of 10 k$ at 10,000 tCO2, and a learning rate of 12% per doubling.

if __name__ == "__main__":

        abatementCostList = [1]
        damageCostList = [1]
        #rampOpts = ['0by2050','welfare','max','min']
        rampOpts = ['welfare']

        maxEval = 100000

        #initCostList = [1.e4,9.e3,8.e3,7.e3,6.e3,5.e3,4.e3,3.e3,2.e3,1.5e3,1.e3,900,800,700,600,500,400,300,200,100,50,0,1.e20]
        #initCostList = [1e4,1e3,1e2]
        #initCostList = [1.e20,1.e4,1.e3,100,0]
        #initCostList = [1.e20,1.e3,900,800,700,600,500,400,300,200,100,50,0]

        
        for damageCostOpt in damageCostList:
            for abatementCostOpt in abatementCostList:


                for rampOpt in rampOpts:
                    if rampOpt == '0by2050':
                        limLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,   
                                    1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
                        limUpper = limLower
                    elif rampOpt == 'max':
                        limLower = 1.0
                        limUpper = limLower
                    elif rampOpt == 'min':
                        limLower = 0.0
                        limUpper = limLower
                    else:
                        limLower = 0.0
                        limUpper = 1.0

                    caseName = 'DICElike1.0_'+str(abatementCostOpt)+'_'+str(damageCostOpt)+'_'+rampOpt+'_'+str(maxEval)

                    # If no arg is given, run vanilla DICE

                    print (caseName)
                    resultCentral = DICE_instance(
                        
                        dt = 1, # dt time step for integration

                        nTechs = 1, # number of technologies considered

                        decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,250,275,290,300], # times for miu decisions
                        # NOTE: <decisionTimes> are also the times assumed for specified limits on miu

                        #limMiuLower = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # lower limit on miu values (= sum across all techs)
                        limMiuLower = limLower,
                        #limMiuLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,
                        #                        1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],
                        #limMiuLower = 0, # can be scalar or vector of len(decisionTimes)
                        limMiuUpper = limUpper, # upper limit on miu values (= sum across all techs)
                        #limMiuUpper = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2], # upper limit on miu values (= sum across all techs)
                        #limMiuUpper = 1.0, # can be scalar or vector of len(decisionTimes)

                        optSavings = True, # True means to optimize on savings rate, False means to use default DICE value

                        savingDecisionTimes =[0,20,40,60,80,100,150,200,250,275,300], # times for savings rate decisions

                        techLearningCurve = [False], # does this technology have a learning curve (True) or a specified cost function (False)
                        # NOTE: <learningCurveTech> must have a length of <nTechs>

                        techInitCost = [550], # Initial cost for learning curve. Must be same shape as nTechs.
                        #techInitCost = [550, 1e4], # Initial cost for learning curve. Must be same shape as nTechs.
                                                            # If no learning curve, then this value is the initial backstop cost (pback)

                        techInitAmount = [0], # Initial cost for learning curve. Must be same shape as nTechs, but value if no learning curve is unimportant 

                        techLearningRate = [0.005050763379468082], # 15% per doubling. Must be same shape as nTechs.
                        #techLearningRate = [0.005050763379468082, 0.23446525363702297], # 15% per doubling. Must be same shape as nTechs.
                        # techLearningRate = [0.005050763379468082, 0.18442457113742744], # 12% per doubling. Must be same shape as nTechs.
                                                            # If no learning curve, then value is fractional cost improvement per year

                        firstUnitFractionalCost = [0.0], # Marginal cost at miuX = 0 compared to marginal cost at miuX = 1.

                        utilityOption = 0, # utilityOption == 0 --> DICE utility function; 1 --> assume consumption == utility

                        prstp = 0.03, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                            
                        parallel = 15, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                        #parallel = 1, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                        
                        maxeval = maxEval,  # maxeval maximum number of iterations for solver
                        #maxeval =  100,  # maxeval maximum number of iterations for solver

                        FOCUS  = 100, # FOCUS parameter for midaco solver

                        damageCostRatio = 1.0, # scaling on climate damage

                        abatementCostRatio = abatementCostOpt # scaling on abatement costs (multiplies costs above for all techs)

                    )


                        
                    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultCentral.out))

                    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

                    limUpper = 1.2
                    caseName = 'DICElike1.2_'+str(abatementCostOpt)+'_'+str(damageCostOpt)+'_'+rampOpt+'_'+str(maxEval)

                    # If no arg is given, run vanilla DICE

                    print (caseName)
                    resultCentral = DICE_instance(
                        
                        dt = 1, # dt time step for integration

                        nTechs = 1, # number of technologies considered

                        decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,250,275,290,300], # times for miu decisions
                        # NOTE: <decisionTimes> are also the times assumed for specified limits on miu

                        #limMiuLower = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # lower limit on miu values (= sum across all techs)
                        limMiuLower = limLower,
                        #limMiuLower = [0.,0.,0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.,
                        #                        1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.],
                        #limMiuLower = 0, # can be scalar or vector of len(decisionTimes)
                        limMiuUpper = limUpper, # upper limit on miu values (= sum across all techs)
                        #limMiuUpper = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2], # upper limit on miu values (= sum across all techs)
                        #limMiuUpper = 1.0, # can be scalar or vector of len(decisionTimes)

                        optSavings = True, # True means to optimize on savings rate, False means to use default DICE value

                        savingDecisionTimes =[0,20,40,60,80,100,150,200,250,275,300], # times for savings rate decisions

                        techLearningCurve = [False], # does this technology have a learning curve (True) or a specified cost function (False)
                        # NOTE: <learningCurveTech> must have a length of <nTechs>

                        techInitCost = [550], # Initial cost for learning curve. Must be same shape as nTechs.
                        #techInitCost = [550, 1e4], # Initial cost for learning curve. Must be same shape as nTechs.
                                                            # If no learning curve, then this value is the initial backstop cost (pback)

                        techInitAmount = [0], # Initial cost for learning curve. Must be same shape as nTechs, but value if no learning curve is unimportant 

                        techLearningRate = [0.005050763379468082], # 15% per doubling. Must be same shape as nTechs.
                        #techLearningRate = [0.005050763379468082, 0.23446525363702297], # 15% per doubling. Must be same shape as nTechs.
                        # techLearningRate = [0.005050763379468082, 0.18442457113742744], # 12% per doubling. Must be same shape as nTechs.
                                                            # If no learning curve, then value is fractional cost improvement per year

                        firstUnitFractionalCost = [0.0], # Marginal cost at miuX = 0 compared to marginal cost at miuX = 1.

                        utilityOption = 0, # utilityOption == 0 --> DICE utility function; 1 --> assume consumption == utility

                        prstp = 0.03, # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                            
                        parallel = 15, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                        #parallel = 1, # number of cores to use, 0 or 1 is single core; Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...
                        
                        maxeval = maxEval,  # maxeval maximum number of iterations for solver
                        #maxeval =  100,  # maxeval maximum number of iterations for solver

                        FOCUS  = 100, # FOCUS parameter for midaco solver

                        damageCostRatio = 1.0, # scaling on climate damage

                        abatementCostRatio = abatementCostOpt # scaling on abatement costs (multiplies costs above for all techs)

                    )


                        
                    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultCentral.out))

                    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)




