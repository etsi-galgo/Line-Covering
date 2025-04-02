# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:29:33 2024

@author: Alina
"""
import math
import numpy as np


def perimeter(point1, point2, y_base):
    """
    Find a triangle perimeter given three points
    """    
    return max(point1, point2) - min(point1, point2) + math.sqrt(point1**2+y_base**2) + math.sqrt(point2**2+y_base**2)

def distance(point, y_base):
    """
    Distances to the base station
    """
    dist = math.sqrt(point**2+y_base**2)
    return dist 

def tour_lenght(tour, y_base):
    """
    The lenght of a single tour
    """    
    dist_left = distance(tour[0],y_base)
    dist_right = distance(tour[1],y_base)
    length = tour[1]-tour[0] + dist_left + dist_right
    return length

def total_lenght(t_set, y_base):
    """
    The lenght of a set of tours
    """ 
    total_l=0
    for t in t_set:
        total_l += tour_lenght(t, y_base)
    return total_l  

def big_bro(t):
    """
    Find a tour tour just one point bigger than a given
    """
    if (t[0]>0) and (t[1]>0): 
        return [t[0]-1, t[1]]
    if (t[0]<0) and (t[1]<0): 
        return [t[0], t[1]+1]
    if (t[0]<0) and (t[1]>0): 
        if abs(t[0])>abs(t[1]):
            return [t[0], t[1]+1]
        else:
            return [t[0]-1, t[1]]
        
def max_tour(l,base):
    """
    Get maximum tour length randomly such as it is always possible to achieve
    a segment and it is not bigger that one which covers the whole line
    """  
    minL = 2*math.sqrt((max(base[0], l-base[0]))**2+base[1]**2)+1
    maxL = math.sqrt(base[0]**2+base[1]**2)+math.sqrt((l-base[0])**2+base[1]**2)+l
    return np.random.randint(minL,minL+(maxL-minL)/3)

