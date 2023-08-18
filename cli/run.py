"""
Usage: run --workdir  /tmp/trend_analysis
            --cfg cfg/cfg.yml

Author: Sijin Zhang
Contact: sijin.zhang@esr.cri.nz

Description: 
    This is a wrapper to run the vis
"""

import argparse
from os.path import join, exists
from os import makedirs
from process.data import download_ww, read_ww
from process.data import read_cfg

from process.rsi import cal_rsi
from process.fft import ts2fft
from process.psd import ts2psd
from process.pca import pca
from process.decomp import stl
from process.basic_stats import cal_basic_stats
from process.vis import plot_rsi, plot_fft, plot_basic_stats, plot_psd, plot_stl, plot_pca
def get_example_usage():
    example_text = """example:
        * run --workdir  /tmp/trend_analysis
              --cfg cfg/cfg.yml
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Creating trend analysis",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--workdir",
        type=str,
        help="Working directory",
        required=True,
    )

    parser.add_argument(
        "--cfg",
        required=True,
        help="Configuration path",
    )


    return parser.parse_args(
        [
            "--workdir",
            "/tmp/trend_analysis",
            "--cfg",
            "cfg/cfg.yml",
        ]
    )


def main(workdir: str, cfg: str):
    
    cfg = read_cfg(cfg)

    if not exists(workdir):
        makedirs(workdir)

    ww_all = download_ww(workdir, force=False)

    if cfg["run_pca"]:
        pca_output = pca(ww_all)
        plot_pca(workdir, pca_output)

    for proc_region in cfg["metrics"]["regions"]:
        proc_ww = read_ww(ww_all, proc_region)

        if cfg["metrics"]["methods"]["basic"]["enable"]:
            for proc_region in cfg["metrics"]["regions"]:
                proc_ww = cal_basic_stats(proc_ww, window_size=cfg["metrics"]["methods"]["basic"]["window"])
                plot_basic_stats(workdir, proc_ww, proc_region, cfg["metrics"]["methods"]["basic"]["window"])

        if cfg["metrics"]["methods"]["rsi"]["enable"]:
            proc_ww = cal_rsi(proc_ww, window_length=cfg["metrics"]["methods"]["rsi"]["window"])
            plot_rsi(workdir, proc_ww, proc_region, cfg["metrics"]["methods"]["rsi"]["window"])

        if cfg["metrics"]["methods"]["psd"]["enable"]:
            proc_psd = ts2psd(proc_ww, sampling_frequency=cfg["metrics"]["methods"]["psd"]["sampling_frequency"])
            plot_psd(workdir, proc_psd, proc_region, cfg["metrics"]["methods"]["psd"]["sampling_frequency"])

        if cfg["metrics"]["methods"]["fft"]["enable"]:
            proc_ww = ts2fft(proc_ww, fft_cutoff=cfg["metrics"]["methods"]["fft"]["fft_cutoff"])
            plot_fft(workdir, proc_ww, proc_region, cfg["metrics"]["methods"]["fft"]["fft_cutoff"])

        if cfg["metrics"]["methods"]["stl"]["enable"]:
            stl_output = stl(proc_ww, cfg["metrics"]["methods"]["stl"]["window"])
            plot_stl(workdir, stl_output, proc_region, cfg["metrics"]["methods"]["stl"]["window"])


if __name__ == "__main__":
    args = setup_parser()
    main(args.workdir, args.cfg)