# TSVD Documentation

## How does this work?

This text analysis method was conceived by Amélia O. F. da S. (User [m3101](https://github.com/m3101) on github, aka me, the one writing this document) based on her intuitions and previous experiences with data analysis.

There are three main phases on the analysis:

### Phase 1 - Dictionary mapping

Firstly, we take all the input texts and create a set with all unique words contained within them. Stop words (common, not very significant words like articles, prepositions etc.) are removed from this dictionary.

> Words not on the dictionary don't count for either the analysis nor the measurement of word-distances!

### Phase 2 - Frequency map/Convolution

In this phase, we take each text and create a matrix for representing it. We'll be referring to this matrix as the "frequency map"(or `freqMap`, in the code).

This matrix will be created by a convolution-like process: each row represents a word, and each column represents another. Every time the `row word+column word` pair occurs, that space in the matrix will be incremented by a certain amount. The words don't need to be contiguous: their distance will be accounted for when mapping the text.

This concept will be better understood through an example:

Let's suppose you have the text "SVD is a nice tool" and we're using the default configuration (maximum distance being 5 and we score the word proximity by square proximity).

Our matrix will have three columns/rows: "SVD", "nice" and "tool".

The "SVD"x"nice" pair (row "SVD", column "nice") will have the value of 16, as it occurs once and at a proximity of 4 (1-word distance out of a maximum of 5 words) and we're using the square of that value.

The "SVD"x"tool" pair will have the value of 9, as it occurs once and at a proximity of 3.

> For more complex texts, this map will show us what groups of words tend to be used together. This will be useful for extracting the overall "subject" of the text.

## Phase 3 - SVD and vectorial representation

With the frequency maps on our hands, we now have to find a way of comparing our texts. This method does this by converting them into vectors that can be projected onto one another.

To do this, we make a `Singular Vector Decomposition` of all of our "reference" texts and store both the most important vector of that projection (the one with the highest eigenvalue) and the reduction of that reference map on that vector.

After doing that for all the references, we can project our "target" texts on each decomposition and compare the resulting vectors with the reference vectors. This gives us an overall "alignment" between the main components of the reference and target texts.

#### Why SVD?

A while ago I saw some word-frequency maps on an article and saw some interesting patterns. Words that represented certain concepts, like "Green energy" or "Coal power" seemed to group together in a linear fashion (graphically, rectangles and squares, for example). This inspired the use of a SVD to extract those "squares" from the maps so we can compare the "concepts" instead of comparing words.

I don't really know whether there is any research on this already, but it felt like a good idea, and it seems to have yielded interesting results.