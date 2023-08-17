from numpy import fft

def ts2fft(ww, fft_cutoff=0.3):

    ts_transformed = fft.fft(list(ww["copies_per_day_per_person"]))
    frequencies = fft.fftfreq(len(ww)) 

    # Apply a low-pass filter by setting high-frequency components to zero
    fft_result_filtered = ts_transformed.copy()
    fft_result_filtered[abs(frequencies) > frequencies.max() * fft_cutoff ] = 0

    filtered_data = fft.ifft(fft_result_filtered)

    ww['fft'] = filtered_data.real

    return ww