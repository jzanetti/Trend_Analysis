from matplotlib.pyplot import savefig, close, subplots, title, semilogy, xlabel, ylabel, figure, plot, legend, fill_between
from numpy import ones
from os.path import join


def plot_confidence_interval(workdir, ww, region, window):
    # Plotting
    fig, ax1 = subplots()
    ax1.plot(ww.index, ww['data'], label='Noisy Data')
    ax1.fill_between(ww.index, ww["lower"], ww["upper"], alpha=0.2, label='95% CI')
    ax1.legend()
    ax1.set_title(f"raw data with confidence interval, {region} \n Window: {window}")
    fig.tight_layout()
    savefig(join(workdir, f"confidence_interval_{region}.png"))
    close()



def plot_raw(workdir, ww, region):

    fig, ax1 = subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('data', color=color)
    ax1.plot(range(len(ww.index)), ww["data"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Set custom x-axis tick labels with rotation
    xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
    ax1.set_xticks(range(len(xticklabels))[::6])
    ax1.set_xticklabels(xticklabels[::6], rotation=45)
    ax1.set_title(f"raw data, {region}")

    fig.tight_layout()
    savefig(join(workdir, f"raw_{region}.png"))
    close()



def plot_pca(workdir, pca_output):

    for data_type in ["coeff", "coeff_std"]:
        fig, axes = subplots(nrows=2, ncols=2, figsize=(12, 10))
        axes[0, 0].bar(pca_output["region"], pca_output[data_type][0,:])
        axes[0, 0].set_title("PC1")
        axes[0, 0].set_xticklabels(pca_output["region"], rotation=90)

        axes[0, 1].bar(pca_output["region"], pca_output[data_type][1,:])
        axes[0, 1].set_title("PC2")
        axes[0, 1].set_xticklabels(pca_output["region"], rotation=90)


        axes[1, 0].bar(pca_output["region"], pca_output[data_type][2,:])
        axes[1, 0].set_title("PC3")
        axes[1, 0].set_xticklabels(pca_output["region"], rotation=90)

        axes[1, 1].bar(pca_output["region"], pca_output[data_type][3,:])
        axes[1, 1].set_title("PC4")
        axes[1, 1].set_xticklabels(pca_output["region"], rotation=90)

        fig.tight_layout()
        savefig(join(workdir, f"pca_{data_type}.png"))
        close()

def plot_basic_stats(workdir, ww, region, window):
    color = 'tab:blue'
    for key in ["MovingMean", "MovingMedian", "MovingVariance", "MovingStd", "Autocorrelation"]:
        fig, ax1 = subplots()


        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('data', color=color)
        ax1.plot(range(len(ww.index)), ww["data"], color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        # Create a twin Axes sharing the xaxis
        ax2 = ax1.twinx()

        # Plot the second dataset on the right y-axis
        color = 'tab:red'
        ax2.set_ylabel(key, color=color)
        ax2.plot(range(len(ww.index)), ww[key], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Set custom x-axis tick labels with rotation
        xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
        ax1.set_xticks(range(len(xticklabels))[::6])
        ax1.set_xticklabels(xticklabels[::6], rotation=45)
        ax1.set_title(f"{key}, Window: {window} \n {region}")

        fig.tight_layout()
        savefig(join(workdir, f"{key}_{region}.png"))
        close()


def plot_psd(workdir, psd_data, region, sample_frequency):
    fig, _ = subplots()
    semilogy(psd_data["freq"], psd_data["psd"])
    xlabel('Frequency (Hz)')
    ylabel('Power/Frequency (dB/Hz)')
    title(f'Power Spectral Density, Sample frequency: {sample_frequency}\n{region}')
    fig.tight_layout()
    savefig(join(workdir, f"psd_{region}.png"))
    close()


def plot_stl(workdir, stl_data, region, window):
    # Plot the decomposition
    fig, _ = subplots()

    plot(stl_data.trend, label='trend', color='blue')
    title(f'STL Decomposition, Window: {window}')
    plot(stl_data.seasonal, label='seasonal', color='green')
    plot(stl_data.resid, label='resid', color='orange')
    plot(stl_data.observed, label='observed', color='red')
    legend()

    fig.tight_layout()
    savefig(join(workdir, f"stl_{region}.png"))
    close()

def plot_fft(workdir, ww, region, fft_cutoff):

    fig, ax1 = subplots()

    # Plot the first dataset on the left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('data', color=color)
    ax1.plot(range(len(ww.index)), ww["data"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a twin Axes sharing the xaxis
    ax2 = ax1.twinx()

    # Plot the second dataset on the right y-axis
    color = 'tab:red'
    ax2.set_ylabel('fft', color=color)
    ax2.plot(range(len(ww.index)), ww["fft"], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Set custom x-axis tick labels with rotation
    xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
    ax1.set_xticks(range(len(xticklabels))[::6])
    ax1.set_xticklabels(xticklabels[::6], rotation=45)
    ax1.set_title(f"Fast Fourier Transform  \n FFT cutoff: {fft_cutoff * 100.0}%, {region} ")
    
    # xticks(rotation=45)

    fig.tight_layout()
    savefig(join(workdir, f"fft_{region}.png"))
    close()


def plot_rsi(workdir, ww, region, window_length):

    fig, ax1 = subplots()

    # Plot the first dataset on the left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('data', color=color)
    ax1.plot(range(len(ww.index)), ww["data"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a twin Axes sharing the xaxis
    ax2 = ax1.twinx()

    # Plot the second dataset on the right y-axis
    color = 'tab:red'
    ax2.set_ylabel('RSI', color=color)
    ax2.plot(range(len(ww.index)), ww["RSI"], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(range(len(ww.index)), 30.0 * ones(len(ww.index)), color=color, linestyle="--", linewidth=0.5)
    ax2.plot(range(len(ww.index)), 70.0 * ones(len(ww.index)), color=color, linestyle="--", linewidth=0.5)

    # Set custom x-axis tick labels with rotation
    xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
    ax1.set_xticks(range(len(xticklabels))[::6])
    ax1.set_xticklabels(xticklabels[::6], rotation=45)
    ax1.set_title(f"The relative strength index (RSI) \n Window length: {window_length} weeks, {region}")

    # shaded areas
    ax2.fill_between(range(len(ww.index)), 70.0, 100.0, interpolate=True, color='red', alpha=0.15)
    ax2.fill_between(range(len(ww.index)), 0.0, 30.0, interpolate=True, color='green', alpha=0.15)

    fig.tight_layout()
    savefig(join(workdir, f"rsi_{region}.png"))
    close()