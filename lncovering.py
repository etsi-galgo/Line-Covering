# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:34:12 2023

@author: Alina
"""

import numpy as np
import random
import greedy
import dp

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
    return line, ones, ab


def main():
    lenght = 100 # line length
    m = 7 # number of segments
    base = np.array((50,50)) # base station coordinates
    
    # Generate a line to cover
    line, ones, ab = LineGenerate(lenght, m)
    L = 142
    
    total_cost = dp.BothSidesDynamics(ab, base, L)
    print(total_cost)
    
    #n, totalL = greedy.GreedyPP(base,line, ones,L)
    #print('Total number of tours:', n)
    #print('Total lenght:', totalL)


if __name__ == "__main__":
    main()