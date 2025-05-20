# -*- coding: utf-8 -*-
"""
MILP Formulation. Migration to Gurobi

Created on Tue Apr 30 14:42:18 2024

@author: Alina Kasiuk
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB
from utils import perimeter

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
    C = prepare_data(A, base)
    try:
        # Create a new model
        m = gp.Model("MinMax") 
        
        # Create variables
        # Variable T
        T = m.addVar(vtype = GRB.CONTINUOUS, lb = 0,  name="T")
    
        # Variable Z
        Z_1 = []
        Z_2 = [] 
        for i in range(A.size):
            z_i_1 = [m.addVar(vtype = GRB.BINARY,  name = f'z1_{i}_{j}') for j in range(i,A.size)]
            z_i_2 = [m.addVar(vtype = GRB.BINARY,  name = f'z2_{i}_{j}') for j in range(i,A.size)]
            Z_1.append(z_i_1)
            Z_2.append(z_i_2)
    
        # Variable S
        S_1 = [m.addVar(vtype = GRB.BINARY,  name = f's1_{q}_{q+1}') for q in range(A.size-1)] 
        S_2 = [m.addVar(vtype = GRB.BINARY,  name = f's2_{q}_{q+1}') for q in range(A.size-1)] 
    
        # Set objective
        m.setObjective(T, GRB.MINIMIZE)
    
        # Add the constraints
        # Min-max condition
        Tours_1 = []
        Tours_2 = []
        for i in range(A.size):
            for j in range(i, A.size):
                Tours_1.append(Z_1[i][j-i]*C[i,j])
                Tours_2.append(Z_2[i][j-i]*C[i,j])
                
        m.addConstr(sum(Tours_1) <= T, "minmax1") 
        m.addConstr(sum(Tours_2) <= T, "minmax2") 
    
        # Tour length limit
        for i in range(A.size):
            for j in range(i, A.size):
                m.addConstr(Z_1[i][j-i]*C[i,j] <= L, "length1")
                m.addConstr(Z_2[i][j-i]*C[i,j] <= L, "length2")

        # Segment covering condition
        finseg=np.zeros(A.size-1)
        for r in range(A.size-1):
            for i in range(n):
                if A[r]==xy[i,1]:
                    finseg[r]=1
            if finseg[r]==0:
                m.addConstr(S_1[r] + S_2[r]==1, "cover_all")        
    
        # Covering while making tours  
        for q in range(A.size-1):
            Owner_1_q = []
            Owner_2_q = []
            for i in range(A.size):
                for j in range(i+1, A.size):
                    if q>=i and q<j:
                        Owner_1_q.append(Z_1[i][j-i])
                        Owner_2_q.append(Z_2[i][j-i])
            m.addConstr(sum(Owner_1_q) == S_1[q], "cover1")
            m.addConstr(sum(Owner_2_q) == S_2[q], "cover2")
            
        # Optimize model
        m.optimize()

        # Return the results
        # Retrieve tours from Z_1 and Z_2
        Tour1 = []
        Tour2 = []
        for i in range(A.size):
            for j in range(i, A.size):
                if Z_1[i][j-i].X > 0.5:  # selected segment
                    Tour1.append((i, j))
                if Z_2[i][j-i].X > 0.5:
                    Tour2.append((i, j))

        # Return the results
        Max_sum = m.ObjVal
        Cover_1 = [s1.X for s1 in S_1]
        Cover_2 = [s2.X for s2 in S_2]
        
        return Max_sum, Cover_1, Cover_2, Tour1, Tour2     
    
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
    except AttributeError:
        print('Encountered an attribute error') 
    

def get_tours(A, cov_id, base):
    """
    Each drone tour details
    """
    T = np.empty(0)
    totalLenght = 0
    for i in range(cov_id.shape[0]):
        T = np.append(T, [A[cov_id[i,0]], A[cov_id[i,1]]])
        T = T.reshape(T.shape[0]//2,2)
        
        T_lenght = perimeter(A[cov_id[i,0]], A[cov_id[i,1]], base[1])
        totalLenght += T_lenght
        
    return T, cov_id.shape[0], totalLenght
    
    
def solver_results(n, A, xy, L, base):
    Max_sum, Cover_1, Cover_2, A_Tour1, A_Tour2 = minmax_problem(n, xy, A, L, base)
    
    Tour1, NTour1 , Lenght1 = get_tours(A, np.array(A_Tour1), base)
    
    Tour2, NTour2 , Lenght2 = get_tours(A, np.array(A_Tour2), base)
    return Tour1, Tour2, Lenght1, Lenght2, Max_sum