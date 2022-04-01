# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
from music21 import converter
from music21 import stream
import numpy as np

def positive_poisson_sample(lam: float) -> int:
    """Return a sample from a shifted Poisson distribution
    where all weight is on the positive integers 1, 2, 3, ...
    So if `x` is a sample from this distribution, then (x-1) is
    Poisson(mu-1)-distributed.
    
    Parameters
    ----------
    lam : float
        The Poisson parameter
    
    Returns
    -------
    int
        A sample from the distribution
    """
    return 1 + np.random.poisson(lam=lam - 1)

def poisson_segmentation(iterable: list, lam: float, 
    omit_first_and_last: bool = True) -> list:
    """Segment an iterable in segments whose length is approximately
    Poisson-distributed. Note that the first and final segment are always
    discarded. Also, the segment lengths cannot be zero, so the
    lengths actually follow a shifted poisson distribution.
    
    Parameters
    ----------
    iterable : list
        The iterable to segment
    lam : float
        The parameter of the poisson
    omit_first_and_last : bool
        Omit the first and final segment? Defaults to true
    
    Returns
    -------
    list
        A list of segments
    """
    if lam < 1: raise ValueError('Lambda should be > 1.')
    segments = []
    last_idx = positive_poisson_sample(lam) if omit_first_and_last else 0
    segment_length = positive_poisson_sample(lam)
    while last_idx + segment_length < len(iterable):
        segment = iterable[last_idx:last_idx+segment_length]
        segments.append(segment)
        last_idx += segment_length
        segment_length = positive_poisson_sample(lam)

    if not omit_first_and_last and last_idx < len(iterable):
        segments.append(iterable[last_idx:])
    
    return segments

def extract_random_segments_from_file(filepath: str, lam: float,
    omit_first_and_last: bool = True) -> list:
    """Extract random segments of notes with a Poisson length-distribution
    from a file.

    Parameters
    ----------
    filename : string
        filename of the file
    lam : float
        The Poisson parameter: average length
    omit_first_and_last : bool
        Omit the first and last segment? Default to True
    
    Returns
    -------
    list
        List of random segments as music21.stream.Stream objects
    """
    s = converter.parse(filepath)
    elements = s.flat.notesAndRests 
    segments = poisson_segmentation(elements, lam=lam, 
        omit_first_and_last=omit_first_and_last)
    
    # Turn the segments into streams and return
    streams = []
    for segment in segments:
        segment_stream = stream.Stream()
        for el in segment:
            segment_stream.append(el)
        streams.append(segment_stream)
    return streams
    