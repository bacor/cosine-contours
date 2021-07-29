# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.fftpack import dct

def cm2inch(*args):
    return list(map(lambda x: x/2.54, args))

def title(text):
    plt.title(text, ha='left', x=0)

def show_num_contours(num_contours, ax, y=1.06):
    plt.text(1, y, f'{num_contours} contours', transform=ax.transAxes, 
         va='bottom', ha='right', size=6, fontstyle='italic', color='0.6')

def normalized_contours(df: pd.DataFrame, normalize=True):
    """Extract a Numpy array of normalized pitch contours from a dataframe
    with pitch contours"""
    start_index = list(df.columns).index('0')
    pitches = df.iloc[:, start_index:].values
    means = pitches.mean(axis=1)
    normalized_pitches = pitches - means[:, np.newaxis]
    if normalize:
        return normalized_pitches
    else:
        return pitches
    
def load_datasets(
    dataset_ids=[
        'erk',
        'boehme',
        'creighton',
        'han', 
        'natmin',
        'shanxi',
        'essen-europe',
        'essen-china',
        'essen-europe-china',
        'liber-antiphons',
        'liber-responsories',
        'liber-alleluias'
    ], 
    include_random=True, dir='../contours', normalize=True):

    dfs = {}
    contours = {}
    for dataset_id in dataset_ids:
        dfs[dataset_id] = pd.read_csv(f'{dir}/{dataset_id}-phrase-contours-1000.csv', index_col=0)
        dfs[f'{dataset_id}-random'] = pd.read_csv(f'{dir}/{dataset_id}-random-contours-1000.csv', index_col=0)
        contours[dataset_id] = normalized_contours(dfs[dataset_id], normalize=normalize)
        contours[f'{dataset_id}-random'] = normalized_contours(dfs[f'{dataset_id}-random'],
                                                               normalize=normalize)
    return dfs, contours



def show_point(coeffs, w=None, h=None, 
               ax=None, 
               scale=.5,
               num_points=20, 
               marker=True,
               line_kws=dict(),
               marker_kws=dict(),
               basis=None):

    if ax == None: ax = plt.gca()
        
    # Determine height/width
    yticks = np.array(ax.get_yticks())
    xticks = np.array(ax.get_xticks())
    min_x = np.min(xticks[1:] - xticks[:-1])
    min_y = np.min(yticks[1:] - yticks[:-1])
    if w is None: w = scale * min_x 
    if h is None: h = scale * min_y 
    
    # Plot a marker
    if marker:
        marker_kwargs = dict(linewidths=0.5, color='0.9', marker='+')
        marker_kwargs.update(marker_kws)
        plt.scatter(coeffs[0], coeffs[1], **marker_kwargs, )
    
    # Plot the basis function
    axins = ax.inset_axes([coeffs[0] - w/2, coeffs[1] - h/2, w, h], 
                          transform=ax.transData)
    line_kwargs = dict(color='.8', linewidth=.5)
    line_kwargs.update(line_kws)
    if basis is None:
        basis = dct(np.eye(num_points), norm='ortho')[:, 1:]
    axins.plot(np.dot(basis[:, :len(coeffs)], coeffs), **line_kwargs)
    
    # Heuristically set the y limits
    ylims = np.array(ax.get_ylim()) / 2
    axins.set_ylim(*ylims)
    axins.axis('off')

def show_grid(xs=None, ys=None, ax=None, **kwargs):
    if ax == None: 
        ax = plt.gca()
    if xs is None: 
        xs = ax.get_xticks()[1:-1]
    if ys is None: 
        ys = ax.get_yticks()[1:-1]
    for x in xs:
        for y in ys:
            show_point([x, y], **kwargs)