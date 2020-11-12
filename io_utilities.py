# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:50:02 2019

@author: kcaldeira
"""
import os
import pickle
import types
import re
import numpy as np

#%%
def pickle_results ( output_path, file_name, data ):
    
    #output results from DICE model into pickle file
    
    output_file_name = file_name + '.pickle'
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    with open(output_path + "/" + output_file_name, 'wb') as db:
        pickle.dump(data, db, protocol=pickle.HIGHEST_PROTOCOL)



#%%
def unpickle_results ( output_path, file_name ):
    
    #output results from DICE model into pickle file
    
    output_file_name = file_name + '.pickle'
    
    if not os.path.exists(output_path):
        print (output_path+' does not exist')
        exit()
        
    with open(output_path + "/" + output_file_name, 'rb') as db:
        data = pickle.load(db)
    
    return data

#%%
def write_CSV_from_pickle( output_path, file):
    LC = unpickle_results( output_path,  file)
    act = LC[2]['x']
    info = LC[3]
    #year = np.arange(2015, 2015+global_params['T']*global_params['tstep'], global_params['tstep'])

    with open(output_path + '/' + file + '.csv', 'w') as f:
        for key in info.keys():
            item = np.array(info[key])
            # don't print scalars
            if 1 == len(item.shape):
                # vector
                f.write("%s,%s\n"%(key,re.sub("\ \ +"," ",str(list(info[key]))[1:-1].replace("\n","")).replace(" ",",").replace(",,",",").replace(",,",",")))
            elif 2 == len(item.shape):
                # array
                for idx in range(item.shape[1]):  # loop over columns
                    f.write("%s,%s\n"%(key+'_'+str(idx),re.sub("\ \ +"," ",str(list(item[:,idx]))[1:-1].replace("\n","")).replace(" ",",").replace(",,",",").replace(",,",","))) 
            else:
                print ('not exported = ',key," ",item.shape)
            # f.write("%s,%s\n"%(key,info[key]))
        f.write("%s,%s\n" %('act',str(act)[1:-1]))
        # f.write("%s,%s\n" %('act',act))
        #f.write("%s,%s\n" %('year',year))

#%%
#  filter out lambda functions etc

def filter_dic(dic_in):
    if isinstance(dic_in, list):  # if list, iterate on each element in list
        dic_out = [filter_dic(x) for x in dic_in]
    elif isinstance(dic_in, dict):
        dic_out = {}
        for (key,value) in dic_in.items():
            if isinstance(value, dict):
                dic_out[key] = filter_dic(value)
            if not callable(value):
                dic_out[key] = value
    else:
        dic_out = dic_in
    return dic_out
            
        