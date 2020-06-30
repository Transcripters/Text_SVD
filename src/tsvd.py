import pdb
import random

# Maps the word pair occurence frequencies on a text.
# Updates wordset to include all the words from the text.
# Outputs a wordset x wordset matrix where every entry is
# the frequency of that word pair (row followed by column).
def markovmap(text,wordset):
    text=[word.lower() for word in ''.join(char for char in text.replace('\n',' ') if char.isalpha() or char==' ').split(' ') if not word=='']
    wordset.update({word for word in text})
    #A map for quickly finding matrix coordinates
    hashmap={}
    for i,w in enumerate(wordset):
        hashmap[w]=i
    matrix=[[0 for w in wordset] for w in wordset]
    for i in range(len(text)-1):
        matrix[hashmap[text[i]]][hashmap[text[i+1]]]+=1
    return matrix
# Orders a markovmap so the most frequent words are the first
# Returns a label list and a matrix in a (labels,matrix) tuple
def ordermatrix(matrix,wordset):
    wordfrequencies=[]
    for i,w in enumerate(wordset):
        wordfrequencies.append((i,(sum(matrix[i])+sum([row[i] for row in matrix])),w))
    wordfrequencies=sorted(wordfrequencies,key=lambda item: item[1],reverse=True)
    #First we switch the matrix's rows to the desired order
    for i in range(len(matrix)):
        if wordfrequencies[i][0]!=i:
            temp=matrix[i]
            matrix[i]=matrix[wordfrequencies[i][0]]
            matrix[wordfrequencies[i][0]]=temp
    #Then we do the same for the columns.
    for i in range(len(matrix)):
        if wordfrequencies[i][0]!=i:
            for row in matrix:
                temp=row[i]
                row[i]=row[wordfrequencies[i][0]]
                row[wordfrequencies[i][0]]=temp
    labels=[tup[2] for tup in wordfrequencies]
    return (matrix,labels)
# Generates a random text of up to <n> words using the given frequency map and labels.
def gibberish_from_map(wmap,labels,n):
    if n<=0:
        return
    l=0
    #Current word
    cur=random.randint(0,len(labels))
    while l<n:
        totalfreq=sum(wmap[cur])
        if(totalfreq==0):
            return
        nword=random.randint(0,totalfreq)
        accrand=0
        for i in range(len(labels)):
            accrand+=wmap[cur][i]
            if accrand>nword:
                print(labels[cur],end=" ")
                cur=i
                break
        l+=1

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import TruncatedSVD
import math
import argparse
parser=argparse.ArgumentParser(description="A simple naïve interface for doing wordpair frequency analysis")
parser.add_argument('--file',help="The file to be analysed")
args=vars(parser.parse_args())
if not args['file']:
    raise Exception("No file specified.")
with open(args['file']) as our_file:
    wordset=set()
    print("Generating frequency matrix...")
    matrix,labels=ordermatrix(markovmap(our_file.read(),wordset),wordset)
    print("Done!")
    print("Generating SVD...")
    SVD=TruncatedSVD(n_components=len(labels)-1,random_state=1)
    SVD.fit(matrix)
    print("Done!")
    print("The two most important components are")
    components=sorted(enumerate(SVD.components_[0]),key=lambda x: x[1],reverse=True)
    print('Component "'+labels[components[0][0]]+' '+labels[components[1][0]]+'"')
    print("And")
    components=sorted(enumerate(SVD.components_[1]),key=lambda x: x[1],reverse=True)
    print('Component "'+labels[components[0][0]]+' '+labels[components[1][0]]+'"')
    gibberish_from_map(matrix,labels,32)
    sns.heatmap(data=matrix,cmap=sns.color_palette("Blues"))
    plt.show()