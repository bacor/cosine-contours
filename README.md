Cosine Contours
============================================================

This repository contains the data and code for the paper 
'Cosine Contours: A  Multipurpose Representation for Melodies' to be presented at [International Society for Music Information Retrieval conference 
(ISMIR2021)](https://ismir2021.ismir.net/). 

[📖 &nbsp;Paper](documents/paper.pdf) ([supplements](documents/supplements.pdf)) &nbsp; • &nbsp; 🎬 &nbsp;Video &nbsp; • &nbsp; 📜 &nbsp;Poster

----

<img src="figures/teaser/teaser.jpg?raw=true" width="800" 
    title="Three approaches to mode classification in plainchant compared">

Here's a funny observation.
Suppose you take a lot of melodies, and measure the pitch height at, say, 50 points in time, equally spaced between the start and end of the melody.
All your melodies are now sequences of 50 pitches: a 50 dimensional dataset.
The principal components of this dataset will probably look like cosine functions.

In this paper we demonstrate that the principal components of melodies (from motifs and phrases to complete songs) tend to be cosine-shaped.
The same is true for artificial random-walk melodies and this suggests that the cosines are a kind of mathematical artefact.
The culprit turns out to be the covariance matrix.
This roughly approximates a so called Toeplitz matrix, and such matrices (asymptotically) have sinusoidal eigenvectors: our principal components.

Now suppose want to efficiently describe the contour of melodies, capturing as much of the variability in as few dimensions as possible. A principal component projection would be the best choice, but our observations show that we might as well use cosines instead of the principal components, and use a discrete cosine transform. This leads us to propose *cosine contours* which are simply the discrete cosine transforms of the melodies (pitch sequences).
We present three short case studies to illustrate their practical usefulness.

**Reference.**
Bas Cornelissen, Willem Zuidema, and John Ashley Burgoyne, 
“Cosine Contours: A  Multipurpose Representation for Melodies”, in 
*Proc. of the 22st Int. Society for Music Information Retrieval Conf.*, 
Online, 2021

---

Repository structure 
--------------------

- **`data/`** The data analyzed in the paper: melodic material from various datasets. The melodies are all represented as fixed-length pitch sequences (see paper for details), and stored as csv files. The original datasets (which we put in a `datasets/` directory) are not included in this repository, but are available online (or just contact us and we can share those).
- **`notebooks/`** Contains the notebooks used in the experiments and to generate all figures. 
- **`figures/`** Contains all figures presented in the paper and supplements. 

Python setup
------------

You can find the Python version used in `.python-version` and all dependencies 
are listed in `requirements.txt`. If you use `pyenv` and `venv` to manage 
python versions and virtual environments, do the following:

```bash
# Install the right python version
pyenv install | cat .python-version

# Create a virtual environment
python -m venv env

# Activate the environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

License
-------

All code is released under an MIT licence. The figures are released under a
CC-BY 4.0 license.