import numpy as np

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

matrix, min_distance = min_edit_distance('intention','intentino')
print(f" the matrix is: \n {matrix} ")
print(f" the minimum distance is: \n {min_distance}")

