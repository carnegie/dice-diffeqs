# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:53:40 2020

@author: kcaldeira
"""
from DICEeq import *
from plot_utilities import *
from io_utilities import *
import cProfile

maxIter = 1000
caseName = 'cProfile_DICEeq'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,2)

cProfile.run("resAbate = optDICEeq(maxIter)",filename="test01.out")

pickle_results('.',caseName,filter_dic(resAbate))

write_CSV_from_pickle(caseName)

"""
maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,1)

resAbate = optDICEeq(maxIter)

pickle_results('.',caseName,filter_dic(resAbate))

write_CSV_from_pickle(caseName)


maxIter = 10000
caseName = 'Vanilla_step10_10k'

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,1)

resAbate = optDICEeq(maxIter)

pickle_results('.',caseName,filter_dic(resAbate))

write_CSV_from_pickle(caseName)
#----------------

caseName = 'Vanilla_step5_10k'
maxIter = 10000
tlist = np.arange(0,305,5)
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,1)

resAbate = optDICEeq(maxIter)

pickle_results('.',caseName,filter_dic(resAbate))

write_CSV_from_pickle(caseName)

#----------------

caseName = 'Vanilla_step20_10k'

tlist = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,1)

resAbate = optDICEeq(maxIter)

pickle_results('.',caseName,filter_dic(resAbate))

write_CSV_from_pickle(caseName)




for rAbate in [1.,2.,5.,10.]:
    for rDamage in [1.,2.,5.,10.]:
        caseName = "res10k_A"+str(rAbate)+"_D"+str(rDamage)


        # case with abatement
        initState,initParams= createGlobalVariables(tmax,1,tlist,3)  # 3 is for the ramp-down case
        
        initParams['pback'] =  initParams['pback']/rAbate
        initParams['a1'] = initParams['a1'] * rDamage
        initParams['a2'] = initParams['a2'] * rDamage
        
        resAbate = optDICEeq(maxIter)
        
        pickle_results('.',caseName,filter_dic(resAbate))
        
        write_CSV_from_pickle(caseName)
        
# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist,2)



resnoAbate = optDICEeq(maxIter)

pickle_results('.',prefix+'noAbate',filter_dic(resnoAbate ))

write_CSV_from_pickle(prefix+'noAbate')



prefix = "res10k_"
maxIter = 10000

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300


# case with abatement
initState,initParams= createGlobalVariables(tmax,1,tlist,2)

resAbate = optDICEeq(maxIter)

pickle_results('.',prefix+'abate',filter_dic(resAbate))

write_CSV_from_pickle(prefix+'abate')

# no abatement case
initState,initParams= createGlobalVariables(tmax,1,tlist,2)

initParams['pback'] = 1000000 * initParams['pback']

resnoAbate = optDICEeq(maxIter)

pickle_results('.',prefix+'noAbate',filter_dic(resnoAbate ))

write_CSV_from_pickle(prefix+'noAbate')


#-------------------------------
import pstats
p = pstats.Stats('cProfile.txt')
p.sort_stats('cumulative').print_stats(20)

------------

tlist = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,280,300]
tmax = 300

initState,initParams= createGlobalVariables(tmax,1,tlist,1)

initParams['miu']=[0.5]
initParams['t']=0
initParams['timeIndex']=0
initParams['saveOutput']=True

dstatedt(initState,initParams)


"""
