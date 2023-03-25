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
    c_ass = c-dist 
    return c, c_ass

def AllCandidates(base, L, ab):
    ab_cut = ab
    c = np.empty(0)
    c_ass = np.empty(0)
    while not (ab_cut.size == 0):
        c_i, c_ass_i = Candidates(base, L, ab_cut)
        c = np.append(c, c_i)
        c_ass = np.append(c_ass, c_ass_i)  
        for j in range(0, c_ass.size):
            for i in range(0,ab.shape[0]):
                if (c_ass[j] > ab[i-1,1]) & (c_ass[j] < ab[i,0]):
                    c_ass[j] = ab[i,0]
                if (c_ass[j] < ab[0,0]):
                    c_ass[j] = ab[0,0]      
        ab_cut = ab_cut[:ab_cut.shape[0]-1]
    return c, c_ass



