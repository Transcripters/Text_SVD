# TSVD - A simple text analysis tool

This is a tool meant to compare texts and measure how "similar" they are conceptually. The method used has no basis besides some scientific intuition and experience with Data Science.

For using the tool, clone this repository and run `src/tsvd --text_ref <your references> --text_comp <texts to compare>`. 

This will yield a result in the following format:

```
## Analysing "<file to compare>" ##
* Text "<your first reference>"
    * Projection magnitude: <a number>
    * Projection angle: <an angle>
* Text "<your second reference>"
[...]
## Analysing "<second file to compare>" ##
[...]
```

Then you may evaluate how "similar" the texts are through the magnitude and angle of the projections. A smaller angle and bigger magnitude means a better alignment.

For understanding how this works, refer to [the documentation](./docs/main.md).

## Sample output

`python3 src/tsvd.py --text_ref samples/effects_of_nuctest,samples/manedwolf --text_comp samples/tunguska,samples/nuctest`

Running the command above on the root directory of the project yields the following result:

```
Generating dictionary...
Mapping reference matrices...
Done!
Generating reference vectors (SVDs)...
# Reference "samples/effects_of_nuctest"
        Magnitude: 472105.0176
# Reference "samples/manedwolf"
        Magnitude: 2147989.2448
Done!
Comparing texts...
## Analysing "samples/tunguska" ##
* Text "samples/effects_of_nuctest"
        * Projection magnitude: 28654.8833
        * Projection angle: 1.12rad
* Text "samples/manedwolf"
        * Projection magnitude: 6720.2297
        * Projection angle: 1.56rad
## Analysing "samples/nuctest" ##
* Text "samples/effects_of_nuctest"
        * Projection magnitude: 442626.3335
        * Projection angle: 1.32rad
* Text "samples/manedwolf"
        * Projection magnitude: 6380.6524
        * Projection angle: 1.57rad
Done!
```

It's clearly visible that both the Tunguska event wikipedia article (samples/tunguska) and the article about nuclear tests (samples/nuctest) align better with the "Effects of Nuclear Tests" reference (samples/effects_of_nuctest) than with the "Maned Wolf" reference (samples/manedwolf).

All those texts were extracted from wikipedia.

The subject choice was merely by chance. The "Tunguska Event" article was featured on the frontpage when development started and I thought it would be nice to compare it with nuclear events. The "Maned Wolf" article came from the need of having a "not aligned" reference and my personal liking of those animals.