# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2019 Bas Cornelissen
# License: MIT
# -----------------------------------------------------------------------------
import os
import pickle
import gzip
import hashlib
import logging
import textwrap
import numpy as np

# Directory structure
CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CUR_DIR, os.path.pardir))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')

# Experiment setup
GENRES = ['responsory', 'antiphon']
SUBSETS = ['full', 'subset']

def md5checksum(path: str) -> str:
    """Returns an md5 hash of a given file

    Parameters
    ----------
    path : str
        The filepath

    Returns
    -------
    str
        An md5 hash
    """
    hash_md5 = hashlib.md5()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def save_model(object, filename, protocol=pickle.HIGHEST_PROTOCOL):
    """Saves a compressed object to disk"""
    # https://gist.github.com/thearn/5424244
    file = gzip.GzipFile(filename, 'wb')
    file.write(pickle.dumps(object, protocol))
    file.close()

def load_model(filename):
    """Loads a compressed object from disk"""
    file = gzip.GzipFile(filename, 'rb')
    model = pickle.load(file)
    file.close()
    return model

def param_str(params):
    """Helper that turns a param dict in a key=value string"""
    return ', '.join([f'{key}={value}' for key, value in params.items()])

def read_predictions(filename):
    with open(filename, 'r') as handle:
        predictions = [int(i) for i in handle.read().split('\n')]
        return np.asarray(predictions)

def relpath(path, start=ROOT_DIR):
    return os.path.relpath(path, start=start)

def start_experiment_log(name, description, results_dir, **kwargs):
    # Start log
    log_fn = os.path.join(results_dir, f'experiment-{name}.log')
    print(f'Starting log: {relpath(log_fn)}')
    logging.basicConfig(
        filename=log_fn,
        filemode='w',
        format='%(levelname)s %(asctime)s %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
        level=logging.INFO) 
    
    # Print header
    logging.info('*' * 60)
    logging.info(f'* Experiment: {name}')
    if description is not None:
        logging.info('* Description:')
        for line in textwrap.wrap(description, width=50):
            logging.info(f'*   {line}')
    for key, value in kwargs.items():
        if key.endswith('_dir'):
            value = relpath(value)
        logging.info(f'* {key}: {value}')
    logging.info('*' * 60)