# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:56:46 2020

@author: kcaldeira
"""

import numpy as np
import csv

def csvWriteVector(csv_file,a_dict):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(a_dict.keys())
            writer.writerows(zip(*a_dict.values()))
    except IOError:
        print("I/O error")

def csvWriteScalar(csv_file,a_dict):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key,item in a_dict.items():
                if type(item) in [int,float,str]:
                    writer.writerow([key,item])
                elif type(item) in [list, np.ndarray]:
                    new_item = [key] + item
                    writer.writerow(new_item)
    except IOError:
        print("I/O error")
