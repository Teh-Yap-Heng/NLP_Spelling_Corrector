# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:56:32 2020

@author: USER
"""

import ast
f=open('addconfusion.data', 'r')
data=f.read()
f.close
addmatrix=ast.literal_eval(data)
f=open('subconfusion.data', 'r')
data=f.read()
f.close
submatrix=ast.literal_eval(data)
f=open('revconfusion.data', 'r')
data=f.read()
f.close
revmatrix=ast.literal_eval(data)
f=open('delconfusion.data', 'r')
data=f.read()
f.close
delmatrix=ast.literal_eval(data)

def editType(candidate, word):
        "Method to calculate edit type for single edit errors."
        edit=[False]*4
        correct=""
        error=""
        x=''
        w=''
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        candidate=candidate[::-1]
        word=word[::-1]
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        if word == candidate:
            return "None", '', '', '', ''
        if edit[1]:
            return "Deletion", correct, error, x, w
        elif edit[0]:
            return "Insertion", correct, error, x, w
        elif edit[2]:
            return "Substitution", correct, error, x, w
        elif edit[3]:
            return "Reversal", correct, error, x, w
        
def channelModel(x,y, edit,corpus):
        """Method to calculate channel model probability for errors."""
        
        if edit == 'add':
            if x == '#':
                return addmatrix[x+y]/corpus.count(' '+y)
            else:
                return addmatrix[x+y]/corpus.count(x)
        if edit == 'sub':
            return submatrix[(x+y)[0:2]]/corpus.count(y)
        if edit == 'rev':
            return revmatrix[x+y]/corpus.count(x+y)
        if edit == 'del':
            return delmatrix[x+y]/corpus.count(x+y)