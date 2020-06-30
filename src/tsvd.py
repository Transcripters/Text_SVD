# Maps the word pair occurence frequencies on a text.
# Updates wordset to include all the words from the text.
# Outputs a wordset x wordset matrix where every entry is
# the frequency of that word pair (row followed by column).
def markovmap(text,wordset):
    text=[word for word in ''.join(char for char in text if char.isalpha() or char==' ').split(' ') if not word=='']
    wordset=wordset.union({word for word in text})
    #A map for quickly finding matrix coordinates
    hashmap={}
    for i,w in enumerate(wordset):
        hashmap[w]=i
    matrix=[[0 for w in wordset] for w in wordset]
    for i in range(len(text)-1):
        matrix[hashmap[text[i]]][hashmap[text[i+1]]]+=1
    return matrix

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
    matrix=markovmap(our_file.read(),wordset)
    print("Done!")
    sns.heatmap(data=matrix)
    plt.show()