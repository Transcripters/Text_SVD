# generator - A tsvd dictionary/vectormap pair generator
# Made with <3 by Amélia O. F. da S.
# Make good use!

import melmap
from sklearn.decomposition import TruncatedSVD
import math
import argparse
import pickle
parser=argparse.ArgumentParser(description="A simple text comparation interface")
parser.add_argument('--text_ref',help='A comma-separated list of paths to the references to be compiled',required=True)
parser.add_argument('--stopwords',help='Stopwords dictionary',required=True)
parser.add_argument('--out',help='The destination filename root (a pair of files will be generated with this name and different extensions)',default="generated")
args=vars(parser.parse_args())

stopwords=[]
with open(args['stopwords']) as our_dictionary:
    stopwords=our_dictionary.read().split("\n")
    our_dictionary.close()

wordset=set()
print("Generating dictionary...")
our_files=args['text_ref']
files=our_files.split(',')
for fil in files:
    with open(fil) as ff:
        text=ff.read()
        melmap.addwords(text,wordset,stopwords)
        ff.close()

print("Mapping reference matrices...")
labels=[]
referencematrices=[]
our_files=args['text_ref']
files=our_files.split(',')
for reference in files:
    with open(reference) as our_file:
        text=our_file.read()
        labels,matrix=melmap.freqMap(text,wordset,5,stopwords,lambda w: w**2)
        referencematrices.append(matrix)
        our_file.close()
print("Done!")
print("Generating reference vectors (SVDs)...")
referenceSVDs=[]
for i,matrix in enumerate(referencematrices):
    SVD=TruncatedSVD(n_components=1,random_state=1)
    SVD.fit(matrix)
    referenceSVDs.append((SVD.components_[0],[entry[0] for entry in SVD.transform(matrix)],files[i]))
    print('# Reference "'+files[i]+'"')
    print("\tMagnitude: "+str(round(melmap.scprod(referenceSVDs[-1][1],referenceSVDs[-1][1]),4)))
print("Done!")
print("Packing data into output files (pickle format)...")
with open(args['out']+'.dict','wb') as our_file:
    pickle.dump(list(wordset),our_file)
with open(args['out']+'.tsvd','wb') as our_file:
    pickle.dump(referenceSVDs,our_file)