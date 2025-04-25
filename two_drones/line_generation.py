# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:37:35 2024

@author: Alina
"""

import numpy as np
import random

def generate(lenght, n, cv, dens, base):
    """
    Creating a line with n random segments
    """
    
    mean = np.random.uniform(10, 100)  # Random mean
    std = cv * mean
    # Generate real numbers
    values = np.random.normal(loc=mean, scale=std, size=n)
    
    # Clip to avoid negatives and round to integers
    values = np.clip(values, a_min=1, a_max=None).round().astype(int)
    

    # Check actual stats
    actual_mean = np.mean(values)
    actual_std = np.std(values)
    actual_cv = actual_std / actual_mean
    
    x=[]
    y=[]
    i=0
    xi=0
    while xi<dens*lenght:
        yi=xi+values[i]
        x.append(xi)
        y.append(yi)
        i+=1
        xi=yi
    xy=np.stack((x, y), axis=1)
    density=y[-1]/lenght
    
    G = lenght-y[-1] #Rest to distribute between gaps
    ng = len(x)+1 #Number of gaps including before and after all
    gaps = split(G, ng)
    
    for i in range(len(x)):
        x[i]=x[i]+sum(gaps[0:i+1])
        y[i]=y[i]+sum(gaps[0:i+1])
        
    xy=np.stack((x, y), axis=1)
    n = xy.shape[0]
    
    # positive points coordinates
    a = np.arange(xy[0,0],xy[0,1]+1)
    for i in range(1,n):
        a = np.concatenate((a, np.arange(xy[i,0],xy[i,1]+1)))
    print("We have to cover the following segments: \n", xy-base[0])
        
    return mean, actual_mean, actual_cv, density, n, xy-base[0], a-base[0]

def split(G, n):
    # Step 1: Generate n-1 sorted unique cut points between 1 and L-1
    cuts = sorted(random.sample(range(1, G), n - 1))
    
    # Step 2: Add the boundaries (0 and L)
    positions = [0] + cuts + [G]
    
    # Step 3: Compute segment lengths as differences
    segments = [positions[i+1] - positions[i] for i in range(n)]
    
    return segments