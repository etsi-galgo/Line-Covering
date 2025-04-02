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
    print(lenght, n)
    segment_centers = np.array(sorted(random.sample(range(50, lenght-51), n))) # random center of the segments
    x=segment_centers-np.random.randint(20, 30, n)
    y=segment_centers+np.random.randint(20, 30, n)
    xy=np.stack((x, y), axis=1)
    
    for i in range(1,n):
        if xy[n-i-1,1]>=xy[n-i,0]:
            xy = np.delete(xy, n-i-1, axis=0)
            
    n = xy.shape[0]
    # positive points coordinates
    a = np.arange(xy[0,0],xy[0,1]+1)
    for i in range(1,n):
        a = np.concatenate((a, np.arange(xy[i,0],xy[i,1]+1)))
    print("We have to cover the following segments: \n", xy-base[0])
        
    return n, xy-base[0], a-base[0]

