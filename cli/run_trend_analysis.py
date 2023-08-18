

from process.data import download_ww, read_ww
from process.rsi import cal_rsi
from process.fft import ts2fft
from process.psd import ts2psd
from process.decomp import stl
from process.basic_stats import cal_basic_stats
from process.vis import plot_rsi, plot_fft, plot_basic_stats, plot_psd, plot_stl
from os import makedirs
from os.path import exists

workdir = "/tmp/trend_analysis"
tasks = {
    "basic_stats": {"enable": True, "window": 20, "regions": ["Auckland"]},
    "psd": {"enable": False, "sampling_frequency": 100, "regions": ["nation"]},
    "stl": {"enable": False, "window": 7, "regions": ["nation"]},
    "rsi": False,
    "fft": False
}
window_length = 8
fft_cutoff = 0.5

if not exists(workdir):
    makedirs(workdir)

ww_all = download_ww(workdir)

if tasks["basic_stats"]["enable"]:
    for proc_region in tasks["basic_stats"]["regions"]:
        proc_ww = read_ww(ww_all, proc_region)
        proc_ww = cal_basic_stats(proc_ww, window_size=tasks["basic_stats"]["window"])
        plot_basic_stats(proc_ww, tasks["basic_stats"]["window"])

if tasks["fft"]:
    ww = ts2fft(ww, fft_cutoff=fft_cutoff)
    plot_fft(ww, fft_cutoff)

if tasks["psd"]["enable"]:
    psd = ts2psd(ww, sampling_frequency=tasks["psd"]["sampling_frequency"])
    plot_psd(psd, tasks["psd"]["sampling_frequency"])

if tasks["rsi"]:
    ww = cal_rsi(ww, window_length=window_length)
    plot_rsi(ww, window_length)

if tasks["stl"]["enable"]:
    stl_output = stl(ww, tasks["stl"]["window"])
    plot_stl(stl_output, tasks["stl"]["window"])
