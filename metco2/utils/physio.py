import peakdet
import numpy as np
from math import (pi, sqrt)
from scipy.signal import convolve

# NOTE: the argument values are specific to the ATTA scan sequence


def convolve_ts(physio_f):
    """
    Calculates and convolves the low-frequency physio timeseries
    (either instantaneous heart-rate [iHR] or respiratory-volume-
    per-time [RVT]) with the appropriate response function.

    Inputs
    ------
    physio_f: file
        A plain-text file containing the sampled physio time series.

    Outputs
    -------
    array-like
        The sampled, low-frequency physiology confound convolved
        with the correct response function.
    """
    if 'ECG' in physio_f:
        timeseries = i_hr(physio_f)
        response_func = crf()
    elif 'Resp' in physio_f:
        timeseries = rvt(physio_f)
        response_func = rrf()
    else:
        print('WARNING: Physio format not understood! \n'
              'No confound timeseries will be generated.')
        return
    return convolve(timeseries, response_func, mode='same')


def crf(tr=2.0):
    """
    Calculate the cardiac response function using the definition
    supplied in Chang and Glover, 2009, NeuroImage, Appendix A.

    Inputs
    ------
    tr: float
        (Optional) sampling frequency of the MRI time series,
        defaults to 2.0 seconds.

    Outputs
    -------
    crf: array-like
        cardiac or "heart" response function
    """
    def _crf(t):
        rf = (0.6 * t ** 2.7 * np.exp(-t / 1.6) -
              16 * (1 / sqrt(2 * pi * 9)) * np.exp(-0.5 * (((t - 12) ** 2)/9)))
        return rf

    t = np.arange(0, 32, tr)
    crf = _crf(t)
    crf = crf / max(abs(crf))
    return crf


def i_hr(physio_f, samplerate=40, tr=2.0):
    """
    Calculates the instantaneous heart rate (iHR)
    from a raw PPG time series.

    Inputs
    ------
    physio_f: file
        A plain-text file containing the PPG time series.
    samplerate: int
        (Optional) sampling frequency of the PPG time series.
        Defaults to 40Hz.
    TR: float
        (Optional) sampling frequency of the MRI time series,
        for binning the instantaneous heart rate time series.
        Defaults to 2.0 seconds.

    Outputs
    -------
    array-like
        instantaneous heart rate (iHR) time series
    """
    datafile = physio_f
    ppg = peakdet.PPG(datafile, samplerate)
    ppg.get_peaks()
    return ppg.iHR(step=2, start=8.0, end=438.0, TR=tr)


def rrf(tr=2.0):
    """
    Calculate the respiratory response function using the definition
    supplied in Chang and Glover, 2009, NeuroImage, Appendix A.

    Inputs
    ------
    tr: float
        (Optional) sampling frequency of the MRI time series,
        defaults to 2.0 seconds.

    Outputs
    -------
    rrf: array-like
        respiratory response function
    """
    def _rrf(t):
        rf = (0.6 * t ** 2.1 * np.exp(-t / 1.6) -
              0.0023 * t ** 3.54 * np.exp(-t / 4.25))
        return rf

    t = np.arange(0, 50, tr)
    rrf = _rrf(t)
    rrf = rrf / max(abs(rrf))
    return rrf


def rvt(physio_f, samplerate=40, tr=2.0):
    """
    Calculates the respiratory-volume-per-time (RVT)
     from a raw pneumatic belt time series.

    Inputs
    ------
    physio_f: file
        A plain-text file containing the RESP time series.
    samplerate: int
        (Optional) sampling frequency of the RESP time series.
        Defaults to 40Hz.
    TR: float
        (Optional) sampling frequency of the MRI time series,
        for binning the instantaneous heart rate time series.
        Defaults to 2.0 seconds.

    Outputs
    -------
    array-like
        respiratory-volume-per-time (RVT) time series
    """
    datafile = physio_f
    resp = peakdet.RESP(datafile, samplerate)
    resp.get_peaks(thresh=0.2)
    return resp.RVT(start=8.0, end=438.0, TR=tr)
