# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:27:56 2020

@author: USER
"""
import re
from collections import Counter
import numpy as np
import pandas as pd
import math
import random
import numpy as np
import pandas as pd
import nltk
import Candidates
import OOV
import Ngram
import ErrorModel

# Read file
with open("514-8.txt", "r") as f:
    data = f.read()
#Preprocess file    
data = re.sub(r'[^A-Za-z\.\?!\']+', ' ', data) #remove special character
data = re.sub(r'[A-Z]{3,}[a-z]+', ' ',data) #remove words with more than 3 Capital letters
sentences = re.split(r'[\.\?!]+[ \n]+', data) #split data into sentences
sentences = [s.strip() for s in sentences] #Remove leading & trailing spaces
sentences = [s for s in sentences if len(s) > 0] #Remove whitespace


tokenized_sentences=[]
for sentence in sentences:
        
        # Convert to lowercase letters
        sentence = sentence.lower()
        
        # Convert into a list of words
        tokenized = nltk.word_tokenize(sentence)
        
        # append the list of wtokenized_sentencesto the list of lists
        tokenized_sentences.append(tokenized)
        

# Get Vocabulary
vocabulary = list(set(OOV.get_nplus_words(tokenized_sentences, 2)))
vocabulary = vocabulary+['<s>']+['<e>']
# Replace less frequent word by <UNK>
processed_sentences = OOV.replace_words_below_n_by_unk(tokenized_sentences, 2)
# Get the unigram and bigram
unigram_counts = Ngram.n_grams_dict(processed_sentences, 1)
bigram_counts = Ngram.n_grams_dict(processed_sentences, 2)


def get_probability(previous_n_words, word, 
                         previous_n_gram_dict, n_gram_dict, vocabulary_size, k=1.0):
    """
    Return N-gram probability given the pair of current word and previous_n_words
    """
    assert type(previous_n_words) == list
    # convert list to tuple to use it as a dictionary key
    previous_n_words = tuple(previous_n_words,)
    
    previous_n_words_count = previous_n_gram_dict[previous_n_words] if previous_n_words in previous_n_gram_dict else 0

    # k-smoothing
    denominator = previous_n_words_count + k*vocabulary_size

    # Define n plus 1 gram as the previous n-gram plus the current word as a tuple
    n_gram = previous_n_words + (word,)

    n_gram_count = n_gram_dict[n_gram] if n_gram in n_gram_dict else 0
   
    # smoothing
    numerator = n_gram_count + 1

    probability = numerator/denominator
    
    
    return probability


def get_corrections(previous_n_words_i, word, vocab, n=2, verbose = False):
    '''
    Get n candidates with individual probability
    '''
    assert type(previous_n_words_i) == list
    corpus = ' '.join(vocabulary)
    suggestions = []
    n_best = []
    ### Convert to UNK if word not in vocab
    previous_n_words = []
    for w in previous_n_words_i:
        if w not in vocabulary:
            previous_n_words.append('<unk>')
        else:
            previous_n_words.append(w)
            
    ##Suggestions include input word only if the input word in vocab
    if word in vocab:    
        suggestions = [word] + list(Candidates.edit_one_letter(word).intersection(vocabulary)) or list(Candidates.edit_two_letters(word).intersection(vocabulary)) 
    else:
        suggestions = list(Candidates.edit_one_letter(word).intersection(vocabulary)) or list(Candidates.edit_two_letters(word).intersection(vocabulary)) 
        
    words_prob = {}
    for w in suggestions: 
        # To make sure all suggestions is within edit distance of 2
        _, min_edits = Candidates.min_edit_distance(' '.join(word),w)
        if not word in vocab: ##use error model only when it is non word error
            if min_edits <= 2:
                edit = ErrorModel.editType(w,' '.join(word))
                if edit:##Some word cannot find edit
                    if edit[0] == "Insertion":
                        error_prob = ErrorModel.channelModel(edit[3][0],edit[3][1], 'add',corpus)
                    if edit[0] == 'Deletion':
                        error_prob = ErrorModel.channelModel(edit[4][0], edit[4][1], 'del',corpus)
                    if edit[0] == 'Reversal':
                        error_prob = ErrorModel.channelModel(edit[4][0], edit[4][1], 'rev',corpus)
                    if edit[0] == 'Substitution':
                        error_prob = ErrorModel.channelModel(edit[3], edit[4], 'sub',corpus)
                else:
                    error_prob = 1
            else:
                error_prob = 1
        else:
            error_prob = 1
        language_prob = get_probability(previous_n_words, w, 
                        unigram_counts, bigram_counts, len(vocabulary), k=1.0)
            
        words_prob[w] = language_prob * error_prob
        
    n_best = Counter(words_prob).most_common(n)
    
    if verbose: print("entered word = ", word, "\nsuggestions = ", suggestions)

    return n_best

# #GUI CREATION
# from tkinter import *
# root = Tk()
# root.geometry("700x900")
# #root.configure(background = "SkyBlue4")
# root.title("NLP Spell Checker")
# Label(root, text = "Project by Group One", fg = "white", bg = "gray", font = "Times 10", height = 2, width = 200).pack()

# # function to retrieve the sentence typed by a user & pass the input through get_corrections() to check spellings
# tokenized_sentence = []
# def getInput():
#     global suggList
#     # Preprocess the original text input to get clean input
#     sentenceValues = entredSentence.get('1.0', '1000.0')
#     sentenceValues = sentenceValues.lower()
        
#     # tokenize the sentence and save the values to tokenizedWords variable
#     tokenized_sentence = nltk.word_tokenize(sentenceValues)
#     tokenized_sentence = ['<s>']+ tokenized_sentence
    
    
#     # Looping through all the words in a sentence & suggesting suitable word. n=2 gives only 2 suggestions per word
#     print("Suitable candidate words are:")
#     suggList=[]
#     for i in range(len(tokenized_sentence)-1):
#         #print(get_corrections([tokenized_sentence[i]], tokenized_sentence[i+1], vocabulary, n=2, verbose=False))
#         suggList.append(get_corrections([tokenized_sentence[i]], tokenized_sentence[i+1], vocabulary, n=2, verbose=False))
#     print(suggList)
               
            
# # Function to display a list of the suggested words
# def showSuggestions():
#     suggestedWords.delete(0.0, 'end')
#     if len(suggList) == 0:
#         print("Sorry, no suggestion can be found for your word. Try again.")
#         suggestedWords.insert(END, "Sorry, no suggestion can be found for your word. Try again.")
#         suggestedWords.config(state="disabled")
#         return; 
#     for i in range(0, len(suggList)):
#         suggestedWords.insert(END, '\n')
#         for j in range(len(suggList[i])):
#             suggestedWords.insert(END, suggList[i][j][0])
#             suggestedWords.insert(END, ' ')
# # Input widget for sentence to be entred by user
# Label(text="Enter sentence here (Max words: 500)").place(x=15, y=80)
# entredSentence = Text(root, height = 20, width = 80)
# entredSentence.place(x=15, y=110)
# submit_btn = Button(root, height=1, width=10, text="Submit", command=getInput).place(x=585, y=110)


# # Creating a suggestions widget for the suggested words to correct the mispelled word
# Label(text="List of suggested words to replace mispelled word:").place(x=15, y=350)
# suggestedWords = Text(root, height = 15, width = 40)
# #suggestedWords.config(state = "disabled")
# suggestedWords.place(x=15, y = 380)
# sugg_btn = Button(root, text="Show suggestions", command=showSuggestions).place(x=305, y=380)


# # Output widget for the sentence entered and open for correcting mispelled words
# Label(text="sentence by user:").place(x=15, y=590)
# outputSentence = Text(root, height = 20, width = 80, wrap=WORD)
# outputSentence.config(state = "disabled")
# outputSentence.place(x=15, y=620)

# root.mainloop()
    

## Testing
# with open("ori.txt", "r") as f:
#     data = f.read()
# sentence = sentence.lower()
        
# #Preprocess file    
# data = re.sub(r'[^A-Za-z\.\?!\']+', ' ', data) #remove special character
# data = re.sub(r'[A-Z]{3,}[a-z]+', ' ',data) #remove words with more than 3 Capital letters
# sentences = re.split(r'[\.\?!]+[ \n]+', data) #split data into sentences
# sentences = [s.strip() for s in sentences] #Remove leading & trailing spaces
# sentences = [s for s in sentences if len(s) > 0] #Remove whitespace


# ori_tokenized_sentences=[]
# for sentence in sentences:
        
#         # Convert to lowercase letters
#         sentence = sentence.lower()
        
#         # Convert into a list of words
#         tokenized = nltk.word_tokenize(sentence)
#         tokenized = ['<s>']+ tokenized
#         # append the list of wtokenized_sentencesto the list of lists
#         ori_tokenized_sentences.append(tokenized)
        
# with open("non.txt", "r") as f:
#     data = f.read()
# sentence = sentence.lower()
        
# #Preprocess file    
# data = re.sub(r'[^A-Za-z\.\?!\']+', ' ', data) #remove special character
# data = re.sub(r'[A-Z]{3,}[a-z]+', ' ',data) #remove words with more than 3 Capital letters
# sentences = re.split(r'[\.\?!]+[ \n]+', data) #split data into sentences
# sentences = [s.strip() for s in sentences] #Remove leading & trailing spaces
# sentences = [s for s in sentences if len(s) > 0] #Remove whitespace


# non_tokenized_sentences=[]
# for sentence in sentences:
        
#         # Convert to lowercase letters
#         sentence = sentence.lower()
        
#         # Convert into a list of words
#         tokenized = nltk.word_tokenize(sentence)
#         tokenized = ['<s>']+ tokenized
#         # append the list of wtokenized_sentencesto the list of lists
#         non_tokenized_sentences.append(tokenized)

# with open("real.txt", "r") as f:
#     data = f.read()
# sentence = sentence.lower()
        
# #Preprocess file    
# data = re.sub(r'[^A-Za-z\.\?!\']+', ' ', data) #remove special character
# data = re.sub(r'[A-Z]{3,}[a-z]+', ' ',data) #remove words with more than 3 Capital letters
# sentences = re.split(r'[\.\?!]+[ \n]+', data) #split data into sentences
# sentences = [s.strip() for s in sentences] #Remove leading & trailing spaces
# sentences = [s for s in sentences if len(s) > 0] #Remove whitespace


# real_tokenized_sentences=[]
# for sentence in sentences:
        
#         # Convert to lowercase letters
#         sentence = sentence.lower()
        
#         # Convert into a list of words
#         tokenized = nltk.word_tokenize(sentence)
#         tokenized = ['<s>']+ tokenized
        
#         # append the list of wtokenized_sentencesto the list of lists
#         real_tokenized_sentences.append(tokenized)
        
# # Looping through all the words in a sentence & suggesting suitable word. n=2 gives only 2 suggestions per word

# ori_List=[]
# for sentence in ori_tokenized_sentences:
#     for i in range(len(sentence)-1):
#         ori_List+=[sentence[i+1]]

# real_corr_List=[]
# for sentence in real_tokenized_sentences:
#     for i in range(len(sentence)-1):
#         if get_corrections([sentence[i]], sentence[i+1], vocabulary, n=1, verbose=False):
#             real_corr_List+=[get_corrections([sentence[i]], sentence[i+1], vocabulary, n=1, verbose=False)[0][0]]
#         else:
#             real_corr_List+=[sentence[i+1]]
    
# non_corr_List=[]
# for sentence in non_tokenized_sentences:
#     for i in range(len(sentence)-1):
#         if get_corrections([sentence[i]], sentence[i+1], vocabulary, n=1, verbose=False):
#             non_corr_List+=[get_corrections([sentence[i]], sentence[i+1], vocabulary, n=1, verbose=False)[0][0]]
#         else:
#             non_corr_List+=[sentence[i+1]]

# ### Real Word Error
# print('Real-word error Evaluation')
# ##Determine if the speelling error occur
# boolean =[]
# for i in range(len(ori_tokenized_sentences)):
#     for j in range(len(ori_tokenized_sentences[i])-1):
#         if ori_tokenized_sentences[i][j+1]==real_tokenized_sentences[i][j+1]:
#             boolean += ['c']
#         else:
#             boolean += ['w']
# tp,tn,fp,fn=0,0,0,0           
# for i in range(len(real_corr_List)):
#     if boolean[i] == 'c':
#         if real_corr_List[i] == ori_List[i]:
#             tp+=1
#         else:
#             fp+=1
#     if boolean[i] == 'w':
#         if real_corr_List[i] == ori_List[i]:
#             tn+=1
#         else:
#             fn+=1
# ##Confusion matrix
# from prettytable import PrettyTable
    
# x = PrettyTable()
# x.field_names = [" ", "c", "w"]
# x.add_row(["c", tp, fp])
# x.add_row(["w", fn, tn])
# print(x)

# accuracy=(tp+tn)/(tp+fp+fn+tn)
# precision=tp/(tp+fp)
# recall=tp/(tp+fn)
# f1=2*(precision*recall)/(precision+recall)
# print('R_Accuracy',accuracy,'\n')
# print('R_Precision',precision,'\n')
# print('R_Recall',recall,'\n')
# print('R_Precision',f1)




# ### Non Word Error
# print('Non-word error Evaluation')
# boolean =[]
# for i in range(len(ori_tokenized_sentences)):
#     for j in range(len(ori_tokenized_sentences[i])-1):
#         if ori_tokenized_sentences[i][j+1]==non_tokenized_sentences[i][j+1]:
#             boolean += ['c']
#         else:
#             boolean += ['w']
# tp,tn,fp,fn=0,0,0,0           
# for i in range(len(real_corr_List)):
#     if boolean[i] == 'c':
#         if non_corr_List[i] == ori_List[i]:
#             tp+=1
#         else:
#             fp+=1
#     if boolean[i] == 'w':
#         if non_corr_List[i] == ori_List[i]:
#             tn+=1
#         else:
#             fn+=1
# ##Confusion Matrix
# z = PrettyTable()
# z.field_names = [" ", "c", "w"]
# z.add_row(["c", tp, fp])
# z.add_row(["w", fn, tn])
# print(z)

# accuracy=(tp+tn)/(tp+fp+fn+tn)
# precision=tp/(tp+fp)
# recall=tp/(tp+fn)
# f1=2*(precision*recall)/(precision+recall)
# print('N_Accuracy',accuracy,'\n')
# print('N_Precision',precision,'\n')
# print('N_Recall',recall,'\n')
# print('N_Precision',f1)
    
# GUI CREATION THROUGH PYTHON'S TKINTER LIBRARY
from tkinter import * 

# creates a base GUI window
root = Tk() 

# creating fixed geometry of the tkinter window with dimensions 700x900
root.geometry("705x780") 
root.configure(background = "gray76")

root.title("NLP Spell Checker") # Adding a title to the GUI window.
Label(root, text = "Project by Group One", fg = "navy", bg = "gray", font = "Arial 11 bold italic", height = 3, width = 200).pack()

 

# function to retrieve the sentence typed by a user & pass the input through get_corrections() to check spellings
tokenized_sentence = []
non_real_word = []

clicked=StringVar()
def getInput():
    global tokenized_sentence
    # Preprocess the original text input to get clean input
    sentenceValues = entredSentence.get('1.0', '50.0')
    sentenceValues = sentenceValues.lower()
    outputSentence.delete(0.0, 'end')
    outputSentence.insert(END, sentenceValues)  
    
    # tokenize the sentence and save the values to tokenizedWords variable
    tokenized_sentence = nltk.word_tokenize(sentenceValues)
    tokenized_sentence = ['<s>']+ tokenized_sentence
    
    not_in_corpus=[]
    real_word_error=[]
    for word in tokenized_sentence:
        if word not in vocabulary:
            not_in_corpus.append(word)  # Saving non real word to not_in_corpus list.

    for word in tokenized_sentence[1:]:
        if word in vocabulary: 
            index=tokenized_sentence.index(word)
            candidate_words = get_corrections([tokenized_sentence[index-1]], word, vocabulary, n=1, verbose=False)
            if candidate_words[0][0] != word :
                real_word_error.append(word) # saving a real & existing word to real_word_error
    print(real_word_error)            
    print("Suitable candidate words are:")
    
    # Checking for non_word errors from the input sentence typed by a user
    options=[]
    for word in not_in_corpus:
        
        offset = '+%dc' % len(word) # +5c (5 chars)
    
        # search word from first char (1.0) to the end of text (END)
        pos_start = entredSentence.search(word, '1.0', END)
        
        # check if the word has been found
        while pos_start:
        
            # create end position by adding (as string "+5c") number of chars in searched word 
            pos_end = pos_start + offset
        
            # add tag
            entredSentence.tag_add('red_tag', pos_start, pos_end)
        
            # search again from pos_end to the end of text (END)
            pos_start = entredSentence.search(word, pos_end, END)
        
        options.append(word)   
    
    # checking for real word error from the input sentence by a user
    for word in real_word_error:
        offset = '+%dc' % len(word) # +5c (5 chars)
    
        # search word from first char (1.0) to the end of text (END)
        pos_start = entredSentence.search(word, '1.0', END)
        
        # check if the word has been found
        while pos_start:
        
            # create end position by adding (as string "+5c") number of chars in searched word 
            pos_end = pos_start + offset
        
            # add tag
            entredSentence.tag_add('blue_tag', pos_start, pos_end)
        
            # search again from pos_end to the end of text (END)
            pos_start = entredSentence.search(word, pos_end, END)
        
        options.append(word)   
    
    # Creating a drop down menu to display the misspelled words.
    # From this drop down list, a user selects the misspelled word that they need suggestions for.
    drop = OptionMenu(root,clicked,*options)
    drop.configure(font=("Arial", 10))
    drop.pack()
    drop.place(x=305, y = 350)

# Function to display a list of the suggested words
def showSuggestions():
    suggestedWords.delete(0, END)
    options=[]
    word_to_replace = clicked.get()
    index=tokenized_sentence.index(word_to_replace)
    
    candidate_words = get_corrections([tokenized_sentence[index-1]], word_to_replace, vocabulary, n=3, verbose=False)
    print(candidate_words)
    for i in range(len(candidate_words)):
        suggestedWords.insert(END,candidate_words[i][0])

    
# Function to replace a misspelled word with the correct word from a list of suggested words            
def replace_word():
    word_to_replace = clicked.get()
    selected_word=suggestedWords.get(ANCHOR)
    offset = '+%dc' % len(word_to_replace) # +5c (5 chars)
    idx = '1.0'
    #searches for desried string from index 1  
    idx = outputSentence.search(word_to_replace, idx, nocase = 1,  
                            stopindex = END) 
    # last index sum of current index and  
    # length of text  
    lastidx = '% s+% dc' % (idx, len(word_to_replace)) 
  
    outputSentence.delete(idx, lastidx) 
    outputSentence.insert(idx, selected_word) 
  
    lastidx = '% s+% dc' % (idx, len(selected_word))  
            
# Input widget for sentence to be entred by user
Label(text="Enter sentence here (Max Words: 500)", font="Arial 11 bold").place(x=15, y=80)
entredSentence = Text(root, height = 10, width = 60)
entredSentence.configure(font=("Arial", 11))
entredSentence.place(x=15, y=110)
submit_btn = Button(root, height=1, width=10, text="Submit", command=getInput).place(x=585, y=110)
entredSentence.tag_config("red_tag", foreground="red", underline=1)
entredSentence.tag_config("blue_tag", foreground="blue", underline=1)


# Creating a suggestions widget for the suggested words to correct the mispelled word
Label(text="List of suggested words to replace misspelled word:", font = "Arial 11 bold").place(x=15, y=320)
suggestedWords = Listbox(root, height = 10, width = 30)
suggestedWords.configure(font=("Arial", 11))
#suggestedWords.config(state = "disabled")
suggestedWords.place(x=15, y = 350)
sugg_btn = Button(root, text="Show suggestions", command=showSuggestions).place(x=305, y=380)
replace_btn = Button(root, text="Replace Word", command=replace_word).place(x=305, y=410)

 
# Output widget for the sentence entered and open for correcting mispelled words
Label(text="Corrected Input Sentence by User:", font = "Arial 11 bold").place(x=15, y=560)
outputSentence = Text(root, height = 10, width = 60, wrap=WORD)
outputSentence.configure(font=("Arial", 11))
#outputSentence.config(state = "disabled")
outputSentence.place(x=15, y=590)

 
# Activating the GUI
root.mainloop()