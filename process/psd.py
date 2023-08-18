from scipy.signal import welch

def ts2psd(ww, sampling_frequency=100):

    psd_freq, psd = welch(ww["data"], fs=sampling_frequency, nperseg=256)    
    return {"freq": psd_freq, "psd": psd}