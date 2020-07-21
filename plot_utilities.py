# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 12:55:43 2019

@author: kcaldeira
"""


import numpy as np
import matplotlib.pyplot as plt

#%%

def qplot(x0,y0=[],xlabel='',ylabel='',title='',filename=''):
    
    if len(y0)==0:  #  one data argument
        if len(np.array(x0).shape) == 1:
            plt.plot(x0) # if vector, just plot it
        else: # assume all args are in x, with first column as x values
            x = np.array(x0)[:,0]
            y = np.array(x0)[:,1:]
            plt.plot(x,y)
    else:  # two data arguments
        if len(np.array(y0).shape) == 1:
            plt.plot(x0,y0)
        elif np.array(y0).shape[1] == len(x0): # check if y values need transposition
            y = np.array(y0).transpose()
            plt.plot(x0, y)
        else:
            plt.plot(x0, y0)

    if xlabel != '':
        plt.xlabel(xlabel)
    if ylabel != '':
        plt.ylabel(ylabel)
    if title != '':
        plt.title(title)
    plt.grid(True)
    if filename != '':
        plt.savefig(filename)
    plt.show()


#%%

def minus(a,b):
    return np.array(a)-np.array(b)

#%%

def qplot2(dic1,dic2,var):
    qplot(minus(dic1[var],dic2[var]))