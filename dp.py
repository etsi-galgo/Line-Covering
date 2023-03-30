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
    while not on_gap:
        # distance from the farthest point to the base
        b = math.sqrt(xB**2+base[1]**2)
        # distance from the farthest point to greedy
        dist = (L**2-2*L*b)/(2*(L-b-xB))
        # greedy point coordinate
        xA = xB-dist
        c = np.append(c, xA)
        xB = xA
        for i in range(0,ab.shape[0]):
            if (xA > ab[i-1,1]) & (xA < ab[i,0]):
                on_gap = True 
            if (xA < ab[0,0]):
                on_gap = True 
    c = c[:c.size-1]
    return c

def AllCandidates(base, L, ab):
    ab_cut = ab
    c = np.empty(0)
    while not (ab_cut.size == 0):
        c_i = Candidates(base, L, ab_cut)
        c = np.append(c, c_i)       
        ab_cut = ab_cut[:ab_cut.shape[0]-1]
    return c

def SegmentNumber(c, ab):
    for i in range(0,ab.shape[0]):
        if (c >= ab[i,0]) & (c <= ab[i,1]):
            return i  

def TourLenght(point1, point2, base):
    return point1 - point2 + math.sqrt(point1**2+base[1]**2) + math.sqrt(point2**2+base[1]**2)

def Recursion(c_k, ab, base, L):
    c_ass = FindAssociated(c_k, ab, base, L)
    j = np.arange(SegmentNumber(c_ass, ab), SegmentNumber(c_k, ab)+1)   
    if c_ass == ab[0,0]:
        return TourLenght(c_k, ab[0,0], base)
    
    elif c_ass in ab[1:,0]:
        func = np.empty(0)
        for i in j:
            func = np.append(func, TourLenght(c_k, ab[i,0], base) + Recursion(ab[i-1,1], ab, base, L))    
        #func1 = (c_k - ab[j,0]) + func
        print(func)
        return min(func)
    
    else: 
        func = np.empty(0)
        for i in j:
            func = np.append(func, TourLenght(c_k, ab[i,0], base) + Recursion(ab[i-1,1], ab, base, L))    
        #func1 = (c_k - ab[j,0]) + func
        
        func2 = L + Recursion(c_ass, ab, base, L)
        
        return min(func2, min(func))
    
def DynamicProgramming(c, ab, base, L):
    c = np.sort(c)
    E = np.zeros(c.size) # check if zeros are ok
    

    for k in range(0, c.size):
        c_ass = FindAssociated(c[k], ab, base, L)
    
        j = np.arange(SegmentNumber(c_ass, ab), SegmentNumber(c[k], ab)+1)  
    
        if c_ass == ab[0,0]:
            E[k] = TourLenght(c[k], ab[0,0], base)
            
        elif c_ass in ab[1:,0]:
            func = np.empty(0)
            for i in j:
                func = np.append(func, TourLenght(c[k], ab[i,0], base) + E[c.tolist().index(ab[i-1,1])])
            E[k] = min(func)
    
        else: 
            func = np.empty(0)
            for i in j:
                func = np.append(func, TourLenght(c[k], ab[i,0], base) + E[c.tolist().index(ab[i-1,1])])      
            func2 = L + E[c.tolist().index(c_ass)]
            E[k] = min(func2, min(func))
            
    return E[c.size-1]

def SeparateLeftRight(ab, base):
    ab_right = ab[np.argmax(ab[:,0] > base[0]):] - base[0]
    ab_left = np.flip(base[0] - ab[:np.argmax(ab[:,1] > base[0])])
    return ab_left, ab_right

def FindCentralTours(c_left, c_right , base, L):
    j = 0
    central_tours = np.empty((0,3))
    tour_lenght = 0
    while (tour_lenght <= L) and (j < c_left.size):
        central_tours_1 = np.empty((0,3))
        i = 0
        while (tour_lenght <= L) and (i < c_right.size):
            dist_left = math.sqrt(c_left[j]**2+base[1]**2)
            dist_right = math.sqrt(c_right[i]**2+base[1]**2)
            tour_lenght = c_left[j] + c_right[i] + dist_left + dist_right
            tour = np.array((c_left[j], c_right[i], tour_lenght)).reshape(1,3)
            central_tours_1 = np.append(central_tours_1, tour, axis=0)
            i += 1
        central_tours = np.append(central_tours, central_tours_1[central_tours_1[:,2]<=L,:], axis=0)
        tour_lenght = 0
        j += 1
    return central_tours

def OneSideDynamics(c, c_first, ab, base, L):
    E = np.zeros(c_first.size)
    ab_i = ab.astype(np.float64)
    for i in range(0, c_first.size):
        if c_first[i] != ab_i[0,1]:
            ab_i[0,0] = c_first[i]
        else:
            ab_i = ab[ab[:,0]>c_first[i]].astype(np.float64)
        if (c[c>c_first[i]].size != 0):
            E[i] = DynamicProgramming(c[c>c_first[i]], ab_i, base, L) 
        else: E[i] = 0
    return E

def BothSidesDynamics(ab, base, L):
    ab_left, ab_right = SeparateLeftRight(ab, base)
    
    c_right = np.sort(AllCandidates(base, L, ab_right))
    c_left =  np.sort(AllCandidates(base, L, ab_left))
    
    central_tours = FindCentralTours(c_left, c_right , base, L)
    
    c_left_first = np.unique(np.sort(central_tours[:,0]))
    c_right_first = np.unique(np.sort(central_tours[:,1]))
    
    E_left = OneSideDynamics(c_left, c_left_first, ab_left, base, L)
    E_right = OneSideDynamics(c_right, c_right_first, ab_right, base, L)
    
    left_central = np.append(c_left_first.reshape(E_left.shape[0],1), E_left.reshape(E_left.shape[0],1), axis=1)
    right_central = np.append(c_right_first.reshape(E_right.shape[0],1), E_right.reshape(E_right.shape[0],1), axis=1)
    
    totalL = np.zeros(central_tours.shape[0])
    for i in range (0,central_tours.shape[0]):
        a = tuple(np.argwhere(left_central == central_tours[i,0])[0])
        b = tuple(np.argwhere(right_central == central_tours[i,1])[0])
        totalL[i] = left_central[a[0],1] + right_central[b[0],1] + float(central_tours[i,2])
    
    E_left_max = DynamicProgramming(c_left, ab_left, base, L)
    E_right_max = DynamicProgramming(c_right, ab_right, base, L)
    
    return min((E_left_max + E_right_max), min(totalL))
