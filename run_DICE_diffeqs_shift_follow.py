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


        caseName = 'shift_10000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 10000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_09000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 09000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_08000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 08000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_07000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 07000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_06000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 06000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_05000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 05000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_04000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 04000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_03000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 03000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'shift_02000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 02000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'shift_01000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 01000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'shift_1e20'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 1.e20,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'shift_00000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 00000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        #==========================================================================================

        caseName = 'follow_10000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 10000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_09000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 09000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 17705.553712619043,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_08000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 08000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 33532.99553928247,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_07000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 07000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 69170.4183444645,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_06000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 06000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 159560.00340327647,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_05000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 05000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 428811.28829378466,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_04000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 04000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1.4379327017549453e6,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_03000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 03000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 6.842113061951967e6,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


        caseName = 'follow_02000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 02000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 6.166017743193007e7,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'follow_01000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 01000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 2.644058012100929e9,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'follow_1e20'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 1.e20,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1.7525254227648863e-83,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        caseName = 'follow_0000'

        # If no arg is given, run vanilla DICE

        resultDICE = DICE_instance(dt = 1,

                # dt time step for integration

                decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                decisionType = 2,

                # decisionType == 1, use prescribed savings rate

                #               == 2, optimize on savings rate in addition to other parameters

                #               == 3, estimate savings rate only, miu hard coded for no abatement.

                learningCurveOption = 3,

                # learningCurveOption == 0, single technology, vanilla DICE

                #                     == 1, single technology, with learning curve

                #                     == 2, dual technology, dual learning curves

                #                     == 3, dual technology, only second has learning curve 

                #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 


                #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                learningCurveInitCost = 00000.,

                # learningCurveInitCost == initial cost for learning curve.
                
                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                learningCurveInitAmount  = 1e4,

                # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                # learningCurveExponent = 0.15200309344504995, # 10% per doubling
                learningCurveExponent = 0.18442457113742744, # 12% per doubling
                # learningCurveExponent = 0.23446525363702297,  # 15% per doubling

                # learningCurveExponent == slope of learning curve on log-log plot,

                #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                # (scalar unless learningCurveOption = 2, in which case 2 element list)

                utilityOption = 1,

                # utilityOption == 0 --> DICE utility function

                #               == 1 --> assume consumption == utility

                prstp = 0.03,

                # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                
                firstUnitFractionalCost = [0.0, 0.1], 

                # firstUnitFractionCost == cost of first unit

                parallel = 15,

                # number of cores to use, 0 or 1 is single core,

                # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                maxeval = 100000

                # maxeval maximum number of iterations for solver

        )

        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resultDICE.out))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


