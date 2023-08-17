

from process.data import download_ww
from process.rsi import cal_rsi
from process.fft import ts2fft
from process.vis import plot_rsi, plot_fft
from os import makedirs
from os.path import exists

workdir = "/tmp/trend_analysis"
window_length = 8
fft_cutoff = 0.1

if not exists(workdir):
    makedirs(workdir)

ww = download_ww(workdir)

ww = ts2fft(ww, fft_cutoff=fft_cutoff)

ww = cal_rsi(ww, window_length=window_length)

plot_rsi(ww, window_length)
plot_fft(ww, fft_cutoff)

