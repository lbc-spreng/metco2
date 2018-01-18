import peakdet
import numpy as np
from math import (exp, pi, sqrt)
from scipy.signal import convolve


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

    # account for dropped volumes, extra samples.
    # the values here are specific to the ATTA scan sequence
    response_func = response_func[4:235]
    return convolve(timeseries, response_func)


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
    t = np.arange(0, 32, tr)
    crf = (0.6 * t ** 2.7 * exp(-t / 1.6) -
           16 * (1 / sqrt(2 * pi * 9)) * exp(-0.5 * (((t - 12) ** 2)/9)))
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
    ppg.TR = tr
    return ppg.iHR(step=2)


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
    t = np.arange(0, 50, tr)
    rrf = (0.6 * t ** 2.1 * exp(-t / 1.6) -
           0.0023 * t ** 3.54 * exp(-t / 4.25))
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
    resp.get_peaks(thresh=0.1)
    resp.TR = tr
    return resp.RVT()
