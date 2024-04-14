


def cal_basic_stats(ww, window_size=4):

    #ww = ww[["data"]]

    #monthly_data = ww.resample('M').mean()  
    # Calculate moving window mean
    ww['MovingMean'] = ww['data'].rolling(window=window_size).mean()

    # Calculate moving window median
    ww['MovingMedian'] = ww['data'].rolling(window=window_size).median()

    # Calculate moving window variance
    ww['MovingVariance'] = ww['data'].rolling(window=window_size).var()

    # Calculate moving window standard deviation
    ww['MovingStd'] = ww['data'].rolling(window=window_size).std()

    # Calculate autocorrelation
    ww['Autocorrelation'] = ww['data'].autocorr(lag=window_size)

    return ww