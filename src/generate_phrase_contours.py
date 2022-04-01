# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
# -------------------------------------------------------------------
"""Code for generating the phrase contour datasets: CSV files stored in
the data/ directory.

Usage:  `python generate_data.py dataset_id`
See `python generate_data.py -h` for details.
"""
import os
import glob
import logging
import pandas as pd
import numpy as np
from contours import extract_phrase_contours
from contours import extract_random_contours
from helpers import relpath, md5checksum

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
_DATASETS_DIR = os.path.join(_ROOT_DIR, 'datasets')
_CONTOUR_DIR = os.path.join(_ROOT_DIR, 'data', 'phrase-contours')
_LOGGING_OPTIONS = dict(
    filemode='w',
    format='%(message)s',
    level=logging.INFO)

def generate_contour_data(dataset_id: str, filepaths: list, 
    num_samples: int = 50, dataset_dir: str = _DATASETS_DIR):

    # Extract phrase contours
    phrase_contours = extract_phrase_contours(filepaths, 
        contour_id_tmpl=dataset_id+'-{i:0>5}',
        num_samples=num_samples)

    # Store csv file and log a checksum
    phrases_contours_fn = os.path.join(_CONTOUR_DIR, f'{dataset_id}-phrase-contours.csv')
    phrase_contours.to_csv(phrases_contours_fn)
    md5 = md5checksum(phrases_contours_fn)
    logging.info(f'Stored phrase contours to {relpath(phrases_contours_fn)}')
    logging.info(f'md5 checksum: {md5}')

    # Extract random phrases
    mean_phrase_length = phrase_contours['phrase_length'].mean()
    logging.info(f'Extracting random contours with mean length lamb={mean_phrase_length:.2f}...' )
    random_contours = extract_random_contours(filepaths, 
        lam=mean_phrase_length,
        contour_id_tmpl=dataset_id+'-rand-{i:0>5}',
        num_samples=num_samples)
    mean_random_length = random_contours['phrase_length'].mean()
    logging.info(f'Mean length of random phrases: {mean_random_length:.2f}...' )

    # Store random phrases
    random_contours_fn = os.path.join(_CONTOUR_DIR, f'{dataset_id}-random-contours.csv')
    random_contours.to_csv(random_contours_fn)
    md5 = md5checksum(random_contours_fn)
    logging.info(f'Stored random contours to {relpath(random_contours_fn)}')
    logging.info(f'md5 checksum: {md5}')

def generate_kern_contour_data(dataset_id: str, file_pattern: str, 
    num_samples: int = 50, dataset_dir: str = _DATASETS_DIR):
    """Generate a phrase contour dataset

    The dataset is stored as `data/dataset_id-contours.csv`.
    The first three columns contain metadata: 
    
    - `contour_id`: a unique id for the contour
    - `song_id`: the if of the song from which the phrase was extracted
    - `phrase_num`: the number of the phrase, starting from 0.

    A log of the generation process is stored as `dataset_id.log`. 
    After generating the CSV file, and md5 checksum of the file is 
    computed and logged, allowing you to validate the dataset. 
    
    Parameters
    ----------
    dataset_id : str
        The id of the dataset, which should also be the name of 
        the directory containing the dataset
    file_pattern : str
        A file pattern passed to glob to search for all files in
        the dataset
    num_samples : int, optional
        The number of points at which the pitch is computed, by default 50
    dataset_dir : str, optional
        The directory in which to find the datasets, defaults to `datasets/`
    """
    log_fn = os.path.join(_CONTOUR_DIR, f'{dataset_id}.log')
    logging.basicConfig(filename=log_fn, **_LOGGING_OPTIONS)
    logging.info(f'Generating contour dataset: {dataset_id}')
    
    # Extract all contours
    logging.info('Extracting phrase contours...')
    pattern = os.path.join(dataset_dir, dataset_id, file_pattern)
    filepaths = sorted(glob.glob(pattern, recursive=True))
    generate_contour_data(dataset_id=dataset_id, filepaths=filepaths,
        dataset_dir=dataset_dir, num_samples=num_samples)

