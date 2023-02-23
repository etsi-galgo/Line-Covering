# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:34:12 2023

@author: Alina
"""

import numpy as np
import random
import math

def LineGenerate(lenght, m):
    """
    Creating a line with m random segments
    """
    line = np.zeros(lenght,)
    # random start and end of the segments
    ab = np.array(sorted(random.sample(range(0, lenght-1), m*2))) 
    ab = ab.reshape((m,2)) # start and end of the segments coordinates
    # positive points coordinates
    ones = np.arange(ab[0,0],ab[0,1])
    for i in range(1,m):
        ones = np.concatenate((ones, np.arange(ab[i,0],ab[i,1])))
    line[ones] = 1  # put the generated segments on the line
    return line, ones

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
        print('The first point of the first segment is the farthest')
    else:
        farthest = last
        dist = ldist
        print('The last point of the last segment is the farthest')
    
    return farthest, dist

def main():
    lenght = 100 # line length
    m = 7 # number of segments
    base = np.array((50,50)) # base station coordinates
    
    # Generate a line to cover
    line, ones = LineGenerate(lenght, m)
    
    covered = False
    first = ones[0] # the first point of the first segment
    last = ones[ones.size-1] # the last point of the last segment
    L = 142 # maximum tour length
    farthest, far_dist = FindTheFarthest(base,ones,first,last)
    if (L < far_dist*2):
        print ("we can not achieve the farthest point")
    else:
        n = 0
        totalL = 0
        print(ones)
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
                line[0:(int(x))] = 0
                if (x >= ones[ones.size-1]): 
                    ones = np.zeros(0)
                else:
                    ones = ones[np.argmax(ones>x):]
            if (farthest == last):
                x = xA+base[0]+1
                line[(int(x)):line.shape[0]] = 0
                ones = ones[:(np.argmax(ones>x))]
            if (ones.size == 0): covered = True
            n += 1
            totalL += L
            print('The farthest point:', farthest)
            print('The greedy point:', x)   
            print(ones)
            print(b)
            print('Total number of tours:', n)
            print('Total lenght:', totalL)  

if __name__ == "__main__":
    main()