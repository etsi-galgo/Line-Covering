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
import solver_gurobi
import minsum
import datetime
from sys import platform
import os
import distribute
from utils import max_tour, tour_lenght
import time


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

def print_results(d, xy, base, L, Tour, TotalLenght, Tour1, Tour2, M1, M2,
                  Tour1_ce, Tour2_ce, M1_ce, M2_ce, Tour1_solv, Tour2_solv,
                  M1_solv, M2_solv, Max_sum):
    print ("Experiment N:", exp) 
    print ("___________________")
    print ("Number of points on the line (discretization):", d) 
    print ("Base coordinates:", base) 
    print ("Max Lenght:", L)                     
    print ("___________________")
    print ("MinSum with DP result:") 
    for i in range(Tour.shape[0]):
        print('Tour', i+1, 'start:', Tour[i,0])
        print('Tour', i+1, 'end:', Tour[i,1])
        print('Tour', i+1, 'length:', tour_lenght(Tour[i], base[1]))
        
    print('Total number of tours:', Tour.shape[0])                    
    print('Total length:', TotalLenght)
    
    print ("___________________")
    print (" Greedy results:")
    
    print("T1 =", Tour1)
    print("T1 total length: l1 =", M1)
    print("T2 =",Tour2)
    print("T2 total length: l2 =", M2)                  
    
    print ("___________________")
    print ("Cutting and enlarging results:")
   
    print("T1 =", Tour1_ce)
    print("T1 total length: l1 =", M1_ce)
    print("T2 =",Tour2_ce)
    print("T2 total length: l2 =", M2_ce)  
    
    print ("___________________")
    print ("MILP solver results:")
    print("T1 =", Tour1_solv)
    print("T1 total length: l1 =", M1_solv)
    print("T2 =",Tour2_solv)
    print("T2 total length: l2 =", M2_solv)  
    

if __name__ == "__main__":
    
    df = pd.DataFrame(columns=['Discretization', 'Experiment N',
                               'Number of segments',
                               '1st segment start',  'last segment end',
                               'Base X', 'Base Y', 'Max Lenght',
                               'Solver N Tours 1','Solver N Tours 2',
                               'Solver Tour Length 1', 'Solver Tour Length 2',
                               'Solver MinMax',
                               'DP N Tours', 'MinSum Length',
                               'Greedy N Tours 1', 'Greedy N Tours 2',
                               'Greedy Tour Length 1', 'Greedy Tour Length 2',
                               'Greedy MinMax', 'Greedy Error',
                               'Cut/Enlarge N Tours 1', 'Cut/Enlarge N Tours 2',
                               'Cut/Enlarge Tour Length 1', 'Cut/Enlarge Tour Length 2',
                               'Cut/Enlarge MinMax', 'Cut/Enlarge Error'])
       
    
    today = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M")
    path = create_dir(today)

    
    exp_N = 1 # Number of experiments
    
    d = 100 # Discretization level
    
    for exp in range(exp_N): # Make exp_N experiments
        tic = time.perf_counter()
        n = np.random.randint(1,10) # Get number of segments randomly
        X = np.random.randint(0,d) # Get base coordinate on X axis randomly
        Y = np.random.randint(1,10*d) # Get base coordinate on X axis randomly
        base = np.array((X,d*Y)) # Base coordinates proportioned
        L = max_tour(d,base) #Get maximum tour length randomly
        
        
        # Generate a random line of segments
        # Output the segments coordinates and the set of points A used for linear problem formulation
        xy, a = line_generation.generate(d, n, base)
        
   
        if (xy[0,0]<0) and (xy[-1,1]>0):
            # MinSum with dynamic programming
            Tour, TotalLenght = minsum.DP_both_sides(xy, base, L)
            # Greedy distribution
            Tour1, Tour2, M1, M2 = distribute.to_the_min_disribution(Tour, base[1])
            # Cutting and enlarging
            Tour1_ce, Tour2_ce, M1_ce, M2_ce = distribute.cut_and_enlarge(Tour, base, L)
            # MILP solving with pulp
            tic_solver = time.perf_counter()
            Tour1_solv, Tour2_solv, M1_solv, M2_solv, Max_sum = solver_gurobi.solver_results(n, a, xy, L, base)
            toc_solver = time.perf_counter()
            
            print_results(d, xy, base, L, Tour, TotalLenght, Tour1, Tour2, M1, M2,
                              Tour1_ce, Tour2_ce, M1_ce, M2_ce, Tour1_solv, Tour2_solv,
                              M1_solv, M2_solv, Max_sum)

            df.loc[exp] = {'Discretization':d, 'Experiment N':exp,
                         'Number of segments': n,
                         '1st segment start':xy[0,0], 'last segment end': xy[-1,1],
                         'Base X': base[0], 'Base Y': base[1], 'Max Lenght':L,
                         'Solver N Tours 1': Tour1_solv.shape[0],
                         'Solver N Tours 2': Tour2_solv.shape[0],
                         'Solver Tour Length 1': M1_solv,
                         'Solver Tour Length 2': M2_solv,
                         'Solver MinMax': Max_sum,
                         'DP N Tours': Tour.shape[1],
                         'MinSum Length': TotalLenght,
                         'Greedy N Tours 1': Tour1.shape[0],
                         'Greedy N Tours 2': Tour2.shape[0],
                         'Greedy Tour Length 1': M1,
                         'Greedy Tour Length 2': M2,
                         'Greedy MinMax': max(M1,M2),
                         'Greedy Error': (max(M1,M2) - Max_sum)/L,                              
                         'Cut/Enlarge N Tours 1': Tour1_ce.shape[0],
                         'Cut/Enlarge N Tours 2': Tour2_ce.shape[0],
                         'Cut/Enlarge Tour Length 1': M1_ce,
                         'Cut/Enlarge Tour Length 2': M2_ce,
                         'Cut/Enlarge MinMax': max(M1_ce,M2_ce),
                         'Cut/Enlarge Error': (max(M1_ce,M2_ce) - Max_sum)/L,
                         }
        else:
            print ("TODO:One side case")   
        toc = time.perf_counter()
        solver_dur = toc_solver - tic_solver 
        total_dur = toc - tic
        print("Experiment duration:", total_dur)
        print("Solver duration:", solver_dur)
        
    df.to_csv (path+"experiment_"+str(d)+"points_"+str(base[1])+"height.csv", sep=';', index = False, header=True) 
            
        
      
                  
        

                
            
                
                
            



    
