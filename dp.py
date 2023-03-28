# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 12:37:15 2023

@author: Alina
"""

import numpy as np
import math

def FindAssociated(c, ab, base, L):
    # distance from the farthest point to the base
    b = math.sqrt(c**2+base[1]**2)
    # distance from the farthest point to greedy
    dist = (L**2-2*L*b)/(2*(L-b-c))
    c_ass = c-dist
    for i in range(0,ab.shape[0]):
        if (c_ass > ab[i-1,1]) & (c_ass < ab[i,0]):
            c_ass = ab[i,0]
        if (c_ass < ab[0,0]):
            c_ass = ab[0,0]  
    return c_ass


def Candidates(base, L, ab):
    on_gap = False
    xB = ab[ab.shape[0]-1,1]
    c = np.array(xB)
    c_ass = np.array(FindAssociated(xB, ab, base, L))
    while not on_gap:
        # distance from the farthest point to the base
        b = math.sqrt(xB**2+base[1]**2)
        # distance from the farthest point to greedy
        dist = (L**2-2*L*b)/(2*(L-b-xB))
        # greedy point coordinate
        xA = xB-dist
        ass = FindAssociated(xA, ab, base, L)  
        c = np.append(c, xA)
        c_ass = np.append(c_ass, ass)
        xB = xA
        for i in range(0,ab.shape[0]):
            if (xA > ab[i-1,1]) & (xA < ab[i,0]):
                on_gap = True 
            if (xA < ab[0,0]):
                on_gap = True 
    c = c[:c.size-1]
    c_ass = c_ass[:c_ass.size-1]
    return c, c_ass

def AllCandidates(base, L, ab):
    ab_cut = ab
    c = np.empty(0)
    c_ass = np.empty(0)
    while not (ab_cut.size == 0):
        c_i, c_ass_i = Candidates(base, L, ab_cut)
        c = np.append(c, c_i)
        c_ass = np.append(c_ass, c_ass_i)       
        ab_cut = ab_cut[:ab_cut.shape[0]-1]
    return c, c_ass

def SegmentNumber(c, ab):
    for i in range(0,ab.shape[0]):
        if (c >= ab[i,0]) & (c <= ab[i,1]):
            return i 

def Recursion(c, ab, base, L):
    c_ass = FindAssociated(c, ab, base, L)
    j = np.arange(SegmentNumber(c_ass, ab), SegmentNumber(c, ab)+1)
    print(c)    
    print(c_ass)    
    if c_ass == ab[0,0]:
        return (c - ab[0,0])
    
    elif c_ass in ab[1:,0]:
        func = np.empty(0)
        for i in j:
            func = np.append(func, Recursion(ab[i-1,1], ab, base, L))    
        func1 = (c - ab[j,0]) + func
        return min(func1)
    
    else: 
        func = np.empty(0)
        for i in j:
            func = np.append(func, Recursion(ab[i-1,1], ab, base, L))    
        func1 = (c - ab[j,0]) + func
        
        func2 = L + Recursion(c_ass, ab, base, L)
        
        return min(func2, min(func1))
    
def DynamicProgramming(c, ab, base, L):
    c = np.sort(c)
    E = np.zeros(c.size) # check if zeros are ok
    
    for k in range(0, c.size):
        c_ass = FindAssociated(c[k], ab, base, L)
    
        j = np.arange(SegmentNumber(c_ass, ab), SegmentNumber(c[k], ab)+1)  
    
        if c_ass == ab[0,0]:
            #print('caso 1')
            E[k] = (c[k] - ab[0,0])
            

        elif c_ass in ab[1:,0]:
            print('caso 2')
            func = np.empty(0)
            for i in j:
                func = np.append(func, (c[k] - ab[i,0]) + E[c.tolist().index(ab[i-1,1])])
            print(func)
            E[k] = min(func)
    
        else: 
            print('caso 3')
            print(j)
            func = np.empty(0)
            for i in j:
                func = np.append(func, (c[k] - ab[i,0]) + E[c.tolist().index(ab[i-1,1])])
            print(func)
            
        
            func2 = L + E[c.tolist().index(c_ass)]
            E[k] = min(func2, min(func))
            
    return E

def FindCentralTours(c_left, c_right , base, L):
    i = 0
    j = 0
    central_tours = np.empty((0,3))
    tour_lenght = 0
    while (tour_lenght <= L) and (j < c_left.size):
        central_tours_1 = np.empty((0,3))
        while (tour_lenght <= L) and (i < c_right.size):
            dist_left = math.sqrt(c_left[j]**2+base[1]**2)
            dist_right = math.sqrt(c_right[i]**2+base[1]**2)
            tour_lenght = c_left[j] + c_right[i] + dist_left + dist_right
            tour = np.array((c_left[j], c_right[i], tour_lenght)).reshape(1,3)
            central_tours_1 = np.append(central_tours_1, tour, axis=0)
            i += 1
        central_tours = np.append(central_tours, central_tours_1, axis=0)
        tour_lenght = 0
        j += 1
    return central_tours
