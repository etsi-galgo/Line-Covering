# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:37:35 2024

@author: Alina
"""

import numpy as np
import random

def generate(lenght, n, base):
    """
    Creating a line with n random segments
    """
    xy = np.array(sorted(random.sample(range(0, lenght-1), n*2))) # random start and end of the segments
    xy = xy.reshape((n,2)) # start and end of the segments coordinates
    # positive points coordinates
    a = np.arange(xy[0,0],xy[0,1]+1)
    for i in range(1,n):
        a = np.concatenate((a, np.arange(xy[i,0],xy[i,1]+1)))
    print("We have to cover the following segments: \n", xy-base[0])
        
    return xy-base[0], a-base[0]

