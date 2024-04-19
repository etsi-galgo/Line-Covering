# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 11:53:54 2024

@author: Alina Kasiuk
"""
import numpy as np
from utils import distance, tour_lenght, total_lenght, big_bro
 

def to_the_min_disribution(Tour, y_base):
    m = Tour.shape[0]-1
    
    Tour1 = np.empty(0)
    Tour2 = np.empty(0)
    l1 = 0
    l2 = 0
    
    while Tour.size>1:
        #Find the farthest tour from the base:
        if distance(Tour[0,0], y_base) >= distance(Tour[m,1],y_base):
            farthest_tour = Tour[0]
            Tour = Tour[1:]
        else:
            farthest_tour = Tour[m]
            Tour = Tour[:m]
        m -= 1
        
        #Add the farthest tour to the smallest set
        if l1 < l2:
            Tour1 = np.append(Tour1, farthest_tour)
            l1 += tour_lenght(farthest_tour, y_base)
        else:
            Tour2 = np.append(Tour2, farthest_tour)
            l2 += tour_lenght(farthest_tour, y_base)
        
    Tour1 = Tour1.reshape(Tour1.shape[0]//2,2)
    Tour2 = Tour2.reshape(Tour2.shape[0]//2,2)

    # Make Tour2 always be the biggest
    if l1 > l2:
        Tour1, Tour2 = Tour2, Tour1
        l1, l2 = l2, l1 
    return Tour1, Tour2, l1, l2    


def candidates_to_cut(T2 ,l, y_base):
    T_cut = np.empty(0)
    for t2 in T2:
        if (distance(t2[1], y_base) + distance(t2[0], y_base))<l:
            T_cut = np.append(T_cut, t2)
            T_cut = T_cut.reshape(T_cut.shape[0]//2,2)
    return T_cut
        
def candidates_to_enlarge(T1, T2, L, y_base):
    T_en_left = np.empty(0)
    T_en_right = np.empty(0)
    for t1 in T1:
        for t2 in T2:
            if (t1[0]<0) and (t1[0]==t2[1]) and (tour_lenght(big_bro(t2), y_base)>L) and (tour_lenght(big_bro(t1), y_base)<L):
                T_en_left = np.append(T_en_left, t1)
                T_en_left = T_en_left.reshape(T_en_left.shape[0]//2,2)
            if (t1[1]>0) and (t1[1]==t2[0]) and (tour_lenght(big_bro(t2), y_base)>L) and (tour_lenght(big_bro(t1), y_base)<L):
                T_en_right = np.append(T_en_right, t1)
                T_en_right = T_en_right.reshape(T_en_right.shape[0]//2,2)
                
    return T_en_left, T_en_right

def cutting_improvement(t, l, y_base):
    c = distance(t[0], y_base)
    f = distance(t[1], y_base)
    s = t[1]-t[0]

    #Option 1: Left tour for T1
    x1 = (l-c*2)/2
    d1 = distance(t[0]+x1, y_base)
    r1 = d1 - c - x1

    #Option 2: Left tour for T2
    x2 = (s*2+f*2-l)/2
    d2 = distance(t[0]+x2, y_base)
    r2 = d2 - s - f + x2

    if r2<r1:
        return x2,r2,2
    else:
        return x1,r1,1

def enlarging_improvement(farthest, closest, l, L, y_base):
    x = l/2
    f = distance(farthest, y_base)
    d = distance(farthest+x, y_base)
    c = distance(closest, y_base)
    
    if (farthest+x-closest+c+d > L):
        dist = 0.5*(L**2-2*L*c)/(closest+L-c)
        x=dist+closest-farthest
        d = distance(farthest+x, y_base)
    s = d-f-x
    
    return x,s

def cutting(T1, T2, win_tour, x):
    #Option 1: Left tour for T1
    for t2 in T2:
        if t2[0] == win_tour[0]:
            start = t2[0]
            t2[0] = t2[0]+np.round(x)
            T1 = np.append(T1, [start, t2[0]])
            T1 = T1.reshape(T1.shape[0]//2,2)
    return T1, T2

def reversed_cutting(T1, T2, win_tour, x):
    #Option 2: Left tour for T2
    for t2 in T2:
        if t2[0] == win_tour[0]:
            end = t2[1]
            t2[1] = t2[0]+np.round(x)
            T1 = np.append(T1, [t2[1], end])
            T1 = T1.reshape(T1.shape[0]//2,2) 
    return T1, T2

def remove_enlarged(t, T):
    for i in range(T.shape[0]):
        if (T[i,0]==t[0]) or (T[i,1]==t[1]):
            T = np.delete(T,i,0)
    return T

def enlarging_right(T1, T2, T_enlarge_right, win_tour, x):
    for t1 in T1:
        for t2 in T2:
            if (t1[0] == win_tour[0]) and (t1[1]==t2[0]):
                t1[1] = t1[1]+np.floor(x)
                t2[0] = t2[0]+np.floor(x)
                
                # Remove t1 from the set T_enlarge_right
                T_enlarge_right = remove_enlarged(t1, T_enlarge_right)
                
    return T1, T2, T_enlarge_right

def enlarging_left(T1, T2, T_enlarge_left, win_tour, x):
    for t1 in T1:
        for t2 in T2:
            if (t1[0] == win_tour[0]) and (t1[0]==t2[1]):
                t1[0] = t1[0]-np.floor(x)
                t2[1] = t2[1]-np.floor(x)
                
                # Remove t1 from the set T_enlarge_left
                T_enlarge_left = remove_enlarged(t1, T_enlarge_left)
    return T1, T2, T_enlarge_left   

def candidates_table(T_cut, T_enlarge_right, T_enlarge_left, l, L, y_base):
    Table = np.empty(0)
    # Find the improvement after each possible cutting
    for t in T_cut:
        x_cut, d_cut, idx = cutting_improvement(t,l, y_base)
        Table = np.append(Table, np.array([t[0],t[1], x_cut, d_cut, idx]))
    
    # Find the improvement after each possible enlarging
    if T_enlarge_left.size>0:
        for t in T_enlarge_right:
            farthest = abs(t[1])
            closest = abs(t[0])
            x_enlarge_right, d_enlarge_right  = enlarging_improvement(farthest, closest,l, L, y_base)
            Table = np.append(Table, np.array([t[0],t[1], x_enlarge_right, d_enlarge_right, 3]))
        
    if T_enlarge_left.size>0:
        for t in T_enlarge_left:
            farthest = abs(t[0])
            closest = abs(t[1])
            x_enlarge_left, d_enlarge_left  = enlarging_improvement(farthest, closest,l,L, y_base)
            Table = np.append(Table, np.array([t[0],t[1], x_enlarge_left, d_enlarge_left, 4]))
    Table = Table.reshape(Table.shape[0]//5,5)
    return Table


def cut_and_enlarge(Tour, base, L):
    
    # Step 2: Distribute T between two sets T1  y T2  such as l(T2)>l(T1)
    Tour1, Tour2, l1, l2 = to_the_min_disribution(Tour, base[1]) 
    
    # Step 3: Get the sets of candidates to enlarge:
    T_enlarge_left, T_enlarge_right = candidates_to_enlarge(Tour1, Tour2, L, base[1])
    
    # Step 4: Improve until l(T2)=l(T1)
    l= l2-l1
    while l>0:
        # Get the set of candidates to cut:
        T_cut = candidates_to_cut(Tour2, l, base[1])
                
        # Find the table of candidates to improve
        # | t(0) | t(1) | x | d | type |
        Table = candidates_table(T_cut, T_enlarge_right, T_enlarge_left, l, L, base[1])   
        # Finish if no candidates are found
        if Table.size == 0:
            break
    
        # Find a candidate that gives the best improvement
        for tab in Table:
            if tab[3]==min(Table[:,3]):
                winner = tab
        win_tour = np.transpose([winner[0],winner[1]])
        
        # Apply cutting
        if winner[4]==1:
            Tour1, Tour2 = cutting(Tour1, Tour2, win_tour, winner[2])
        if winner[4]==2:
            Tour1, Tour2 = reversed_cutting(Tour1, Tour2, win_tour, winner[2])  
    
        # Apply enlarging
        if winner[4]==3:
            Tour1, Tour2, T_enlarge_right = enlarging_right(Tour1, Tour2, T_enlarge_right, win_tour, winner[2])       
        if winner[4]==4:
            Tour1, Tour2, T_enlarge_left = enlarging_left(Tour1, Tour2, T_enlarge_left, win_tour, winner[2]) 
                    
        l1 = total_lenght(Tour1, base[1])
        l2 = total_lenght(Tour2, base[1])
        l= l2-l1
    
    return Tour1, Tour2, l1, l2
    
    
    
    