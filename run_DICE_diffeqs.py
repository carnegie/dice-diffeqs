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

if __name__ == "__main__":

        caseName = 'test_case'

        # If no arg is given, run vanilla DICE

        result40 = DICE_instance(dt = 1,

                                 # dt time step for integration
        
                                 decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,130,150,200,280,290,300],

                                 decisionType = 1,

                                 # decisionType == 1, use prescribed savings rate

                                 #               == 2, optimize on savings rate in addition to other parameters

                                 #               == 3, estimate savings rate only, miu hard coded for no abatement.

                                 learningCurveOption = 1,

                                 # learningCurveOption == 0, single technology, vanilla DICE

                                 #                     == 1, single technology, with learning curve

                                 #                     == 2, dual technology, dual learning curves

                                 #                     == 3, dual technology, only second has learning curve 

                                 #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

                                 #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

                                 innovationRatio = 0,

                                 # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                 learningCurveInitCost = 5500.,

                                 # learningCurveInitCost == initial cost for learning curve.
                                 
                                 # (scalar unless learningCurveOption = 2, in which case 2 element list)

                                 learningCurveInitAmount  = 1e4,

                                 # learningCurveInitAmount == cumulative amount at time zero for learning curve.

                                 # (scalar unless learningCurveOption = 2, in which case 2 element list)

                                 earningCurveExponent = 0.15200309344504995,

                                 # learningCurveExponent == slope of learning curve on log-log plot,

                                 #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

                                 # (scalar unless learningCurveOption = 2, in which case 2 element list)

                                 utilityOption = 1,

                                 # utilityOption == 0 --> DICE utility function

                                 #               == 1 --> assume consumption == utility

                                 prstp = 0.03,

                                 # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )
                                 
                                 firstUnitFractionalCost = 0.1, 

                                 # firstUnitFractionCost == cost of first unit

                                 parallel = 15,

                                 # number of cores to use, 0 or 1 is single core,

                                 # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

                                 maxeval = 1000

                                 # maxeval maximum number of iterations for solver

                           )
        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(result40))

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





"""

# More regular kind of test case (takes about 3 min to run on my machine )



caseName = 'test_10k'



result = runDICEeq(



    # dt time step for integration

    dt = 1,

    

    # tlist list of decision times (last decision time is end time of integration)

    

    decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300],

    

    

    # decisionType == 1, use prescribed savings rate

    #              == 2, optimize on savings rate in addition to other parameters

    #              == 3, estimate savings rate only

    #                          miu hard coded for no abatement.

    

    #decisionType = 3,

    decisionType = 2,

    

    # learningCurveOption == 0, single technology, vanilla DICE

    #                     == 1, single technology, with learning curve

    #                     == 2, dual technology, dual learning curves

    #                     == 3, dual technology, only second has learning curve 

    #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

    #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

    

    learningCurveOption = 3,

    

    # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                        

    innovationRatio = 0,

    

    # learningCurveInitCost == initial cost for learning curve.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveInitCost = 5500. ,

    

    # learningCurveInitAmount == cumulative amount at time zero for learning curve.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveInitAmount  = 1e4, 

    

    # learningCurveExponent == slope of learning curve on log-log plot,

    #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveExponent = 0.15200309344504995, 

           

    # utilityOption == 0 --> DICE utility function

    #               == 1 --> assume consumption == utility

    

    utilityOption = 1,

    

    # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

    

    prstp = 0.03,

    

    # firstUnitFractionCost == cost of first unit

    

    firstUnitFractionalCost = [0.1, 0.1],

    

    # number of cores to use, 0 or 1 is single core,

    # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

    

    parallel = 1,

    

    # maxeval maximum number of iterations for solver

    

    maxeval = 10000

    )





pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(result))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

#"""













#%%