def generate_gregobase_contour_data(genre, num_samples: int = 50,
    dataset_dir: str = _DATASETS_DIR):
    """Generate a phrase contour dataset from the GregoBase Corpus.
    We extract all chants of a certain genre in the Liber Usualis.
    Otherwise, the function is identical to `generate_kerndataset`;
    see that function for further details.
    
    Parameters
    ----------
    genre : [type]
        The liturgical genre, can be one of: `antiphons`, `hymns`, `alleluias`,
        `introits`, `communions`, `responsories`, `offertories`, `graduals`, 
        `kyries`, and `tracts`
    num_samples : int, optional
        The number of points at which the pitch is computed, by default 50
    dataset_dir : str, optional
        The directory in which to find the datasets, defaults to `datasets/`
    """    
    genres = {
        'antiphons': 'an',
        'hymns': 'hy',
        'alleluias': 'al',
        'introits': 'in',
        'communions': 'co',
        'responsories': 're',
        'offertories': 'of',
        'graduals': 'gr',
        'kyries': 'ky',
        'tracts': 'tr'
    }
    genre_key = genres[genre]
    dataset_id = f'liber-{genre}'
    log_fn = os.path.join(_CONTOUR_DIR, f'{dataset_id}.log')
    logging.basicConfig(filename=log_fn, **_LOGGING_OPTIONS)
    logging.info(f'Generating contour dataset: {dataset_id}')
    logging.info(f'Contours of {genre} from the Liber Usualis in GregoBaseCorpus v0.3')

    # Load GregoBase Corpus
    csv_dir = os.path.join(_DATASETS_DIR, 'gregobase', 'csv')
    chants = pd.read_csv(os.path.join(csv_dir, 'chants.csv'), index_col=0)
    sources = pd.read_csv(os.path.join(csv_dir, 'sources.csv'), index_col=0)
    chant_sources = pd.read_csv(os.path.join(csv_dir, 'chant_sources.csv'))

    # Select the right subset
    liber_usualis = chant_sources.query('source==3').chant_id
    logging.info(f'Number of chants in the liber usualis: {len(liber_usualis)}')
    right_genre = chants.query(f"office_part == '{genre_key}'").index
    logging.info(f'Number of {genre}: {len(right_genre)}')
    subset = right_genre.intersection(liber_usualis)
    logging.info(f'Number of {genre} in the Liber Usualis: {len(subset)}')

    # Extract all contours
    pattern = os.path.join(_DATASETS_DIR, 'gregobase', 'gabc', '{idx:0>5}.gabc')
    filepaths = sorted([pattern.format(idx=idx) for idx in subset])
    
    generate_contour_data(dataset_id=dataset_id, filepaths=filepaths,
        dataset_dir=dataset_dir, num_samples=num_samples)

def main():
    """CLI for the generation
    Usage:  `python generate_data.py dataset_id`
    """
    import argparse
    parser = argparse.ArgumentParser(description='Extract the contour data from a dataset')
    parser.add_argument('dataset', type=str, help='ID of the dataset to generate,\
        such as `creighton` or `boehme`, or `liber-antiphons`, `liber-kyries`, etc.\
        So either it corresponds to a directory in datasets/, or it is of the form \
        liber-genre.')
    args = parser.parse_args()
    if args.dataset.startswith('liber'):
        genre = args.dataset.split('-')[1]
        generate_gregobase_contour_data(genre, num_samples=100)
    else:
        file_patterns = dict()#creighton='kern/*krn')
        file_pattern = file_patterns.get(args.dataset, '**/*.krn')
        generate_kern_contour_data(args.dataset, file_pattern=file_pattern, num_samples=100)

if __name__ == '__main__':
    np.random.seed(123456)
    main()
    
