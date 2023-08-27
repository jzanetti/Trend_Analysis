


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

def cal_confidence_interval(ww, n_samples, window_size): # 1.96 Corresponds to 95% confidence level

    smoothed_data = ww["data"].rolling(window=window_size, min_periods=1).mean()

    resamples_tmp = [resample(smoothed_data) for _ in range(n_samples)]
    resamples = []
    for proc_sample in resamples_tmp:
        resamples.append(proc_sample.sort_index())

    percentiles = np.percentile(resamples, q=[5.0, 95.0], axis=0)  # Transpose the array here
    ww["lower"] = percentiles[0]
    ww["upper"] = percentiles[1]

    return ww

