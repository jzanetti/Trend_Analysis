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
from process.data import download_data, read_ww
from process.data import read_cfg

from process.rsi import cal_rsi
from process.fft import ts2fft
from process.psd import ts2psd
from process.pca import pca
from process.corr import cal_ww_case_corr
from process.decomp import stl
from process.conf_interval import cal_confidence_interval
from process.basic_stats import cal_basic_stats
from process.vis import plot_rsi, plot_fft, plot_basic_stats, plot_psd, plot_stl, plot_pca, plot_raw, plot_confidence_interval, plot_corr
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
        "--data_src",
        type=str,
        help="Data source (dir) to use [If None, then Github data will be used]",
        required=False,
        default=None
    )

    parser.add_argument(
        "--cfg",
        required=True,
        help="Configuration path",
    )


    return parser.parse_args(
        [
            "--workdir",
            "/tmp/trend_analysis/20240505",
            #"--data_src",
            #"etc/2024-02-09",
            "--cfg",
            "cfg/cfg_weekly.yml",
        ]
    )


def main(workdir: str, data_src: str or None, cfg: str):
    
    cfg = read_cfg(cfg)

    if not exists(workdir):
        makedirs(workdir)

    ww_all = download_data(
        workdir, 
        cfg["start_datetime"], 
        cfg["end_datetime"],
        cfg["resample_method"],
        force=True, 
        data_areas=["national", "regional"], 
        data_src=data_src)

    if cfg["run_corr"]["enable"]:


        hosp_all = download_data(
            workdir, 
            cfg["start_datetime"], 
            cfg["end_datetime"],
            cfg["resample_method"],
            force=True, 
            data_type="hosp", 
            data_areas=["national"], 
            data_src=data_src)

        case_all = download_data(
            workdir, 
            cfg["start_datetime"], 
            cfg["end_datetime"],
            cfg["resample_method"],
            force=True, 
            data_type="cases", 
            data_areas=["national"], 
            data_src=data_src)
        
        corr_hosp = cal_ww_case_corr(
            ww_all, 
            hosp_all, 
            rolling_window=cfg["run_corr"]["window"], 
            if_norm=False, 
            if_gradient=True)

        corr_all = cal_ww_case_corr(
            ww_all, 
            case_all, 
            rolling_window=cfg["run_corr"]["window"], 
            if_norm=False, 
            if_gradient=False)

        plot_corr(
            workdir, 
            corr_hosp, 
            cfg["run_corr"]["window"],
            cfg["resample_method"],
            "national", 
            "hosp")

        plot_corr(
            workdir, 
            corr_all, 
            cfg["run_corr"]["window"],
            cfg["resample_method"], 
            "national", 
            "case")

    if cfg["run_pca"]:
        pca_output = pca(ww_all)
        plot_pca(workdir, pca_output)

    for proc_region in cfg["metrics"]["regions"]:
        proc_ww = read_ww(ww_all, proc_region)

        if cfg["metrics"]["methods"]["raw"]:
            plot_raw(workdir, proc_ww, proc_region, cfg["resample_method"])

        if cfg["metrics"]["methods"]["basic"]["enable"]:

            for proc_window in cfg["metrics"]["methods"]["basic"]["window"]:
                for proc_region in cfg["metrics"]["regions"]:
                    proc_ww_output = cal_basic_stats(
                        proc_ww, window_size=proc_window)
                    plot_basic_stats(
                        workdir, 
                        proc_ww_output, 
                        proc_region, 
                        proc_window,
                        cfg["resample_method"],
                        label_scale=6)

        if cfg["metrics"]["methods"]["rsi"]["enable"]:
            for proc_window in cfg["metrics"]["methods"]["rsi"]["window"]:
                proc_ww_output = cal_rsi(
                    proc_ww,
                    window_length=proc_window)
                plot_rsi(
                    workdir, 
                    proc_ww_output, 
                    proc_region, 
                    proc_window)

        if cfg["metrics"]["methods"]["psd"]["enable"]:
            proc_ww_output = ts2psd(
                proc_ww, sampling_frequency=cfg["metrics"]["methods"]["psd"]["sampling_frequency"])
            plot_psd(
                workdir, 
                proc_ww_output, 
                proc_region, 
                cfg["metrics"]["methods"]["psd"]["sampling_frequency"])

        if cfg["metrics"]["methods"]["fft"]["enable"]:
            proc_ww_output = ts2fft(
                proc_ww, 
                fft_cutoff=cfg["metrics"]["methods"]["fft"]["fft_cutoff"])
            plot_fft(
                workdir, 
                proc_ww_output, 
                proc_region, 
                cfg["metrics"]["methods"]["fft"]["fft_cutoff"])

        if cfg["metrics"]["methods"]["stl"]["enable"]:
            for proc_window in cfg["metrics"]["methods"]["stl"]["window"]:
                proc_ww_output = stl(
                    proc_ww, 
                    proc_window)
                plot_stl(
                    workdir, 
                    proc_ww_output, 
                    proc_region, 
                    proc_window)

        if cfg["metrics"]["methods"]["confidence_interval"]["enable"]:
            for proc_window in cfg["metrics"]["methods"]["confidence_interval"]["window"]:
                proc_ww_output = cal_confidence_interval(
                    proc_ww, cfg["metrics"]["methods"]["confidence_interval"]["n_samples"], 
                    proc_window)
                plot_confidence_interval(
                    workdir, 
                    proc_ww_output, 
                    proc_region, 
                    proc_window)



if __name__ == "__main__":
    args = setup_parser()
    main(args.workdir, args.data_src, args.cfg)