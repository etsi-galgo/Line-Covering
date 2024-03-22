# -*- coding: utf-8 -*-
"""
Covering line segments with drones: the minmax criterion
Comparison of proposed G2D-algorithm and G2D-CutEnlarge-algorithm
with MILP formulation solving

Created on Tue Mar 19 12:29:06 2024

@author: Alina Kasiuk
"""
import numpy as np
import line_generation
import solver
import minsum
import time
import math


if __name__ == "__main__":

    
    d_levels= 8
    length = [10**i for i in range(2,d_levels)] # The line length (total number of single points located on a line) 

    
    # Number of segments
    cases_per_level = 100
    n = np.empty((d_levels-2,cases_per_level)) 
    i=0
    for l in length:
        n[i]=np.random.randint(1,l/2, size=(cases_per_level))
        i+=1
        
    n = n.astype('int')

    
    # Base station coordinates
    
    
    Y_base = [length[0]*2**i for i in range(-2,4)]
    
    X_cases = 10
    i=0
    base = np.empty((360,2)) 
    j=0
    for l in length:
        for Y in Y_base:
            X_base=np.random.randint(0,l, size=(X_cases))
  
            for i in range(X_cases):
                base[i+j,0] = X_base[i]
                base[i+j,1] = Y
                
            j+=X_cases
    


    
    # Segment coordinates and the set of points A used for linear problem formulation
    i=1
    for num in n[0]:
        for bb in (base[:50,:]):
            xy, a = line_generation.generate(length[0], num, bb)
            minL = 2*math.sqrt((max(bb[0], length[0]-bb[0]))**2+bb[1]**2)+1
            maxL = math.sqrt(bb[0]**2+bb[1]**2)+math.sqrt((length[0]-bb[0])**2+bb[1]**2)+length[0]
            # Maximum tour length:
            L = np.random.randint(minL,maxL)
            
            # MinSum with dynamic prgramming
            print ("Case N:", i) 
            print ("___________________")
            print ("Base coordinates:", bb) 
            print ("Max Lenght:", L) 
            print ("___________________")
            print ("MinSum with DP result:")    
            if (xy[0,0]<0) and (xy[-1,1]>0):
                Tour, TotalLenght = minsum.DP_both_sides(xy, bb, L)
                i+=1
            else:
                print ("TODO:One side case")
                
        
            # MILP solving with pulp
            print ("___________________")
            print ("MILP solver results:")
                
            solver.solver_results(num, a, xy, L, bb)
                
            
                
                
            



    
