from statsmodels.tsa.seasonal import STL



def stl(ww, window):
    # Seasonal Decomposition of Time Series
    stl_model = STL(ww["data"], seasonal=window)
    stl_output = stl_model.fit()
    return stl_output