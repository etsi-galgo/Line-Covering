# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:34:12 2023

@author: Alina
"""

import numpy as np
import math

def FindTheFarthest(base,ones,first,last):
    """
    Looking for the farthest point from the base
    """
    # distances to the base station
    fdist = math.sqrt((first-base[0])**2+base[1]**2)
    ldist = math.sqrt((last-base[0])**2+base[1]**2)

    # comparing the distances
    if fdist > ldist:
        farthest = first
        dist = fdist
    else:
        farthest = last
        dist = ldist
    
    return farthest, dist



def Greedy(base,line,ones,L):
    covered = False
    first = ones[0] # the first point of the first segment
    last = ones[ones.size-1] # the last point of the last segment
    L = 142 # maximum tour length
    farthest, far_dist = FindTheFarthest(base,ones,first,last)
    if (L < far_dist*2):
        print ("we can not achieve the farthest point")
        return 0, 0
    else:
        n = 0
        totalL = 0
        while not covered:
            first = ones[0] # the first point of the first segment
            last = ones[ones.size-1] # the last point of the last segment
            farthest, far_dist = FindTheFarthest(base,ones,first,last)
            # the farthest point coordinate
            xB = abs(farthest-base[0])
            # distance from the farthest point to the base
            b = far_dist
            # distance from the farthest point to greedy
            c = (L**2-2*L*b)/(2*(L-b-xB))
            # greedy point coordinate
            xA = xB-c
            if (farthest == first):
                x = -xA+base[0]
                #line[0:(int(x))] = 0
                if (x >= ones[ones.size-1]): 
                    ones = np.zeros(0)
                else:
                    ones = ones[np.argmax(ones>x):]
            if (farthest == last):
                x = xA+base[0]+1
                #line[(int(x)):line.shape[0]] = 0
                ones = ones[:(np.argmax(ones>x))]
            if (ones.size == 0): covered = True
            n += 1
            totalL += L
            print('Tour', n ,'start:', farthest)
            print('Tour', n ,' end:',  ones[:(np.argmax(ones>x))]) 
        return n, totalL

def GreedySE(base,line, ones,L):
    covered = False
    first = ones[0] # the first point of the first segment
    last = ones[ones.size-1] # the last point of the last segment
    L = 142 # maximum tour length
    farthest, far_dist = FindTheFarthest(base,ones,first,last)
    if (L < far_dist*2):
        print ("we can not achieve the farthest point")
        return 0, 0
    else:
        n = 0
        totalL = 0
        print(ones)
        first = ones[0] # the first point of the first segment
        last = ones[ones.size-1] # the last point of the last segment
        while not covered:
            farthest, far_dist = FindTheFarthest(base,ones,first,last)
            # the farthest point coordinate
            xB = abs(farthest-base[0])
            # distance from the farthest point to the base
            b = far_dist
            # distance from the farthest point to greedy
            c = (L**2-2*L*b)/(2*(L-b-xB))
            # greedy point coordinate
            xA = xB-c
            if (farthest == first):
                x = -xA+base[0]
                xNew = ones[np.argmax(ones>x)-1]
                
                #line[0:(int(x))] = 0
                if (x >= ones[ones.size-1]): 
                    ones = np.zeros(0)
                else:
                    ones = ones[np.argmax(ones>x):]
                                
                if (line[xNew+1] == 1):
                    xNew = x
                    first = x
                else:
                    if (ones.size > 0): first = ones[0]
                lineL = xNew-farthest
                a = math.sqrt((xNew-base[0])**2+base[1]**2)
                
            if (farthest == last):
                x = xA+base[0]+1
                xNew = ones[np.argmax(ones>x)]
                #line[(int(x)):line.shape[0]] = 0
                ones = ones[:(np.argmax(ones>x))] 
                
                if (line[xNew-1] == 1):
                    xNew = x
                    last = x
                else:
                    if (ones.size > 0): last = ones[ones.size-1]
                lineL = farthest - xNew
                a = math.sqrt((xNew-base[0])**2+base[1]**2)

            if (ones.size == 0): covered = True
            n += 1
            totalL += (lineL + a + b) 
            
            print('Tour', n ,'start:', farthest)
            print('Tour', n ,' end:', xNew) 
        return n, totalL
    
    
def GreedyPP(base,line, ones,L):
    covered = False
    left = ones[0] # the leftmost point of the first segment
    right = ones[ones.size-1]# the rightmost point of the last segment
    farthest, far_dist = FindTheFarthest(base,ones,left,right) # the farthest point from the base
    if (L < far_dist*2):
        print ("we can not achieve the farthest point")
    else:
        n = 0 # number of tours
        totalL = 0 # total length
        print(ones)
        while not covered:
            farthest, far_dist = FindTheFarthest(base,ones,left,right)
            # the farthest point coordinate
            xB = abs(farthest-base[0])
            # distance from the farthest point to the base
            b = far_dist
            # distance from the farthest point to greedy
            c = (L**2-2*L*b)/(2*(L-b-xB))
            # greedy point coordinate
            xA = xB-c
            
            if (farthest == left):
                gp = -xA+base[0] # greedy point num in ones array
                lpc = ones[np.argmax(ones>gp)-1] # last point covered
                
                # cutting ones until the greedy point
                if (gp >= ones[ones.size-1]): 
                    ones = np.zeros(0)
                else:
                    ones = ones[np.argmax(ones>=gp):]
                    
                if (ones.size == 0): 
                    x = right
                else:                        
                    if gp > base[0]: # if achvieve the projection point
                        x = ones[np.argmax(ones>=base[0])-1] # last point covered 
                        left = x # finish the tour
                        # cutting ones until the p.p.
                        if (x >= ones[ones.size-1]): 
                            ones = np.zeros(0)
                        else:
                            ones = ones[np.argmax(ones>x):]  
                        
                        
                    else:                            
                        if (line[lpc+1] == 1): # if the greedy point is inside the segment
                            x = gp # finish the tour on greedy
                            left = gp # cut the line on greedy
                        else:
                            x = lpc
                            left = ones[0] # cut the line on the next segment             
                        
                
            if (farthest == right):
                gp = xA+base[0]
                lpc = ones[np.argmax(ones>gp)]
                ones = ones[:(np.argmax(ones>=gp))]  
                 
                
                if (ones.size == 0):
                    x = left
                else:
                    if gp < base[0]: # if achvieve the projection point
                        x = ones[np.argmax(ones>=base[0])]
                        right = x
                        ones = ones[:(np.argmax(ones>=x))] 
                    else:                      
                        if (line[lpc-1] == 1):
                            x = gp
                            right = gp
                        else:
                            x = lpc
                            right = ones[ones.size-1]
                
                        
            
            lineL = abs(farthest - x) # length of the line covered
            a = math.sqrt((x-base[0])**2+base[1]**2) # distance to the base

            if (ones.size == 0): covered = True
            n += 1
            totalL += (lineL + a + b)

        return n, totalL
        