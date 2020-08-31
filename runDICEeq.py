# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:53:40 2020

@author: kcaldeira
"""
from DICEeq import *
from plot_utilities import *
from io_utilities import *
import cProfile
   
maxIter = 10000

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]
tmax = 300




caseName = 'test_1_0_1_0.03_10k'  # f for following

initState,initParams= createGlobalVariables(tmax,1,tlist,
        
        # decisionType == 1, use prescribed savings rate
        #              == 2, optimize on savings rate in addition to other parameters
        #              == 3, estimate savings rate only
        #                          miu hard coded to ramp to zero between 2020 and 2050.
        
        decisionType = 1,
        
        # learningCurveOption == 0, single technology, vanilla DICE
        #                     == 1, single technology, with learning curve
        #                     == 2, dual technology, dual learning curves
        #                     == 3, dual technology, only second has learning curve 
        #                     == 4, dual technology, only second has learning curve, potential for curve shifting investment 
        #                     == 5, dual technology, only second has learning curve, potential for curve following investment 
        
        innovationRatio = 0,
        
        # fractional cost reduction per $ invested in innovation, i.e., 1e-12 means a 0.1% cost reduction per billion dollars invested.
                                            
        learningCurveOption = 0,
        
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
        
        # pure rate of time preference
        
        prstp = 0.03,
        
        # firstUnitFractionCost == cost of first unit
        
        firstUnitFractionalCost = 0 
        )

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

#%%
"""
maxIter = 10000

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 110, 130,150,200,280,290,300]
tmax = 300



caseName = 'test_2_3_1_10k'  # f for following

caseName = 'test_2_3_1_10k'  # f for following

initState,initParams= createGlobalVariables(tmax,1,tlist,
        
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
tmax = 300


for initCost in list(np.round(550*10.**(np.arange(-1.,1.05,0.05)))):
#for initCost in list(np.round(550*10.**(np.arange(-1.,1.6,0.1)))):
   
    #initAmount = 1100.* 1e9*0.15200309344504995
    #amount = (initCost/const)**(-1./0.15200309344504995)
        
    print(initCost)

    caseName = 'dual_learning_compl_'+str(initCost)+'_3_1e10-1e9_20k'  # f for following
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300


#for initCost in list(np.round(550*10.**(np.arange(-1.,1.05,0.05)))):
#for initCost in list(np.round(550*10.**(np.arange(-1.,1.6,0.1)))):
   
    #initAmount = 1100.* 1e9*0.15200309344504995
    #amount = (initCost/const)**(-1./0.15200309344504995)
        


caseName = 'single_learning_1_1e10_20k'  # f for following

initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

#for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:
for initCost in list(np.round(550*2**(np.arange(-3.125,4.5,0.125)))):
    
    #initAmount = 1100.* 1e9*0.15200309344504995
    #amount = (initCost/const)**(-1./0.15200309344504995)
        
    print(initCost)

    caseName = 'dual_learning_compl_'+str(initCost)+'_3_0.1_20k'  # f for following
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

#for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:
for initCost in [550,1100,2200,4400,8800,17600,35200]:
    
    initAmount = 1100.* 1e9*0.15200309344504995
    amount = (initCost/const)**(-1./0.15200309344504995)
        
    print(initCost, initAmount)

    caseName = 'dual_learning_'+str(initCost)+'_3f_10k'  # f for following
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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

initState,initParams= createGlobalVariables(tmax,1,tlist, 
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

initState,initParams= createGlobalVariables(tmax,1,tlist, 
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

initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

for initCost in [25,50,100,200,400,800,1600,3200,6400,12800,25600,51200,102400]:
        
    print(initCost)

    caseName = 'dual_learning_'+str(initCost)+'_3_10k'
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

for initCost in [550,1100,2200,4400,8800,17600,35200]:
        
    print(initCost)

    caseName = 'dual_learning_'+str(initCost)+'_3_10k'
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

for initCost in [767,769,766,768]:
        
    print(initCost)

    caseName = 'dual_learning_'+str(initCost)+'_10k'
    
    initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist, 
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
tmax = 300

for initCost in [550,525,500,475,450,425,400,375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]:
    
    print(initCost)

    caseName = 'learningCurve_'+str(initCost)+'_uknwn_10_10k'
    

    const = 550.* 1e10**0.13750352375
    amount = (initCost/const)**(-1./0.13750352375)
    print(initCost,amount)
    initState,initParams= createGlobalVariables(tmax,1,tlist, learningCurveOption = 1, learningCurveInitCost = initCost, learningCurveInitAmount = amount)
    
    resAbate = optDICEeq(maxIter, initState, initParams)
    
    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))
    
    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)




maxIter = 100000


tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

for initCost in [550,525,500,475,450,425,400,375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]:
    
    print(initCost)

    caseName = 'learningCurve_'+str(initCost)+'_1e10_10_100k'
    initState,initParams= createGlobalVariables(tmax,1,tlist, learningCurve = True, learningCurveInitCost = initCost, learningCurveInitAmount = 1e10)
    
    resAbate = optDICEeq(maxIter, initState, initParams)
    
    pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))
    
    write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


maxIter = 10000
caseName = 'cProfile_DICEeq'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

cProfile.run("resAbate = optDICEeq(maxIter, initState, initParams)",filename="test01.out")

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)




maxIter = 10000
caseName = 'learningCurve_550_1e10_10'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist, learningCurve = True, learningCurveInitCost = 550., learningCurveInitAmount = 1e10)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)




maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)


maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)
#----------------

caseName = 'Vanilla_step5_10k'
maxIter = 10000
tlist = np.arange(0,305,5)
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)

#----------------

caseName = 'Vanilla_step20_10k'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)




for rAbate in [1.,2.,5.,10.]:
    for rDamage in [1.,2.,5.,10.]:
        caseName = "res10k_A"+str(rAbate)+"_D"+str(rDamage)


        # case with abatement
        initState,initParams= createGlobalVariables(tmax,1,tlist,3)  # 3 is for the ramp-down case
        
        initParams['pback'] =  initParams['pback']/rAbate
        initParams['a1'] = initParams['a1'] * rDamage
        initParams['a2'] = initParams['a2'] * rDamage
        
        resAbate = optDICEeq(maxIter, initState, initParams)
        
        pickle_results('../dice-diffeqs_analyze/output',caseName,filter_dic(resAbate))
        
        write_CSV_from_pickle('../dice-diffeqs_analyze/output',caseName)
        
# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)



resnoAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',prefix+'noAbate',filter_dic(resnoAbate ))

write_CSV_from_pickle(prefix+'noAbate')



prefix = "res10k_"
maxIter = 10000

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300


# case with abatement
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('../dice-diffeqs_analyze/output',prefix+'abate',filter_dic(resAbate))

write_CSV_from_pickle(prefix+'abate')

# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)

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
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

initParams['miu']=[0.5]
initParams['t']=0
initParams['timeIndex']=0
initParams['saveOutput']=True

dstatedt(initState,initParams)


"""
