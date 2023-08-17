from matplotlib.pyplot import savefig, close, subplots, title
from numpy import ones



def plot_fft(ww, fft_cutoff):

    fig, ax1 = subplots()

    # Plot the first dataset on the left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('copies_per_day_per_person', color=color)
    ax1.plot(ww.index, ww["copies_per_day_per_person"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a twin Axes sharing the xaxis
    ax2 = ax1.twinx()

    # Plot the second dataset on the right y-axis
    color = 'tab:red'
    ax2.set_ylabel('fft', color=color)
    ax2.plot(ww.index, ww["fft"], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Set custom x-axis tick labels with rotation
    xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
    ax1.set_xticklabels(xticklabels, rotation=45)
    ax1.set_title(f"Fast Fourier Transform  \n FFT cutoff: {fft_cutoff * 100.0}% ")
    
    # xticks(rotation=45)

    fig.tight_layout()
    savefig("fft.png")
    close()


def plot_rsi(ww, window_length):

    fig, ax1 = subplots()

    # Plot the first dataset on the left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('copies_per_day_per_person', color=color)
    ax1.plot(ww.index, ww["copies_per_day_per_person"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a twin Axes sharing the xaxis
    ax2 = ax1.twinx()

    # Plot the second dataset on the right y-axis
    color = 'tab:red'
    ax2.set_ylabel('RSI', color=color)
    ax2.plot(ww.index, ww["RSI"], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(ww.index, 30.0 * ones(len(ww.index)), color=color, linestyle="--", linewidth=0.5)
    ax2.plot(ww.index, 70.0 * ones(len(ww.index)), color=color, linestyle="--", linewidth=0.5)

    # Set custom x-axis tick labels with rotation
    xticklabels = ww.index.strftime('%Y-%m-%d')  # Format the dates as desired
    ax1.set_xticklabels(xticklabels, rotation=45)
    ax1.set_title(f"The relative strength index (RSI) \n Window length: {window_length} weeks")
    
    # xticks(rotation=45)

    fig.tight_layout()
    savefig("rsi.png")
    close()