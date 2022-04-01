# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""Functions for extracting phrases from kern an gabc files using music21."""
import os
from music21 import humdrum
from music21 import converter
import chant21 

class MultipleSpinesException(Exception):
    """An exception raised when encountering multiple spines
    while expecting only 1"""
    pass

def extract_phrases_from_spine(spine):
    """Enxtract the phrases as music21 streams from kern
    Phrases in a humdrum file are delimited by curly brackets.
    All events that do not occur between an opening and closing bracket
    (i.e., are not in a phrase) are ignored. 
    
    Parameters
    ----------
    spine : music21.humdrum.spineParser.KernSpine
        A humdrum spine with the melody
    
    Returns
    -------
    list
        A list of phrases, each represented as a music21.stream.Stream
    """
    phrases = []
    in_phrase = False
    cur_phrase = humdrum.spineParser.KernSpine()
    for event in spine:
        is_phrase_start = event.contents.startswith('{')
        is_phrase_end = event.contents.endswith('}')
        
        if is_phrase_start:
            in_phrase = True

        if in_phrase:
            cur_phrase.append(event)

        if is_phrase_end and in_phrase:
            phrases.append(cur_phrase)
            cur_phrase = humdrum.spineParser.KernSpine()
            in_phrase = False
    
    # Parse spines and return streams
    for phrase in phrases: phrase.parse()
    streams = [phrase.stream.flat for phrase in phrases]
    return streams

def extract_phrases_from_kern_file(filename: str) -> list:
    """Extract all phrases from a kern file.
    Phrases are returned as flattened music21 streams
    
    Parameters
    ----------
    filename : string
        filename of the file
    
    Returns
    -------
    list
        List of phrases as music21.stream.Stream objects
    
    Raises
    ------
    MultipleSpinesException
        Whenever the file contains multiple spines
    """
    song = humdrum.parseFile(filename)
    if len(song.spineCollection.spines) > 1:
        raise MultipleSpinesException
    spine = song.spineCollection.spines[0]
    return extract_phrases_from_spine(spine)

def extract_phrases_from_gabc_file(filename: str) -> list:
    chant = converter.parse(filename)
    return chant.phrases

def extract_phrases_from_file(filepath: str) -> list:
    """Extract phrases from a file to a list of music21 streams.
    Delegates the extration based on the file extension.

    Parameters
    ----------
    filename : string
        filename of the file
    
    Returns
    -------
    list
        List of phrases as music21.stream.Stream objects
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError
    extension = os.path.splitext(filepath)[1]
    if extension == '.krn':
        return extract_phrases_from_kern_file(filepath)
    elif extension == '.gabc':
        return extract_phrases_from_gabc_file(filepath)
    else:
        raise Exception('Unknown file format')
    