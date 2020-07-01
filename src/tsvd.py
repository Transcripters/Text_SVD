import pdb
import random
import collections
random.seed(10)

stopwords=[]
with open("data/nltk_stopwords") as our_dictionary:
    stopwords=our_dictionary.read().split("\n")
    our_dictionary.close()

# Adds a text's words to the shared dictionary.
def addwords(text,wordset):
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
def freqMap(text,wordset,weightscale,weightfunc=lambda w: w):
    text=[word.lower() for word in ''.join(char for char in text.replace('\n',' ') if char.isalpha() or char==' ').split(' ') if not word=='' and not word in stopwords]
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

# Calculates the scalar product between two vectors
def scprod(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])
# Calculates the angle between two vectors
def vectorAngle(a,b):
    return math.acos((scprod(a,b))/(math.sqrt(scprod(a,a))*math.sqrt(scprod(b,b))))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import TruncatedSVD
import math
import argparse
parser=argparse.ArgumentParser(description="A simple naïve interface for doing wordpair frequency analysis")
parser.add_argument('--text_ref',help='The files we will compare to ("concept" references)')
parser.add_argument('--text_comp',help="The files to be compared/measured")
args=vars(parser.parse_args())
if not args['text_ref'] or not args['text_comp']:
    raise Exception("Not enough files specified.")
wordset=set()
print("Generating dictionary...")
our_files=args['text_ref']
files=our_files.split(',')
for fil in files:
    with open(fil) as ff:
        text=ff.read()
        addwords(text,wordset)
        ff.close()
our_files=args['text_comp']
files=our_files.split(',')
for fil in files:
    with open(fil) as ff:
        text=ff.read()
        addwords(text,wordset)
        ff.close()
wordset=frozenset(wordset)

print("Mapping reference matrices...")
labels=[]
referencematrices=[]
our_files=args['text_ref']
files=our_files.split(',')
for reference in files:
    with open(reference) as our_file:
        text=our_file.read()
        labels,matrix=freqMap(text,wordset,5,lambda w: w**2)
        referencematrices.append(matrix)
        our_file.close()
print("Done!")
print("Generating reference vectors (SVDs)...")
referenceSVDs=[]
for i,matrix in enumerate(referencematrices):
    SVD=TruncatedSVD(n_components=1,random_state=1)
    SVD.fit(matrix)
    referenceSVDs.append((SVD,[entry[0] for entry in SVD.transform(matrix)],files[i]))
    print('# Reference "'+files[i]+'"')
    print("\tMagnitude: "+str(round(scprod(referenceSVDs[-1][1],referenceSVDs[-1][1]),4)))
    if "i" in args:
        components=pd.DataFrame(data=[(labels[item[0]],item[1]) for item in sorted(enumerate(SVD.components_[0]),reverse=True,key=lambda x:x[1])[:20]],columns=["Word","Weight"]
)
        sns.barplot(data=components,x="Weight",y="Word")
        plt.show()
print("Done!")
print("Comparing texts...")
our_files=args['text_comp']
files=our_files.split(',')
for fil in files:
    with open(fil) as ff:
        textb=ff.read()
        _,matrixb=freqMap(textb,wordset,5,lambda w: w**2)
        vectorb=[entry[0] for entry in SVD.transform(matrixb)]
        print('## Analysing "'+fil+'" ##')
        for reference in referenceSVDs:
            projection=[entry[0] for entry in reference[0].transform(matrixb)]
            print('* Text "'+reference[2]+'"')
            print('\t* Projection magnitude: '+str(round(scprod(projection,projection),4)))
            print('\t* Projection angle: '+str(round(vectorAngle(reference[1],projection),2))+'rad')
        ff.close()
print("Done!")