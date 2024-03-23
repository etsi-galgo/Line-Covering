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
