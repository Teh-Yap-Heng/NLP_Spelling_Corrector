# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:26:19 2020

@author: USER
"""
import numpy as np
def delete_letter(word, verbose=False):
    '''return list of word with deleted letter
    '''
    
    delete_l = []
    split_l = []
    
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    delete_l = [L+R[1:] for L,R in split_l if R]

    if verbose: print(f"input word {word}, \ndelete_l = {delete_l}")

    return delete_l

def transpose_letter(word, verbose=False):
    '''
    return list of words with transposed letter
    ''' 
    
    transpose_l = []
    split_l = []

    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    transpose_l = [L + R[1] + R[0] + R[2:] for L,R in split_l if len(R)>1]
    
    if verbose: print(f"Input word = {word} \ntranspose_l = {transpose_l}") 

    return transpose_l

def subst_letter(word, verbose=False):
    '''
    return list of substitute letter
    ''' 
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    subst_l = []
    split_l = []

    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    subst_l = [L + l + R[1:] for L,R in split_l if R for l in letters]
    subst_set = set(subst_l)    
    subst_set.discard(word)

    # turn the set back into a list and sort it, for easier viewing
    subst_l = sorted(list(subst_set))
    
    if verbose: print(f"Input word = {word} \nsubst_l {subst_l}")   
    
    return subst_l

def ins_letter(word, verbose=False):
    '''
     return list of words with inserted letter
    ''' 
    letters = 'abcdefghijklmnopqrstuvwxyz'
    ins_l = []
    split_l = []
    

    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    ins_l = [L + l + R for L,R in split_l for l in letters]
    
    if verbose: print(f"Input word {word} \nins_l = {ins_l}")
    
    return ins_l

def edit_one_letter(word):
    """
    return a set of real/non word which is within edit distance of one 
    """
    edit_one_set = set(delete_letter(word) + transpose_letter(word) + subst_letter(word) + ins_letter(word))
    
    return edit_one_set

def edit_two_letters(word):
    '''
    return a set of real/non word which is within edit distance of two
    '''
    
    edit_one = edit_one_letter(word)
    edit_two_set = set()
    for w in edit_one:
        edit_two = edit_one_letter(w)
        edit_two_set = edit_two_set.union(edit_two_set, edit_two)
   
    return edit_two_set

def min_edit_distance(source, target, ins_cost = 1, del_cost = 1, rep_cost = 1, trp_cost= 1):

    # use deletion and insert cost as  1
    m = len(source) 
    n = len(target) 
    #initialize cost matrix with zeros and dimensions (m+1,n+1) 
    D = np.zeros((m+1, n+1), dtype=int) 
    

   # Fill in column 0, from row 1 to row m, both inclusive
    for row in range(1,m+1): 
        D[row,0] = D[row-1, 0] + del_cost
        
    # Fill in row 0, for all columns from 1 to n, both inclusive
    for col in range(1,n+1): 
        D[0,col] = D[0, col-1] + ins_cost
                
    # Loop through row 1 to row m, both inclusive
    for row in range(1,m+1): 
        
        # Loop through column 1 to column n, both inclusive
        for col in range(1,n+1):
            
            # Intialize r_cost to the 'replace' cost that is passed into this function
            r_cost = rep_cost
            
            # Check to see if source character at the previous row
            # matches the target character at the previous column, 
            if source[row-1] == target[col-1]:
                # Update the replacement cost to 0 if source and target are the same
                r_cost = 0
              
            # Update the cost at row, col based on previous entries in the cost matrix
            D[row,col] = min (D[row, col-1] + ins_cost, D[row-1, col] + del_cost, D[row-1, col-1] + r_cost)
            # transposition  
            if row>1 and col>1 and source[row-1]==target[col-2] and source[row-2] == target[col-1]:
                D[row,col] = min (D[row,col], D[row-2,col-2] + trp_cost) 
    # Set the minimum edit distance with the cost found at row m, column n
    min_distance = D[m,n]
    
    
    return D, min_distance