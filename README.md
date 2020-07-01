# TSVD - A simple text analysis tool

This is a tool meant to compare texts and measure how "similar" they are conceptually. The method used has no basis besides some scientific intuition and experience with Data Science.

For understanding how this works, please refer to [the documentation](./docs/main.md).

## Sample output

`python3 src/generator.py --text_ref samples/effects_of_nuctest,samples/manedwolf --stopwords data/nltk_stopwords --out demo;python3 src/comparator.py --tsvd demo.tsvd --dict demo.dict --text_comp samples/tunguska,samples/nuctest,samples/fennec --stopwords data/nltk_stopwords`

Running the command above on the root directory of the project yields the following result:

```
Comparing texts...
## Analysing "samples/tunguska" ##
Reference "samples/effects_of_nuctest":
        Normalized magnitude: 1.0
        Normalized angle: 0.0
        Normalized score: 1.0
Reference "samples/manedwolf":
        Normalized magnitude: 0.0
        Normalized angle: 1.0
        Normalized score: 0.0
## Analysing "samples/nuctest" ##
Reference "samples/effects_of_nuctest":
        Normalized magnitude: 1.0
        Normalized angle: 0.0
        Normalized score: 1.0
Reference "samples/manedwolf":
        Normalized magnitude: 0.0
        Normalized angle: 1.0
        Normalized score: 0.0
## Analysing "samples/fennec" ##
Reference "samples/effects_of_nuctest":
        Normalized magnitude: 0.0
        Normalized angle: 1.0
        Normalized score: 0.0
Reference "samples/manedwolf":
        Normalized magnitude: 1.0
        Normalized angle: 0.0
        Normalized score: 1.0
Done!
```

One can easily see that both the "Tunguska Event" sample (samples/tunguska) and "Nuclear Tests" sample (samples/nuctest) align better with `samples/effects_of_nuctest` and the article about the Fennec Fox aligns better with the one about Maned Wolves.

These results are only that well-separated (0 and 1) because we have two samples and we normalize the values over the results of all the references. For more than two references one should receive intermediary values too.

All those texts were extracted from wikipedia.

The subject choice was merely by chance. The "Tunguska Event" article was featured on the frontpage when development started and I thought it would be nice to compare it with nuclear events. The "Maned Wolf" and "Fennec Fox" articles came from the need of having a "not aligned" reference and my personal liking of those animals.