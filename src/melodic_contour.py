import numpy as np
import scipy.interpolate

class Contour(object):
    def __init__(self, pitches, times=None, min_pitches=3):
        """A melodic contour is a sequence of pitches in time. These are not 
        notes, but more like the output of a pitch tracking algorithm. The 
        ``times`` attribute contains the time points (in seconds) corresponding
        to the pitches (in continuous MIDI pitch space). 

        Timepoints will be sorted.
        """
        if times is None:
            times = np.arange(len(pitches))

        if not len(times) == len(pitches):
            raise ValueError(
                'The number of time points and pitches should be identical'
            )

        if len(pitches) < min_pitches:
            raise ValueError(
                'A contour should have at least three pitches'
            )

        times = np.asarray(times)
        pitches = np.asarray(pitches)
        order = np.argsort(times)
        self.points = np.asarray([times, pitches]).T[order, :]

    def __len__(self):
        """The number of points in the contour"""
        return self.points.shape[0]
        
    @property
    def resolution(self):
        """Returns the average resolution: number of points per second"""
        return (self.times[-1] - self.times[0]) / len(self)

    @property
    def times(self):
        """An array of timesteps in seconds"""
        return self.points[:, 0]

    @property
    def pitches(self):
        """An array of pitches in pitch space (semitones)"""
        return self.points[:, 1]

    @property
    def positions(self):
        """The relative positions of the points, with 0 being the start of the
        contour and 1 the end.
        
        >>> c = Contour([0, 20, 50, 90, 100], [0, 2, 5, 9, 10])
        >>> c.positions
        array([0. , 0.2, 0.5, 0.9, 1. ])
        """
        return (self.times - self.start) / self.duration

    @property
    def start(self):
        """The starting time"""
        return self.points[0, 0]

    @property
    def end(self):
        """The end time"""
        return self.points[-1, 0]
    
    @property
    def duration(self):
        """Duration of the contour"""
        return self.points[-1, 0] - self.points[0, 0]

    @property
    def initial(self):
        return self.points[0, 1]

    @property
    def final(self):
        return self.points[-1, 1]

    @property
    def lowest(self):
        return self.points[:, 1].min()
    
    @property
    def highest(self):
        return self.points[:, 1].max()

    @property 
    def endpoints(self):
        return self.points[[0, -1], 1]
    
    @property 
    def extremes(self):
        return np.asarray([self.lowest, self.highest])
    
    def interpolate(self, num_samples: int = None, times = None, 
        kind: str = 'previous'):
        """Return an interpolated copy of the contour instance, with
        pitches either at regularly spaced points in time, or at custom 
        timepoints. You can specify the interpolation method using the 
        ``kind`` keyword which is passed to :func:`scipy.interpolate.interp1d`.
        
        Parameters
        ----------
        num_samples : int, optional
            The number of regularly spaced timesteps at which to compute
            the interpolated pitches
        times : iterable, optional
            An iterable of timesteps. Only used if num_samples is not specified.
        kind : str, optional
            The interpolation method; see :func:`scipy.interpolate.interp1d`.
            By default 'previous'

        Returns
        -------
        Contour
            An iterpolated contour
        """
        if times is None and num_samples is None:
            raise ValueError(
                'Either pass an iterable times with timesteps or set the '
                'number of samples num_samples. These cannot both be None.'
            )
        if num_samples is not None:
            times = np.linspace(self.start, self.end, num_samples)
        func = scipy.interpolate.interp1d(self.times, self.pitches, kind=kind)
        pitches = func(times)
        return Contour(pitches, times)


def stream_to_contour(stream, **kwargs):
    """Converts a music21 stream to a contour object. Time measured in quarter
    notes, and one point is added to the contour for every note, except for the 
    last note. To make sure the contour has the right total duration, a final
    point is added at the end of the final note. 

    >>> from music21 import converter
    >>> s = converter.parse('tinyNotation: C D E F')
    >>> c = stream_to_contour(s)
    >>> c.pitches
    array([48., 50., 52., 53., 53.])
    >>> c.times
    array([0., 1., 2., 3., 4.])

    Note that rests are ignored, and rests at the start are skipped:

    >>> s = converter.parse('tinyNotation: r4 C4 r4 D4 r4 r4')
    >>> c = stream_to_contour(s)
    >>> c.times
    array([0., 2., 5.])
    >>> c.pitches
    array([48., 50., 50.])

    Parameters
    ----------
    stream : music21.stream.Stream

    Returns
    -------
    Contour
    """
    duration = stream.quarterLength
    # Important: if you use stream.recurse().notes then the offset is 
    # wrt measure start!
    notes = stream.flat.notes 
    offsets = [float(n.offset) for n in notes]
    pitches = [n.pitch.ps for n in notes]
    
    # Deal with phrases starting with a rest
    if offsets[0] > 0:
        duration = duration - offsets[0]
        offsets = [x - offsets[0] for x in offsets]
    
    # Ensure the final note has the proper duration
    offsets.append(duration)
    pitches.append(pitches[-1])
    return Contour(pitches, offsets, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()