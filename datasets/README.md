Original datasets 
-----------------

We did not include the original datasets in this repository. These were:

- CantusCorpus: https://github.com/bacor/cantuscorpus
- GregoBaseCorpus: https://github.com/bacor/gregobasecorpus
- Several subsets from the Essen Folksong Collection: https://kern.humdrum.org/cgi-bin/browse?l=/essen
- Densmore collection: https://github.com/shanahdt/densmore/

The last two you can also find in Catafolk, e.g. https://bacor.github.io/catafolk/datasets/erk-deutscher-liederhort/0.0.1. 
The structure of the `datasets/` directory is as follows:

```
- boehme
    - deut2272.krn
    - deut2273.krn
    ...

- cornelissen-etal-2020
  - run-0
    - antiphon
      - full 
        - data-generation.log  
        - test-chants.csv
        - test-features.csv
        ...
      - subset
    - responsory
  - run-1
  - run-2

- creighton
  - kern
    - nova001.krn
    - nova002.krn
    - ...

- densmore-choctaw
  - data
    - choct01.krn
    - choct02.krn
    - ...

(similar for all Densmore dataset)

- densmore-maidu
- densmore-menominee
- densmore-nootka
- densmore-northern-ute
- densmore-ojibway
- densmore-papago
- densmore-pawnee
- densmore-pueblo
- densmore-teton-sioux


- erk
  - deut0567.krn
  - deut0568.krn
  ...

- gregobase
  - csv
  - gabc
    - 00001.gabc
    - 00002.gabc
    ...

- han
  - han0001.krn
  - han0002.krn
  ...

- natmin
  - natmin001.krn
  - natmin002.krn
  ...

- shanxi
  - shanx001.krn
  - shanx002.krn
  ...
```