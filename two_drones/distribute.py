# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 11:53:54 2024

@author: Alina Kasiuk
"""
import numpy as np
import math

def find_the_farthest(base,first,last):
    """
    Looking for the farthest point from the base
    """
    # distances to the base station
    fdist = math.sqrt(first**2+base[1]**2)
    ldist = math.sqrt(last**2+base[1]**2)

    # comparing the distances
    if fdist > ldist:
        farthest = first
        dist = fdist
    else:
        farthest = last
        dist = ldist
    
    return farthest, dist

def tour_lenght(tour, base):
    dist_left = math.sqrt(tour[0]**2+base[1]**2)
    dist_right = math.sqrt(tour[1]**2+base[1]**2)
    lenght = abs(tour[0]-tour[1]) + dist_left + dist_right
    return lenght

def to_the_min_disribution(Tour, base):
    Tour = np.transpose(Tour)
    Tour1 = np.empty(0)
    Tour2 = np.empty(0)
    M1 = 0
    M2 = 0
    while Tour.size>1:
        farthest, dist = find_the_farthest(base,Tour[0,0],Tour[Tour.shape[0]-1,1])
        if farthest == Tour[0,0]:
            if M1 < M2:
                Tour1 = np.append(Tour1, Tour[0])
                M1 += tour_lenght(Tour[0], base)
            else:
                Tour2 = np.append(Tour2, Tour[0])
                M2 += tour_lenght(Tour[0], base)
            Tour = Tour[1:]
        else:
            if M1 < M2:
                Tour1 = np.append(Tour1, Tour[Tour.shape[0]-1])
                M1 += tour_lenght(Tour[Tour.shape[0]-1], base)
            else:
                Tour2 = np.append(Tour2, Tour[Tour.shape[0]-1])
                M2 += tour_lenght(Tour[Tour.shape[0]-1], base)
            Tour = Tour[:Tour.shape[0]-1]
    Tour1 = Tour1.reshape(Tour1.shape[0]//2,2)
    Tour2 = Tour2.reshape(Tour2.shape[0]//2,2)
    if M1 > M2:
        Tour1, Tour2 = Tour2, Tour1
        M1, M2 = M2, M1

    print("T1 =", Tour1)
    print("T1 total length: M1 =", M1)
    print("T2 =",Tour2)
    print("T2 total length: M2 =", M2)   
    return Tour1, Tour2, M1, M2

def get_subTour1(Tour, Tour1, base, L):
    #TODO: Transpose Tour  
    T11 = np.empty(0)
    for tour in Tour1:
        if tour_lenght(tour, base)<L:
            T11 = np.append(T11, tour)
    T11 = T11.reshape(T11.shape[0]//2,2)

    T1_right = np.empty(0)
    T1_left = np.empty(0)
    
    for tour in T11:
        a = np.where(Tour == tour)[0][0]
        if a < Tour.shape[0]-1:
            if (tour_lenght(Tour[a+1], base) >= L) and (Tour[a,1] == Tour[a+1,0]):
                T1_right = np.append(T1_right, tour)
                
            if (tour_lenght(Tour[a-1], base) >= L) and (Tour[a,0] == Tour[a-1,0]):
                T1_left = np.append(T1_left, tour)
    
    return T1_right.reshape(T1_right.shape[0]//2,2),  T1_left.reshape(T1_left.shape[0]//2,2)

def get_subTour2(Tour2, base, l):    
    T2 = np.empty(0)
    for tour in Tour2:
        dist_left = math.sqrt(tour[0]**2+base[1]**2)
        dist_right = math.sqrt(tour[1]**2+base[1]**2)
        if (dist_left + dist_right)<l:
            T2 = np.append(T2, tour)
    return T2.reshape(T2.shape[0]//2,2)

def find_XR(tour, base,l):
    if abs(tour[1]) > abs(tour[0]):
        closest = abs(tour[0])
    else:
        closest = abs(tour[1])
    
    a = math.sqrt(closest**2+base[1]**2)
    x = (l-a*2)/2
    d = math.sqrt((closest+x)**2+base[1]**2)
    r = d - a - x
    return x, r

def find_XS(tour, base,l):
    if abs(tour[1]) > abs(tour[0]):
        farthest = abs(tour[1])
    else:
        farthest = abs(tour[0])  
    x = l/2
    c = math.sqrt(farthest**2+base[1]**2)
    d = math.sqrt((farthest+x)**2+base[1]**2)
    s = d - c - x
    return x, s

def cut_and_enlarge(Tour, base, L):
    # STEP 1: MinSum
    # STEP 2
    Tour = np.sort(Tour, axis = 0)
    # STEP 3
    Tour1, Tour2, M1, M2 = to_the_min_disribution(Tour, base)
    # STEP 4
    l = M2 - M1
    # STEP 5
    sub_Tour2 = get_subTour2(Tour2, base, l)
    # STEP 6
    sub_Tour1_right,  sub_Tour1_left = get_subTour1(Tour, Tour1, base, L)
    # STEP 7:
    xr = np.empty(0)
    r = np.empty(0)
    for tour in sub_Tour2:    
        x_k, r_k = find_XR(tour, base,l)
        xr = np.append(xr, x_k)
        r = np.append(r, r_k)
    
    # STEP 8
    xs = np.empty(0)
    s = np.empty(0)
    for tour in sub_Tour1_right:
        x_n, s_n = find_XS(tour, base,l)
        xs_right = np.append (xs,  x_n)
        s = np.append(s, s_n)
    
    for tour in sub_Tour1_left:
        x_n, s_n = find_XS(tour, base,l)
        xs_left = np.append (xs,  x_n)
        s = np.append(s, s_n)    
        
    
    # STEP 9
    if (s.size > 0) and (r.size > 0):
        minrs = min(np.min(r), np.min(s))
    else: 
        if r.size > 0:
            minrs = np.min(r)
        else:
            if s.size > 0:
                minrs = np.min(s)
            else:
                minrs = 0       
    
    # STEP 10
    # Cutting

    if r.size > 0:
        if minrs != 0:
            if minrs == np.min(r):
                for i in range(Tour2.shape[0]):
                    if Tour2[i,0] == sub_Tour2[sub_Tour2.shape[0]-1,0]:
                        ind=i
                if abs(Tour2[ind, 1]) < abs(Tour2[ind, 0]):
                    a = Tour2[ind, 1]
                    Tour2[ind, 1] = Tour2[ind, 1] - int(xr[sub_Tour2.shape[0]-1] )
                    newTour = np.array([Tour2[ind, 1], a])        
                else:
                    a = Tour2[ind, 0]
                    Tour2[ind, 0] = Tour2[ind, 0] + int(xr[sub_Tour2.shape[0]-1]) 
                    newTour = np.array([a, Tour2[ind, 0]])
                Tour1 = np.append(Tour1, newTour)
                
            if Tour1.shape[0]>1:
                Tour1 = Tour1.reshape(Tour1.shape[0]//2,2)  
    
    # STEP 11 #Check
    # Enlarge
    #if s.size > 0:
    #    if minrs != 0:
    #        if minrs == np.min(s):
    #            Tour1[0,1] = Tour1[0,1]+xs_right[0]
    #            Tour2[0,0] = Tour2[0,0]+xs_right[0]
                
            
                
    Tour1Lenght = 0
    Tour2Lenght = 0
    for tour in Tour1:
        Tour1Lenght += tour_lenght(tour, base)
    for tour in Tour2:
        Tour2Lenght += tour_lenght(tour, base)         
    
    return Tour1, Tour2, Tour1Lenght, Tour2Lenght
    
    
    
    