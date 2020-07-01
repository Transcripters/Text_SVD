# melmap - An implementation of my still unnamed text comparation method (currently named melmap)
# Made with <3 by Amélia O. F. da S.
# Make good use!

import random
import collections
import math
random.seed(3101)

# Adds a text's words to the shared dictionary.
def addwords(text,wordset,stopwords):
    text=[word.lower() for word in ''.join(char for char in text.replace('\n',' ') if char.isalpha() or char==' ').split(' ') if not word=='' and not word in stopwords]
    wordset.update({word for word in text})
# Maps the word pair occurence frequencies on a text.
# Updates wordset to include all the words from the text.
# Outputs a wordset x wordset matrix where every entry is
# the "weight" of that word pair (row followed by column)
# and a dictionary of ordered labels for each word. These 
# results come in a tuple (labels,matrix).
# The "weight" of a combination is basically a convolution
# With many the pair of words in many different distances.
# Weightscale defines how far back we'll look for each word
# pair. The distance (in words) is then passed to <weightfunc>,
# which can transform that weight (for giving more importance to
# closer words, for example).
def freqMap(text,wordset,weightscale,stopwords,weightfunc=lambda w: w):
    text=[word.lower() for word in ''.join(char for char in text.replace('\n',' ') if char.isalpha() or char==' ').split(' ') if (not word=='' and not word in stopwords) and word in wordset]
    #A map for quickly finding matrix coordinates
    hashmap=collections.OrderedDict()
    for i,w in enumerate(wordset):
        hashmap[w]=i
    matrix=[[0 for w in hashmap.keys()] for w in hashmap.keys()]
    for i in range(len(text)):
        for j in range(-weightscale,weightscale):
            compindex=i+j
            if compindex<0 or compindex>=len(text) or compindex==i:
                break
            matrix[hashmap[text[i]]][hashmap[text[compindex]]]+=weightfunc((weightscale-abs(j))+1)
    return ([key for key in hashmap.keys()],matrix)
# Orders a freqMap so the most frequent words are the first
# Returns a label list and a matrix in a (labels,matrix) tuple
def ordermatrix(labels,matrix):
    wordfrequencies=[]
    for i,w in enumerate(labels):
        wordfrequencies.append((i,(sum(matrix[i])+sum([row[i] for row in matrix])),w))
    wordfrequencies=sorted(wordfrequencies,key=lambda item: item[1],reverse=True)
    print(wordfrequencies[:4])
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
    return (labels,matrix)
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
        nword=random.random()*totalfreq
        accrand=0
        for i in range(len(labels)):
            accrand+=wmap[cur][i]
            if accrand>nword:
                print(labels[cur],end=" ")
                cur=i
                break
        l+=1
# Applies dimensionality reduction on a matrix
def ApplyComponent(matrix,component):
    return [sum([row[i]*component[i] for i in range(len(row))]) for row in matrix]
# Calculates the scalar product between two vectors
def scprod(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])
# Calculates the angle between two vectors
def vectorAngle(a,b):
    return math.acos((scprod(a,b))/(math.sqrt(scprod(a,a))*math.sqrt(scprod(b,b))))
# Generates a list of comparation indices for a given matrix.
# It has the following format: [(magnitude,angle,alignment index),...].
# All values are normalized so each tuple entry goes from 0 (smallest value
# within the references) to 1 (bigges value within the references)
#def compare(references,matrix):