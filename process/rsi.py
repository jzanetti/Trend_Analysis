


def cal_rsi(ww, window_length = 14):
    # Calculate daily price changes
    ww["diff"] = ww["copies_per_day_per_person"].diff()

    # Calculate average gain and average loss
    ww['gain'] = ww["diff"].apply(lambda x: x if x > 0 else 0).rolling(window=window_length).mean()
    ww['loss'] = ww["diff"].apply(lambda x: abs(x) if x < 0 else 0).rolling(window=window_length).mean()

    # Calculate relative strength (RS) and relative strength index (RSI)
    ww['RS'] = ww['gain'] / ww['loss']
    ww['RSI'] = 100 - (100 / (1 + ww['RS']))

    return ww
