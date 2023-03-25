# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 12:37:15 2023

@author: Alina
"""

import numpy as np
import math

def Candidates(base, L, ab):
    on_gap = False
    xB = ab[ab.shape[0]-1,1]
    c = np.array(xB)
    while not on_gap:
        # distance from the farthest point to the base
        b = math.sqrt(xB**2+base[1]**2)
        # distance from the farthest point to greedy
        dist = (L**2-2*L*b)/(2*(L-b-xB))
        # greedy point coordinate
        xA = xB-dist
        c = np.append(c,xA)
        xB = xA
        for i in range(0,ab.shape[0]):
            if (xA>ab[i-1,1])&(xA<ab[i,0]):
                on_gap = True 
            if (xA<ab[0,0]):
                on_gap = True 
    c = c[:c.size-1]
    return c

