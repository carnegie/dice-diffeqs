# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:15:46 2020

@author: kcaldeira

Computer ROI on ramp down to 50 as function of abatement cost and 
"""


from DICEeq import *
from plot_utilities import *
from io_utilities import *
import cProfile

variationVec = 10**np.arange(-1,1)