"""



#TEST EXAMPLE. THE NEXT LINE SHOULD RUN PROPERLY AND PRODUCE OUTPUT LIKE THE FOLLOWING



res2 = runDICEeq()





        10/09/2020 20:40:51

        [0.11782187651078362, 0.11847914215584855, 0.13538843014627477, 0.1546948554357284, 0.17522880655301645, 0.2006530657664092, 0.21299159464892045, 0.21969442781205817, 0.28028569815473725, 0.2504005642594187, 0.32603836643362694, 0.3330327910967299, 0.36916401639180496, 0.4172079475947874, 0.43691469409735884, 0.4662520216829885, 0.5369353318154555, 0.5401704157815219, 0.5671256891479827, 0.6238056046187326, 0.6977797502307891, 0.7236226547046273, 1.0568964770874654, 1.197045549757535, 1.19995093881849, 1.1929180591265525, 0.6267507576856426, 0.7668773743742695]

        10/09/2020 20:40:59

        elapsed time =  0.1350484  minutes

        0.48611825629538824









#%%



# Vanilla DICE-2016R simulation  THESE ARE THE DEFAULT PARAMETER VALUES



caseName = 'DICEtest_10k'



result = runDICEeq(



    # dt time step for integration

    dt = 1,

    

    # tlist list of decision times (last decision time is end time of integration)

    

    decisionTimes =[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300],

    

    

    # decisionType == 1, use prescribed savings rate

    #              == 2, optimize on savings rate in addition to other parameters

    #              == 3, estimate savings rate only

    #                          miu hard coded for no abatement.

    

    #decisionType = 3,

    decisionType = 1,

    

    # learningCurveOption == 0, single technology, vanilla DICE

    #                     == 1, single technology, with learning curve

    #                     == 2, dual technology, dual learning curves

    #                     == 3, dual technology, only second has learning curve 

    #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

    #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

    

    learningCurveOption = 0,

    

    # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                        

    innovationRatio = 0,

    

    # learningCurveInitCost == initial cost for learning curve.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveInitCost = 5500. ,

    

    # learningCurveInitAmount == cumulative amount at time zero for learning curve.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveInitAmount  = 1e4, 

    

    # learningCurveExponent == slope of learning curve on log-log plot,

    #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

    # (scalar unless learningCurveOption = 2, in which case 2 element list)

    

    learningCurveExponent = 0.15200309344504995, 

           

    # utilityOption == 0 --> DICE utility function

    #               == 1 --> assume consumption == utility

    

    utilityOption = 0,

    

    # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

    

    prstp = 0.015,

    

    # firstUnitFractionCost == cost of first unit

    

    firstUnitFractionalCost = 0,

    

    # number of cores to use, 0 or 1 is single core,

    # Serial: 0 or 1, Parallel: 2,3,4,5,6,7,8...

    

    parallel = 1,

    

    # maxeval maximum number of iterations for solver

    

    maxeval = 1000

    )





# OUTPUT OF TEST RUN with maxeval = 1000



        10/09/2020 18:02:23

        [0.11782187651078362, 0.11847914215584855, 0.13538843014627477, 0.1546948554357284, 0.17522880655301645, 0.2006530657664092, 0.21299159464892045, 0.21969442781205817, 0.28028569815473725, 0.2504005642594187, 0.32603836643362694, 0.3330327910967299, 0.36916401639180496, 0.4172079475947874, 0.43691469409735884, 0.4662520216829885, 0.5369353318154555, 0.5401704157815219, 0.5671256891479827, 0.6238056046187326, 0.6977797502307891, 0.7236226547046273, 1.0568964770874654, 1.197045549757535, 1.19995093881849, 1.1929180591265525, 0.6267507576856426, 0.7668773743742695]

        10/09/2020 18:02:31

        elapsed time =  0.14119486666666664  minutes

        0.48611825629538824



# TEST RUN WITH maxeval = 10,000 instead of 1000

        

res2 = runDICEeq(maxeval = 10000)



        10/09/2020 18:07:46

        [0.11588568882948175, 0.12799732039436923, 0.14210742312962285, 0.1579449759522625, 0.1754216406375176, 0.19445960647246685, 0.21502320477485518, 0.23709857721630762, 0.26068996341459005, 0.2858135775611535, 0.3124940867380768, 0.34076226587417796, 0.37065036513027555, 0.4021987805754812, 0.4354327509095898, 0.4704131313840456, 0.5071404715012597, 0.5456876127445954, 0.5861207986990827, 0.6283278547644422, 0.6731181395180476, 0.7643533839078004, 0.9822891203379444, 1.2, 1.2, 1.2, 0.6744423671565069, 0.0]

        10/09/2020 18:09:07

        elapsed time =  1.35658935  minutes

        0.48611903642090903  



# TEST RUN WITH maxeval = 20,000 instead of 1000



res2 = runDICEeq(maxeval = 20000)



        10/09/2020 18:04:01

        [0.11588530588955423, 0.12799644726180467, 0.14210664856788185, 0.157944564283299, 0.17542148580230665, 0.19445956460096497, 0.21502312494653752, 0.23709870548803644, 0.2606900092175558, 0.28581355263478253, 0.3124941063240477, 0.3407621848937199, 0.37065087083058135, 0.4021972994912176, 0.43543639583813915, 0.4704068205953609, 0.507146022358954, 0.5456872496780522, 0.586119168732383, 0.6283264006536459, 0.6731154076575664, 0.7643588141981891, 0.9822846456442204, 1.2, 1.2, 1.2, 0.6744422990347867, 0.0]

        10/09/2020 18:06:46

        elapsed time =  2.7607190666666668  minutes

        0.48611903642091703

        

      









#%%



NOTE THE STUFF BELOW HERE IS OLD ARE EXAMPLES OF SOME INTERESTING PARAMTER VALUES



maxIter = 20000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]



qlist = [1e100, 7.09787e10, 7.4252e8, 5.15509e7, 7.76762e6, 1.78951e6, 539282., 195608., 81258.3, 37440.8, 18720.4, 10000.]

alist = [6.30508e-16,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500]

aStringlist = ["0000","0500",    "1000",    "1500",   "2000",    "2500",    "3000",   "3500",  "4000", "4500",  "5000",  "5500"]



for qval,aval,aString in zip(qlist,alist,aStringlist):



    #caseName = 'test_1_0_0_0.015_10k'  # f for following

    caseName = 'initcost_2_3_' + aString + 'q_1_0.03_0.1_20k' 

    

    initState,initParams= createGlobalVariables(1,tlist,

            # dt, and decisionTimes (last time step is last decision time)

            

            # decisionType == 1, use prescribed savings rate

            #              == 2, optimize on savings rate in addition to other parameters

            #              == 3, estimate savings rate only

            #                          miu hard coded for no abatement.

            

            #decisionType = 3,

            decisionType = 2,

            

            # learningCurveOption == 0, single technology, vanilla DICE

            #                     == 1, single technology, with learning curve

            #                     == 2, dual technology, dual learning curves

            #                     == 3, dual technology, only second has learning curve 

            #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

            #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

            

            learningCurveOption = 3,

            

            # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                                

            innovationRatio = 0,

            

            # learningCurveInitCost == initial cost for learning curve.

            # (scalar unless learningCurveOption = 2, in which case 2 element list)

            

            learningCurveInitCost = aval ,

            

            # learningCurveInitAmount == cumulative amount at time zero for learning curve.

            # (scalar unless learningCurveOption = 2, in which case 2 element list)

            

            learningCurveInitAmount  = qval, 

            

            # learningCurveExponent == slope of learning curve on log-log plot,

            #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

            # (scalar unless learningCurveOption = 2, in which case 2 element list)

            

            learningCurveExponent = 0.15200309344504995, 

                   

            # utilityOption == 0 --> DICE utility function

            #               == 1 --> assume consumption == utility

            

            utilityOption = 1,

            

            # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

            

            prstp = 0.03,

            

            # firstUnitFractionCost == cost of first unit

            

            firstUnitFractionalCost = [0.1, 0.1]

            )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)







#%%







maxIter = 20000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]



#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_5500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 5500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_5000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 5000. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_4500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 4500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_4000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 4000. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_3500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 3500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_3000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 3000. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_2500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 2500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_2000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 2000. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_1500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 1500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_1000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 1000. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_0500_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'initcost_2_3_0000_1_0.03_0.1_20k' 



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 0. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1, 0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)









#%%





maxIter = 1000000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]









#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'test_2_0_1_0.03_0.1_1M'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 0,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 5500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = 0.1

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)







#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'test_2_3-5500-1e4_1_0.03_0.1-0.1_1M'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 5500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1,0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#%%



maxIter = 30000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]









#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'test_2_3-5500-1e4_1_0.03_0.1-0.1_30k'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        # dt, and decisionTimes (last time step is last decision time)

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 3,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 5500. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e4, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

               

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = [0.1,0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#%%



      

maxIter = 300



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]











#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'test_info_3p_0_0_0.015_300'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        decisionType = 3,

        #decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 0,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 550. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e10, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

        

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 0,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.015,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = 0 

        )



tlist = initParams['tlist']

    

initParams['miu'] = np.full((len(tlist)),0.0)

initParams['savings']= np.full((len(tlist)),initParams['optlrsav'])

initParams['saveOutput'] = True

info = timeEvolve(initState,initParams)





pickle_results('../dice-diffeqs_analyze/output',caseName,info)



with open('../dice-diffeqs_analyze/output' + '/' + caseName + '.csv', 'w') as f:

    for key in info.keys():

        f.write("%s,%s\n"%(key,info[key]))

    #f.write("%s,%s\n" %('act',act))

    #f.write("%s,%s\n" %('year',year))





#%%



   

maxIter = 30000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]











#caseName = 'test_1_0_0_0.015_10k'  # f for following

caseName = 'test_2_0_1_0.03_30k'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        

        # decisionType == 1, use prescribed savings rate

        #              == 2, optimize on savings rate in addition to other parameters

        #              == 3, estimate savings rate only

        #                          miu hard coded for no abatement.

        

        #decisionType = 3,

        decisionType = 2,

        

        # learningCurveOption == 0, single technology, vanilla DICE

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve 

        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 

        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 

        

        learningCurveOption = 0,

        

        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.

                                            

        innovationRatio = 0,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 550. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e10, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

        

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # pure rate of time preference (0.015 is DICE default ; for default, just comment out and don't define )

        

        prstp = 0.03,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost = 0 

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





#%%



maxIter = 10000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]









caseName = 'test_2_3_1_10k'  # f for following



caseName = 'test_2_3_1_10k'  # f for following



initState,initParams= createGlobalVariables(1,tlist,

        

        # decisionType == 1, estimate abatement rate and ratios only

        #              == 2, estimate abatement rates and ratios and savings rate

        #              == 3, estimate savings rate only

        

        decisionType = 2,

        

        # learningCurveOption == 0, vanilla DICE, single technology

        #                     == 1, single technology, with learning curve

        #                     == 2, dual technology, dual learning curves

        #                     == 3, dual technology, only second has learning curve

        #                           hard coded to ramp to zero between 2020 and 2050.

                                            

        learningCurveOption = 3,

        

        # learningCurveInitCost == initial cost for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitCost = 550. ,

        

        # learningCurveInitAmount == cumulative amount at time zero for learning curve.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveInitAmount  = 1e10, 

        

        # learningCurveExponent == slope of learning curve on log-log plot,

        #                       == exponent on powerlaw cost = cost0* cumAmount^exponent.

        # (scalar unless learningCurveOption = 2, in which case 2 element list)

        

        learningCurveExponent = 0.15200309344504995, 

        

        # utilityOption == 0 --> DICE utility function

        #               == 1 --> assume consumption == utility

        

        utilityOption = 1,

        

        # firstUnitFractionCost == cost of first unit

        

        firstUnitFractionalCost =[0,0.1]

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%



maxIter = 20000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]







for initCost in list(np.round(550*10.**(np.arange(-1.,1.05,0.05)))):

#for initCost in list(np.round(550*10.**(np.arange(-1.,1.6,0.1)))):

   

    #initAmount = 1100.* 1e9*0.15200309344504995

    #amount = (initCost/const)**(-1./0.15200309344504995)

        

    print(initCost)



    caseName = 'dual_learning_compl_'+str(initCost)+'_3_1e10-1e9_20k'  # f for following

    

    initState,initParams= createGlobalVariables(1,tlist, 

            learningCurveOption = 3,

            learningCurveInitCost = [550.,initCost] ,

            learningCurveInitAmount = [1e10,1e9],

            learningCurveExponent = [0.15200309344504995, 0.15200309344504995],

            utilityOption = 0,

            firstUnitFractionalCost = [0.1,0.1]

            )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

    

    #%%

maxIter = 20000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]







#for initCost in list(np.round(550*10.**(np.arange(-1.,1.05,0.05)))):

#for initCost in list(np.round(550*10.**(np.arange(-1.,1.6,0.1)))):

   

    #initAmount = 1100.* 1e9*0.15200309344504995

    #amount = (initCost/const)**(-1./0.15200309344504995)

        





caseName = 'single_learning_1_1e10_20k'  # f for following



initState,initParams= createGlobalVariables(1,tlist, 

        learningCurveOption = 1,

        learningCurveInitCost = 550. ,

        learningCurveInitAmount = 1e10,

        learningCurveExponent = 0.15200309344504995, 

        utilityOption = 0,

        firstUnitFractionalCost = 0.1

        )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%

  

    

maxIter = 20000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]





#for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:

for initCost in list(np.round(550*2**(np.arange(-3.125,4.5,0.125)))):

    

    #initAmount = 1100.* 1e9*0.15200309344504995

    #amount = (initCost/const)**(-1./0.15200309344504995)

        

    print(initCost)



    caseName = 'dual_learning_compl_'+str(initCost)+'_3_0.1_20k'  # f for following

    

    initState,initParams= createGlobalVariables(1,tlist, 

            learningCurveOption = 3,

            learningCurveInitCost = [550.,initCost] ,

            learningCurveInitAmount = [1e10,1e10],

            learningCurveExponent = [0.15200309344504995, 0.23446525363702297],

            utilityOption = 0,

            firstUnitFractionalCost = [0.1,0.1]

            )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



maxIter = 10000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]





#for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:

for initCost in [550,1100,2200,4400,8800,17600,35200]:

    

    initAmount = 1100.* 1e9*0.15200309344504995

    amount = (initCost/const)**(-1./0.15200309344504995)

        

    print(initCost, initAmount)



    caseName = 'dual_learning_'+str(initCost)+'_3f_10k'  # f for following

    

    initState,initParams= createGlobalVariables(1,tlist, 

                                                learningCurveOption = 3,

                                                learningCurveInitCost = [550.,initCost],

                                                learningCurveInitAmount = [1e10,initAmount],

                                                learningCurveExponent = [0.15200309344504995, 0.15200309344504995]

                                                )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%

initCost = 550

caseName = 'single_learning_'+str(initCost)+'_1_10k'  # f for following



initState,initParams= createGlobalVariables(1,tlist, 

                                            learningCurveOption = 1,

                                            learningCurveInitCost = 550.,

                                            learningCurveInitAmount = 1e10,

                                            learningCurveExponent = 0.15200309344504995,

                                            utilityOption = 0,

                                            firstUnitFractionalCost = 0

                                            )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%

initCost = 550

caseName = 'dual_learning_subs_'+str(initCost)+'_1_10k'  # f for following



initState,initParams= createGlobalVariables(1,tlist, 

            learningCurveOption = 2,

            learningCurveInitCost = [550.,1100.],

            learningCurveInitAmount = [1e10,1e10],

            learningCurveExponent = [0.15200309344504995,0.23446525363702297],

            utilityOption = 1,

            firstUnitFractionalCost = 0.5

            )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%

initCost = 1100

caseName = 'dual_learning_compl_'+str(initCost)+'_1_10k'  # f for following



initState,initParams= createGlobalVariables(1,tlist, 

            learningCurveOption = 3,

            learningCurveInitCost = [550.,initCost] ,

            learningCurveInitAmount = [1e10,1e10],

            learningCurveExponent = [0.15200309344504995, 0.23446525363702297],

            utilityOption = 0,

            firstUnitFractionalCost = [0,0]

            )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#%%







maxIter = 10000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]





for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:

        

    print(initCost)



    caseName = 'dual_learning_'+str(initCost)+'_3_10k'

    

    initState,initParams= createGlobalVariables(1,tlist, 

                                                learningCurveOption = 3,

                                                learningCurveInitCost = [550., initCost],

                                                learningCurveInitAmount = [1e10,1e9],

                                                learningCurveExponent = [0.15200309344504995, 0.15200309344504995]

                                                )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

    



maxIter = 10000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]





for initCost in [550,1100,2200,4400,8800,17600,35200]:

        

    print(initCost)



    caseName = 'dual_learning_'+str(initCost)+'_3_10k'

    

    initState,initParams= createGlobalVariables(1,tlist, 

                                                learningCurveOption = 3,

                                                learningCurveInitCost = [550., initCost],

                                                learningCurveInitAmount = [1e10,1e9],

                                                learningCurveExponent = [0.15200309344504995, 0.15200309344504995]

                                                )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

    





maxIter = 10000



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290, 295, 300]





for initCost in [767,769,766,768]:

        

    print(initCost)



    caseName = 'dual_learning_'+str(initCost)+'_10k'

    

    initState,initParams= createGlobalVariables(1,tlist, 

                                                learningCurveOption = 2,

                                                learningCurveInitCost = [550., initCost],

                                                learningCurveInitAmount = [1e10,1e9],

                                                learningCurveExponent = [0.15200309344504995, 0.15200309344504995]

                                                )

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





maxIter = 10000

caseName = 'dual_curve_test'



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290, 295, 300]





initState,initParams= createGlobalVariables(1,tlist, 

                                            learningCurveOption = 2,

                                            learningCurveInitCost = [550., 650.],

                                            learningCurveInitAmount = [1e10,1e9],

                                            learningCurveExponent = [0.15200309344504995, 0.3219280948873623]

                                            )



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)











maxIter = 10000





tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]





for initCost in [550,525,500,475,450,425,400,375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]:

    

    print(initCost)



    caseName = 'learningCurve_'+str(initCost)+'_uknwn_10_10k'

    



    const = 550.* 1e10**0.13750352375

    amount = (initCost/const)**(-1./0.13750352375)

    print(initCost,amount)

    initState,initParams= createGlobalVariables(1,tlist, learningCurveOption = 1, learningCurveInitCost = initCost, learningCurveInitAmount = amount)

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)









maxIter = 100000





tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]





for initCost in [550,525,500,475,450,425,400,375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]:

    

    print(initCost)



    caseName = 'learningCurve_'+str(initCost)+'_1e10_10_100k'

    initState,initParams= createGlobalVariables(1,tlist, learningCurve = True, learningCurveInitCost = initCost, learningCurveInitAmount = 1e10)

    

    resAbate = optDICEeq(maxIter, initState, initParams)

    

    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

    

    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





maxIter = 10000

caseName = 'cProfile_DICEeq'



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]





initState,initParams= createGlobalVariables(1,tlist)



cProfile.run("resAbate = optDICEeq(maxIter, initState, initParams)",filename="test01.out")



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)









maxIter = 10000

caseName = 'learningCurve_550_1e10_10'



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]





initState,initParams= createGlobalVariables(1,tlist, learningCurve = True, learningCurveInitCost = 550., learningCurveInitAmount = 1e10)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)









maxIter = 10000

caseName = 'Vanilla_step10_10k'



tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]





initState,initParams= createGlobalVariables(1,tlist)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)





maxIter = 10000

caseName = 'Vanilla_step10_10k'



tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]





initState,initParams= createGlobalVariables(1,tlist)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

#----------------



caseName = 'Vanilla_step5_10k'

maxIter = 10000

tlist = np.arange(0,305,5)





initState,initParams= createGlobalVariables(1,tlist)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)



#----------------



caseName = 'Vanilla_step20_10k'



tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,160,180,200,280,300]





initState,initParams= createGlobalVariables(1,tlist)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))



write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)









for rAbate in [1.,2.,5.,10.]:

    for rDamage in [1.,2.,5.,10.]:

        caseName = "res10k_A"+str(rAbate)+"_D"+str(rDamage)





        # case with abatement

        initState,initParams= createGlobalVariables(1,tlist,3)  # 3 is for the ramp-down case

        

        initParams['pback'] =  initParams['pback']/rAbate

        initParams['a1'] = initParams['a1'] * rDamage

        initParams['a2'] = initParams['a2'] * rDamage

        

        resAbate = optDICEeq(maxIter, initState, initParams)

        

        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

        

        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

        

# no abatement case

initState,initParams= createGlobalVariables(1,tlist, decisionType = 2)







resnoAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',prefix+'noAbate',filter_dic(resnoAbate ))



write_CSV_from_pickle(prefix+'noAbate')







prefix = "res10k_"

maxIter = 10000



tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]







# case with abatement

initState,initParams= createGlobalVariables(1,tlist, decisionType = 2)



resAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',prefix+'abate',filter_dic(resAbate))



write_CSV_from_pickle(prefix+'abate')



# no abatement case

initState,initParams= createGlobalVariables(1,tlist, decisionType = 2)



initParams['pback'] = 1000000 * initParams['pback']



resnoAbate = optDICEeq(maxIter, initState, initParams)



pickle_results('../dice-diffeqs_analyze/output',prefix+'noAbate',filter_dic(resnoAbate ))



write_CSV_from_pickle(prefix+'noAbate')





#-------------------------------

import pstats

p = pstats.Stats('cProfile.txt')

p.sort_stats('cumulative').print_stats(20)



------------



tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]





initState,initParams= createGlobalVariables(1,tlist)



initParams['miu']=[0.5]

initParams['t']=0

initParams['timeIndex']=0

initParams['saveOutput']=True



dstatedt(initState,initParams)





"""

