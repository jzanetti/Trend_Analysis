from numpy import fft

def ts2fft(ww, fft_cutoff=0.3):

    ts_transformed = fft.fft(list(ww["data"]))
    frequencies = fft.fftfreq(len(ww)) 

    # Apply a low-pass filter by setting high-frequency components to zero
    fft_result_filtered = ts_transformed.copy()
    fft_result_filtered[abs(frequencies) > frequencies.max() * fft_cutoff ] = 0

    filtered_data = fft.ifft(fft_result_filtered)

    filtered_data = filtered_data.real

    # remove negative data
    filtered_data_min = filtered_data.min()

    if filtered_data_min < 0:
        filtered_data += abs(filtered_data_min) + 0.1
    
    sf = filtered_data.mean() / ww["data"].mean()

    filtered_data /= sf

    ww['fft'] = filtered_data
    return ww