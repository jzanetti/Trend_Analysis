


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

def cal_confidence_interval(ww, n_samples, window_size): # 1.96 Corresponds to 95% confidence level
    """Calculate confidence interval:

    Approach: Imagine you’re a farmer and you’ve been keeping track of how many apples you pick from 
    your apple tree each day. You’ve noticed that the number can vary quite a bit from day to day, 
    so you decide to calculate a “rolling average” to get a smoother picture of your apple harvest.

    step 1: instead of looking at the apples picked each day, you look at the average 
            number of apples picked over the last 7 days. This gives you a smoother line 
            that’s less affected by one-off bad or good days.
    
    step 2: Now, you want to get an idea of how this average might vary. So, you create many (say, 1000) 
            new sets of data that are similar to your original data but with the days mixed up. 
            This is like imagining 1000 parallel universes where the days happened in a different order.
    
    step 3: Here, you’re just putting these “parallel universes” in order, so the days are back in their original sequence.

    step 4: you look at your 1000 parallel universes and see what the 5th worst and 5th best outcomes were. 
    This gives you a range (from the 5th worst to the 5th best) that you expect the real outcome to fall into 90% of the time.


    Note: the reasons of doing step 2 (resampling) and 3 (sorting) are: To see how much your average cases 
    could vary just due to random chance. 
    - By resampling, you’re creating many possible “parallel universes” of case number that could have happened. 
    - Then, by looking at how much your average case number across these parallel universes, 
       you can get an idea of how much you’d expect it to vary in the future.

    Args:
        ww (_type_): _description_
        n_samples (_type_): _description_
        window_size (_type_): _description_

    Returns:
        _type_: _description_
    """
    smoothed_data = ww["data"].rolling(window=window_size, min_periods=1).mean()

    resamples_tmp = [resample(smoothed_data) for _ in range(n_samples)]
    resamples = []
    for proc_sample in resamples_tmp:
        resamples.append(proc_sample.sort_index())

    percentiles = np.percentile(resamples, q=[5.0, 95.0], axis=0)  # Transpose the array here
    ww["lower"] = percentiles[0]
    ww["upper"] = percentiles[1]

    return ww

