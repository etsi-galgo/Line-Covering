# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:06:59 2024

@author: Alina Kasiuk
"""

import numpy as np
import math
from utils import perimeter

def candidates(base, L, ab):
    """
    Making the greedy jumps to find candidate points c
    """
    on_gap = False
    xB = ab[ab.shape[0]-1,1]
    c = np.array(xB)
    while not on_gap:
        # distance from the farthest point to the base
        b = math.sqrt(xB**2+base[1]**2)
        # distance from the farthest point to greedy
        dist = (L**2-2*L*b)/(2*(L-b-xB))
        # greedy point coordinate
        xA = xB-math.floor(dist)
        c = np.append(c, xA)
        
        xB = xA
        for i in range(0,ab.shape[0]):
            if (xA > ab[i-1,1]) & (xA < ab[i,0]):
                on_gap = True 
            if (xA < ab[0,0]):
                on_gap = True 
    c = c[:c.size-1]
    return c

def all_candidates(base, L, ab):
    """
    Construction of the candidate set 𝐶={c_i}
    """    
    ab_cut = ab
    c = np.empty(0)
    while not (ab_cut.size == 0):
        c_i = candidates(base, L, ab_cut)
        c = np.append(c, c_i)       
        ab_cut = ab_cut[:ab_cut.shape[0]-1]
    return c

def find_associated(c, ab, base, L):
    """
    For a given point c find its associated point 𝑐′
    """
    # distance from the farthest point to the base
    b = math.sqrt(c**2+base[1]**2)
    # distance from the farthest point to greedy
    dist = (L**2-2*L*b)/(2*(L-b-c))
    c_ass = c-math.floor(dist)
    for i in range(0,ab.shape[0]):
        if (c_ass > ab[i-1,1]) & (c_ass < ab[i,0]):
            c_ass = ab[i,0]
        if (c_ass < ab[0,0]):
            c_ass = ab[0,0]  
    return c_ass

def segment_number(c, ab):
    """
    For a point c find a segment it belongs to
    """
    for i in range(0,ab.shape[0]):
        if (c >= ab[i,0]) & (c <= ab[i,1]):
            return i  
        
def separate_left_right(ab, base):
    """
    Separate the segment into two groups: left and right from the base
    """

    if (ab[-1,0]>=0):
        ab_right = ab[np.argmax(ab[:,0] > 0):]
    else:
        ab_right = np.empty((0,2))
        
    if (ab[0,1]<=0):
        ab_left = -np.flip(ab[:np.argmax(ab[:,1] > 0)])
    else:
        ab_left = np.empty((0,2))       
    
    
    for i in range(0,ab.shape[0]):
        if (0 > ab[i,0]) & (0 < ab[i,1]):
            central_right = np.array([[0, ab[i,1]]])
            central_left = -(np.array([[0,ab[i,0]]]))
            ab_right = np.append(central_right, ab_right, axis=0)
            ab_left = np.append(central_left, ab_left, axis=0)
    return ab_left, ab_right

def find_central_tours(c_left, c_right , base, L):
    """
    Find a set of segments that can be covered from left to right and vice versa
    """   
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

def DP_one_side(c, ab, base, L):   

    """
    One side dynamic programming implementation
    """
    c = np.sort(c)  
    E = np.zeros(c.size) # check if zeros are ok
    Start_Points = - np.ones((c.size,c.size)) # check if zeros are ok
    End_Points = - np.ones((c.size,c.size))

    for k in range(0, c.size):
        c_ass = find_associated(c[k], ab, base, L)
        
        j = np.arange(segment_number(c_ass, ab), segment_number(c[k], ab)+1)  
        
        if c_ass == ab[0,0]:
            E[k] = perimeter(c[k], ab[0,0], base[1])  

            
            Start_Points[k,0] = c[k]
            End_Points[k,0] = ab[0,0]
            
            
            
        elif c_ass in ab[1:,0]:      
            
            func = np.empty(0)
            for i in j:
                func = np.append(func, perimeter(c[k], ab[i,0], base[1]) + E[c.tolist().index(ab[i-1,1])])
            E[k] = min(func)
            index_min = np.argmin(func)+j[0]
            
            Start_Points[k,:] = Start_Points[c.tolist().index(ab[index_min-1,1]),:]
            End_Points[k,:] = End_Points[c.tolist().index(ab[index_min-1,1]),:]
                                   
            Start_Points[k, np.argmax(Start_Points[k,:]<0)] = c[k]
            End_Points[k, np.argmax(End_Points[k,:]<0)] = ab[index_min,0]
    
        else:             
            func = np.empty(0)
            if (c_ass < ab[segment_number(c[k], ab),0]): 
                for i in j[1:]:
                    func = np.append(func, perimeter(c[k], ab[i,0], base[1]) + E[c.tolist().index(ab[i-1,1])])  
            else:
                func = [1000000.0]
            func2 = L + E[c.tolist().index(c_ass)]
            
            if (func2>min(func)):
                index_min = np.argmin(func)+j[0]+1
               
                Start_Points[k,:] = Start_Points[c.tolist().index(ab[index_min-1,1]),:]
                End_Points[k,:] = End_Points[c.tolist().index(ab[index_min-1,1]),:]
                End_Points[k,np.argmax(End_Points[k,:]<0)] = ab[index_min,0]
            else:
                Start_Points[k,:] = Start_Points[c.tolist().index(c_ass),:] 
                #check
                End_Points[k,:] = End_Points[c.tolist().index(c_ass),:] 
                End_Points[k,np.argmax(End_Points[k,:]<0)] = c_ass
                
            Start_Points[k,np.argmax(Start_Points[k,:]<0)] = c[k]                    
            E[k] = min(func2, min(func))
            
    Start_Points = Start_Points[c.size-1]
    End_Points = End_Points[c.size-1]
    return E[c.size-1], Start_Points[Start_Points>=0], End_Points[End_Points>=0]

def all_left_right_DP(c, c_first, ab, base, L):
    """
    Go through all the options and do one side DP removing the central segment
    """
    E = np.zeros(c_first.size)
    StartPoints = np.zeros((c_first.size,c.size))
    EndPoints = np.zeros((c_first.size,c.size))
    ab_i = ab.astype(np.float64)
    for i in range(0, c_first.size):
        if c_first[i] != ab_i[0,1]:
            ab_i[0,0] = c_first[i]
        else:
            ab_i = ab[ab[:,0]>c_first[i]].astype(np.float64)
        if (c[c>c_first[i]].size != 0):
            E[i],  Start_Points, End_Points = DP_one_side(c[c>c_first[i]], ab_i, base, L) 
            StartPoints[i,:Start_Points.size] = Start_Points
            EndPoints[i,:End_Points.size] = End_Points
            
        else: E[i] = 0
    return E, StartPoints, EndPoints

def join_tours(StartPoints, EndPoints):
    """
    Save right and left points of the tours together in one array
    """  
    Start = np.array([StartPoints[StartPoints>=0]])
    End = np.array([EndPoints[EndPoints>=0]])
    Tour = np.append(Start, End, axis = 0)
    idx = np.argwhere(np.all(Tour[..., :] == 0, axis=0))
    
    return np.delete(Tour, idx, axis=1)



def DP_both_sides(ab, base, L):
    """
    Full DP solution with all comparisons near the projection point
    """  
    
    ab_left, ab_right = separate_left_right(ab, base)
    
    c_right = np.sort(all_candidates(base, L, ab_right))
    c_left =  np.sort(all_candidates(base, L, ab_left))
    
    
    central_tours = find_central_tours(c_left, c_right , base, L)
    
    
    if not (central_tours.size == 0):  
        c_left_first = np.unique(np.sort(central_tours[:,0]))
        c_right_first = np.unique(np.sort(central_tours[:,1]))   
        
        
        E_left, StartPoints_left, EndPoints_left = all_left_right_DP(c_left, c_left_first, ab_left, base, L)
        E_right, StartPoints_right, EndPoints_right = all_left_right_DP(c_right, c_right_first, ab_right, base, L)
        
        
        left_central = np.append(c_left_first.reshape(E_left.shape[0],1), E_left.reshape(E_left.shape[0],1), axis=1)
        right_central = np.append(c_right_first.reshape(E_right.shape[0],1), E_right.reshape(E_right.shape[0],1), axis=1)
      
        
      
        totalL = np.zeros(central_tours.shape[0])
        for i in range (0, central_tours.shape[0]):
            a = tuple(np.argwhere(left_central == central_tours[i,0])[0])
            b = tuple(np.argwhere(right_central == central_tours[i,1])[0])
            totalL[i] = left_central[a[0],1] + right_central[b[0],1] + float(central_tours[i,2])
        
        c = tuple(np.argwhere(left_central == central_tours[np.argmin(totalL),0])[0])
        d = tuple(np.argwhere(right_central == central_tours[np.argmin(totalL),1])[0])
    else: 
        totalL = np.array([100000000])

    E_left_max, StartPoints_left_max, EndPoints_left_max = DP_one_side(c_left, ab_left, base, L)
    E_right_max, StartPoints_right_max, EndPoints_right_max = DP_one_side(c_right, ab_right, base, L)
    
    
    if (E_left_max + E_right_max) <= min(totalL):
        Tour_right = join_tours(StartPoints_right_max, EndPoints_right_max)
        Tour_right = Tour_right[ ::-1, :]
        Tour_left = -join_tours(StartPoints_left_max, EndPoints_left_max)


        Tour = np.append(np.flip(Tour_left,1), Tour_right, axis = 1)
        
    else:  
        Tour_right = join_tours(StartPoints_right[d[0]], EndPoints_right[d[0]])
        Tour_right = Tour_right[ ::-1, :]
        Tour_left = -join_tours(StartPoints_left[c[0]], EndPoints_left[c[0]])
        Tour_central = np.array([[-central_tours[np.argmin(totalL),0], central_tours[np.argmin(totalL),1] ]]).reshape((2, 1))
        
        Tour = np.append(np.flip(Tour_left,1), Tour_central, axis = 1)
        Tour = np.append(Tour, Tour_right, axis = 1)
        
    TotalLenght = min((E_left_max + E_right_max), min(totalL)) 
    
    return np.transpose(Tour), TotalLenght        

