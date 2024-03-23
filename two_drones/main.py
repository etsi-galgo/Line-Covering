# -*- coding: utf-8 -*-
"""
Covering line segments with drones: the minmax criterion
Comparison of proposed G2D-algorithm and G2D-CutEnlarge-algorithm
with MILP formulation solving

Created on Tue Mar 19 12:29:06 2024

@author: Alina Kasiuk
"""
import numpy as np
import pandas as pd
import line_generation
import solver
import minsum
import datetime
import math
from sys import platform
import os
import distribute

def _create_dir_win32(name):
     directory="results\\{}\\".format(name)      
     return directory
 

def create_dir(name):
    "Creating the folders to save results"
    
    # Folder path define for different platforms. '\\', '/' issue
    if platform == "win32":
        directory = _create_dir_win32(name)
    else:
        print('unknown OS')
        
    if not os.path.exists(directory):
         os.makedirs(directory)
         
    return directory


if __name__ == "__main__":

    
    d_levels= 8
    length = [10**i for i in range(2,d_levels)] # The line length (total number of single points located on a line) 

    
    # Number of segments
    cases_per_level = 10
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
    

    df = pd.DataFrame(columns=['Experiment N', '1st segment start',  'last segment end',
                               'Base X', 'Base Y', 'Solver N Tours 1',
                               'Solver N Tours 2', 'Solver Tour Length 1',
                               'Solver Tour Length 2', 'Solver MinMax', 'DP N Tours', 'MinSum Length',
                               'Greedy N Tours 1', 'Greedy N Tours 2', 'Greedy Tour Length 1', 'Greedy Tour Length 2',
                               'Greedy MinMax', 'Greedy Error'])
    
    i=1
    today = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M")
    path = create_dir(today)
    j=1
    for bb in (base[20:30,:]):
        for num in n[0]:
            # Segment coordinates and the set of points A used for linear problem formulation
            xy, a = line_generation.generate(length[0], num, bb)
            minL = 2*math.sqrt((max(bb[0], length[0]-bb[0]))**2+bb[1]**2)+1
            maxL = math.sqrt(bb[0]**2+bb[1]**2)+math.sqrt((length[0]-bb[0])**2+bb[1]**2)+length[0]
            # Maximum tour length:
            L = np.random.randint(minL,maxL)
            
            
            print ("Case N:", i) 
            print ("___________________")
            print ("Base coordinates:", bb) 
            print ("Max Lenght:", L) 
            print ("___________________")
            print ("MinSum with DP result:")    
            if (xy[0,0]<0) and (xy[-1,1]>0):
                # MinSum with dynamic prgramming
                Tour, TotalLenght = minsum.DP_both_sides(xy, bb, L)
                
                # Greedy distribution
                Tour1, Tour2, M1, M2 = distribute.to_the_min_disribution(Tour, bb)
                
                # MILP solving with pulp
                print ("___________________")
                print ("MILP solver results:")
                NTour1 , Lenght1, NTour2 , Lenght2, Max_sum = solver.solver_results(num, a, xy, L, bb)
                df.loc[i] = {'Experiment N':i, '1st segment start':xy[0,0], 
                             'last segment end': xy[-1,1],
                             'Base X': bb[0], 'Base Y': bb[1], 
                             'Solver N Tours 1': NTour1,
                             'Solver N Tours 2': NTour2,
                             'Solver Tour Length 1': Lenght1,
                             'Solver Tour Length 2': Lenght2,
                             'Solver MinMax': Max_sum,
                             'DP N Tours': Tour.shape[1],
                             'MinSum Length': TotalLenght,
                             'Greedy N Tours 1': Tour1.shape[0],
                             'Greedy N Tours 2': Tour2.shape[0],
                             'Greedy Tour Length 1': M1,
                             'Greedy Tour Length 2': M2,
                             'Greedy MinMax': max(M1,M2),
                             'Greedy Error': (max(M1,M2) - Max_sum)/L,  
                             }
                i+=1
            else:
                print ("TODO:One side case")            
        df.to_csv (path+"expriment_base_"+str(bb[1])+".csv", sep=';', index = False, header=True)  
        j+=1
            
          
                  
        

                
            
                
                
            



    
