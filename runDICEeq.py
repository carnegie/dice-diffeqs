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


tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

for initCost in [550,525,500,475,450,425,400,375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]:
    
    print(initCost)

    caseName = 'learningCurve_'+str(initCost)+'_1e10_10'
    initState,initParams= createGlobalVariables(tmax,1,tlist, learningCurve = True, learningCurveInitCost = initCost, learningCurveInitAmount = 1e10)
    
    resAbate = optDICEeq(maxIter, initState, initParams)
    
    pickle_results('./output',caseName,filter_dic(resAbate))
    
    write_CSV_from_pickle('./output',caseName)


"""
maxIter = 10000
caseName = 'cProfile_DICEeq'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

cProfile.run("resAbate = optDICEeq(maxIter, initState, initParams)",filename="test01.out")

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)




maxIter = 10000
caseName = 'learningCurve_550_1e10_10'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,120,140,160,180,200,250,280,290, 295, 300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist, learningCurve = True, learningCurveInitCost = 550., learningCurveInitAmount = 1e10)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)




maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)


maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)
#----------------

caseName = 'Vanilla_step5_10k'
maxIter = 10000
tlist = np.arange(0,305,5)
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)

#----------------

caseName = 'Vanilla_step20_10k'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',caseName,filter_dic(resAbate))

write_CSV_from_pickle('./output',caseName)




for rAbate in [1.,2.,5.,10.]:
    for rDamage in [1.,2.,5.,10.]:
        caseName = "res10k_A"+str(rAbate)+"_D"+str(rDamage)


        # case with abatement
        initState,initParams= createGlobalVariables(tmax,1,tlist,3)  # 3 is for the ramp-down case
        
        initParams['pback'] =  initParams['pback']/rAbate
        initParams['a1'] = initParams['a1'] * rDamage
        initParams['a2'] = initParams['a2'] * rDamage
        
        resAbate = optDICEeq(maxIter, initState, initParams)
        
        pickle_results('./output',caseName,filter_dic(resAbate))
        
        write_CSV_from_pickle('./output',caseName)
        
# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)



resnoAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',prefix+'noAbate',filter_dic(resnoAbate ))

write_CSV_from_pickle(prefix+'noAbate')



prefix = "res10k_"
maxIter = 10000

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300


# case with abatement
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)

resAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',prefix+'abate',filter_dic(resAbate))

write_CSV_from_pickle(prefix+'abate')

# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist, decisionType = 2)

initParams['pback'] = 1000000 * initParams['pback']

resnoAbate = optDICEeq(maxIter, initState, initParams)

pickle_results('./output',prefix+'noAbate',filter_dic(resnoAbate ))

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
