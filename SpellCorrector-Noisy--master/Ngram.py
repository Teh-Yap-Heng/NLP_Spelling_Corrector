# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:02:47 2020

@author: USER
"""

def n_grams_dict(tokenized_sentences, n, start_token='<s>', end_token = '<e>'):
    """
    Return all n_grams with count
    """  
    n_grams = {}

    for sentence in tokenized_sentences: # complete this line
        
        # add start and end token
        sentence = n * [start_token] + sentence + [end_token]
        # convert to tuple
        sentence = tuple(sentence)

        for i in range(len(sentence)-n+1): 

            n_gram = sentence[i:i+n]
            
            if n_gram in n_grams:
                n_grams[n_gram] += 1
            else:
                n_grams[n_gram] = 1
    
            ### END CODE HERE ###
    return n_grams