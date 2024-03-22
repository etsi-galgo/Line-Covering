# -*- coding: utf-8 -*-
"""
MILP Formulation

Created on Tue Mar 19 12:44:42 2024

@author: Alina Kasiuk
"""

import numpy as np
import math
import pulp

def prepare_data(a, base):
    # The set Beta of distances from the base station to all points in A:
    beta = np.sqrt(a**2+base[1]**2) 
    
    # The set C of all possible tour lengths:
    c=np.zeros((a.size, a.size))
    for i in range(a.size):
        for j in range(i, a.size):
            c[i,j]=beta[i]+beta[j]+a[j]-a[i]
    return c


def minmax_problem(n, xy, A, L, base):
    
    # Create a problem -- indicate that we will minimize the objectives
    prob = pulp.LpProblem('Line Covering MinMax', pulp.LpMinimize)

    # Add decision variables
    
    C = prepare_data(A, base)
    # Variable T
    T = pulp.LpVariable('T', lowBound = 0)

    # Variable Z
    Z_1 = []
    Z_2 = []
    for i in range(A.size):
        z_i_1 = [pulp.LpVariable(f'z1_{i}_{j}', cat ='Binary') for j in range(i,A.size)]
        z_i_2 = [pulp.LpVariable(f'z2_{i}_{j}', cat ='Binary') for j in range(i,A.size)]
        Z_1.append(z_i_1)
        Z_2.append(z_i_2)

    # Variable S
    S_1 = [pulp.LpVariable(f's1_{q}_{q+1}', cat ='Binary') for q in range(A.size-1)] 
    S_2 = [pulp.LpVariable(f's2_{q}_{q+1}', cat ='Binary') for q in range(A.size-1)] 

    # Set the objective
    prob += T

    # Add the constraints
    # Min-max condition    
    Tours_1 = []
    Tours_2 = []
    for i in range(A.size):
        for j in range(i, A.size):
            Tours_1.append(Z_1[i][j-i]*C[i,j])
            Tours_2.append(Z_2[i][j-i]*C[i,j])
    prob += pulp.lpSum(Tours_1) <= T
    prob += pulp.lpSum(Tours_2) <= T    


    # Tour length limit
    for i in range(A.size):
        for j in range(i, A.size):
            prob += Z_1[i][j-i]*C[i,j] <= L
            prob += Z_2[i][j-i]*C[i,j] <= L

    # Segment covering condition
    finseg=np.zeros(A.size-1)
    for r in range(A.size-1):
        for i in range(n):
            if A[r]==xy[i,1]:
                finseg[r]=1
        if finseg[r]==0:
            prob += S_1[r] + S_2[r]==1

    # Covering while making tours  
    for q in range(A.size-1):
        Owner_1_q = []
        Owner_2_q = []
        for i in range(A.size):
            for j in range(i+1, A.size):
                if q>=i and q<j:
                    Owner_1_q.append(Z_1[i][j-i])
                    Owner_2_q.append(Z_2[i][j-i])
        prob += pulp.lpSum(Owner_1_q) == S_1[q]
        prob += pulp.lpSum(Owner_2_q) == S_2[q]

    # Solving the Problem
    pulp.LpSolverDefault.msg = 1
    status = prob.solve()

    if status == pulp.constants.LpStatusInfeasible:
        print('Problem is infeasible')
    elif status == pulp.constants.LpStatusUnbounded:
        print('Problem is unbounded. Cannot proceed')
    else:
        assert status == pulp.constants.LpStatusOptimal, 'Something went wrong while solving since status is either undefined or unsolved'
        # extract values
        print('Success: optimal answer found')

        # Return the result
        Max_sum = T.varValue
        Cover_1 = [s1.varValue for s1 in S_1]
        Cover_2 = [s2.varValue for s2 in S_2]
            
        return Max_sum, Cover_1, Cover_2
    
def get_tour_index(cov):
    """
    Getting the indexes of each tour from the covering variable S of MIPL
    """
    p = []
    q = []
    if cov[0]==1:
        p.append(0)
    for i in range(len(cov)-1):
        if cov[i]==0 and cov[i+1]==1:
            p.append(i+1)
        if cov[i]==1 and cov[i+1]==0:
            q.append(i+1)    
    if cov[len(cov)-1]==1:
        q.append(len(cov))
    T = np.transpose(np.array([p,q]))
    return T

def perimeter(point1, point2, base):
    return max(point1, point2) - min(point1, point2) + math.sqrt(point1**2+base[1]**2) + math.sqrt(point2**2+base[1]**2)

def get_tours(A, cov_id, base):
    """
    Printing the trajectory details for each drone
    """
    
    totalLenght = 0
    for i in range(cov_id.shape[0]):
        print('Tour', i+1, 'start:', A[cov_id[i,0]])
        print('Tour', i+1, 'end:', A[cov_id[i,1]])
        T_lenght = perimeter(A[cov_id[i,0]], A[cov_id[i,1]], base)
        print('Tour', i+1, 'lenght:', T_lenght)
        totalLenght += T_lenght

    print('Total number of tours:', cov_id.shape[0])
    print('Total lenght:', totalLenght)
    
    
def solver_results(n, A, xy, L, base):
    Max_sum, Cover_1, Cover_2 = minmax_problem(n, xy, A, L, base)
    
    print("the Max trajectory lenght:", Max_sum)
    
    print ("Drone 1 trajectory:")
    drone_1 = get_tour_index(Cover_1)
    get_tours(A, drone_1, base)
    
    print ("___________________")
    print ("Drone 2 trajectory:")
    drone_2 = get_tour_index(Cover_2)
    get_tours(A, drone_2, base)
    