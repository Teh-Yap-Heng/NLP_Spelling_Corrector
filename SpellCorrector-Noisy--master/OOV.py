# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:34:59 2020

@author: USER
"""

def count_words(tokenized_sentences):
    """
    Count the number of each individual word in every sentences
    """
    word_counts = {}
    for sentence in tokenized_sentences: # complete this line
        word_counts
        # Go through each token in the sentence
        for token in sentence: # complete this line

            # If the token is not in the dictionary yet, set the count to 1
            if not token in word_counts: # complete this line
                word_counts[token] = 1
            
            # If the token is already in the dictionary, increment the count by 1
            else:
                word_counts[token] += 1

    
    return word_counts

def get_nplus_words(tokenized_sentences, n):
    """
    Find words in corpus with nplus frequency
    """
    nplus_vocab = []
    
    word_counts = count_words(tokenized_sentences)

    for word, cnt in word_counts.items():
        if cnt >= n:
            nplus_vocab.append(word)
    
    return  nplus_vocab

def replace_words_below_n_by_unk(tokenized_sentences, n=2):
    """
    Process training data to replace words with frequency less than n by UNK
    """
    vocabulary = set(get_nplus_words(tokenized_sentences, n))
    
    processed_tokenized_sentences = []
    
    for sentence in tokenized_sentences:
        temp_sentence = []
        
        for token in sentence: 
            if token in vocabulary: # complete this line
                temp_sentence.append(token)
            else:
                temp_sentence.append("<unk>")
        
        processed_tokenized_sentences.append(temp_sentence)
        
    return processed_tokenized_sentences