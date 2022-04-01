# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""Functions for working with contours"""
import os
import numpy as np
import pandas as pd
import logging
from melodic_contour import stream_to_contour
from phrases import extract_phrases_from_file
from random_segments import extract_random_segments_from_file

def extract_phrase_contours(filepaths: list, num_samples: int = 50,
    contour_id_tmpl: str = '{i:0>3}',
    extractor = extract_phrases_from_file,
    extractor_kwargs: dict = {}) -> pd.DataFrame:
    """Extract all phrase contours from an iterable of files.
    The song ids are extracted from the filenames automatically.
    
    Parameters
    ----------
    filepaths : list
        An iterable of file paths
    num_samples : int, optional
        The number of points at which the pitch is computed, by default 50
    contour_id_tmpl : str, optional
        A template string for the contour ids, for example: `nova{i:0>3}`.
        Defaults to `'{i:0>3}'`
    
    Returns
    -------
    pd.DataFrame
        A Dataframe with song ids, phrase numbers and the contours
    """
    entries = []
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        song_id = os.path.splitext(filename)[0]
        entry = {}
        try:
            phrases = extractor(filepath, **extractor_kwargs)
            phrase_entries = []
            for i, phrase in enumerate(phrases):
                c = stream_to_contour(phrase).interpolate(num_samples=num_samples)
                entry = {
                    'song_id': song_id,
                    'phrase_num': i,
                    'phrase_duration': float(phrase.quarterLength),
                    'phrase_length': len(phrase.flat.notes)
                }
                entry.update({ t: pitch for t, pitch in enumerate(c.pitches) })
                phrase_entries.append(entry)
            
            # Only add phrases if all phrases could be extracted
            entries.extend(phrase_entries)
            logging.info(f'Extracted {len(phrases):0>2} contours from {filename}')
        except Exception as e:
            logging.warn(f'Skipping {song_id}: {e}')
    
    # Package the contours in a DataFrame
    df = pd.DataFrame(entries)
    contour_ids = [contour_id_tmpl.format(i=i) for i in range(1, len(df)+1)]
    df['contour_id'] = contour_ids
    column_order = [
        'contour_id', 
        'song_id', 
        'phrase_num', 
        'phrase_length', 
        'phrase_duration']
    column_order += list(range(0, num_samples))
    df['contour_id'] = contour_ids
    df = df[column_order].set_index('contour_id')
    return df
    
def extract_random_contours(filepaths: list, lam: float,
    num_samples: int = 50, contour_id_tmpl: str = '{i:0>3}', 
    random_seed: float = 0):
    np.random.seed(random_seed)
    return extract_phrase_contours(filepaths=filepaths, num_samples=num_samples,
        contour_id_tmpl=contour_id_tmpl, extractor=extract_random_segments_from_file,
        extractor_kwargs=dict(lam=lam))