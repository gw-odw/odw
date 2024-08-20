"""
Utils
=====

Utility functions to simplify tutorials.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from scipy import stats

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 20


def plot_real_imag_spectrograms(timestamps, frequency, fourier_data, tsft=1800):
    fig, axs = plt.subplots(1, 2, figsize=(16, 10))

    for ax in axs:
        ax.set(xlabel="SFT index", ylabel="Frequency [Hz]")

    time_in_days = (timestamps - timestamps[0]) / tsft

    axs[0].set_title("SFT Real part")
    c = axs[0].pcolormesh(
        time_in_days,
        frequency,
        fourier_data.real,
        norm=colors.CenteredNorm(),
    )
    fig.colorbar(
        c, ax=axs[0], orientation="horizontal", label="Fourier Amplitude"
    )

    axs[1].set_title("SFT Imaginary part")
    c = axs[1].pcolormesh(
        time_in_days,
        frequency,
        fourier_data.imag,
        norm=colors.CenteredNorm(),
    )

    fig.colorbar(
        c, ax=axs[1], orientation="horizontal", label="Fourier Amplitude"
    )

    return fig, axs


def plot_real_imag_spectrograms_with_gaps(
        timestamps, frequency, fourier_data, Tsft):

    # Fill up gaps with Nans
    gap_length = timestamps[1:] - (timestamps[:-1] + Tsft)

    gap_data = [fourier_data[:, 0]]
    gap_timestamps = [timestamps[0]]

    for ind, gap in enumerate(gap_length):
        if gap > 0:
            gap_data.append(np.full_like(fourier_data[:, ind], np.nan + 1j * np.nan))
            gap_timestamps.append(timestamps[ind] + Tsft)

        gap_data.append(fourier_data[:, ind + 1])
        gap_timestamps.append(timestamps[ind + 1])

    return plot_real_imag_spectrograms(
        np.hstack(gap_timestamps), frequency, np.vstack(gap_data).T
    )


def plot_real_imag_histogram(fourier_data, theoretical_stdev=None):

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set(xlabel="SFT value", ylabel="PDF", yscale="log")

    ax.hist(
        fourier_data.real.ravel(),
        density=True,
        bins="auto",
        histtype="step",
        lw=2,
        label="Real part",
    )
    ax.hist(
        fourier_data.imag.ravel(),
        density=True,
        bins="auto",
        histtype="step",
        lw=2,
        label="Imaginary part",
    )

    if theoretical_stdev is not None:
        x = np.linspace(-4 * theoretical_stdev, 4 * theoretical_stdev, 1000)
        y = stats.norm(scale=theoretical_stdev).pdf(x)
        ax.plot(x, y, color="black", ls="--", label="Gaussian distribution")

    ax.legend()

    return fig, ax


def plot_amplitude_phase_spectrograms(timestamps, frequency, fourier_data):
    fig, axs = plt.subplots(1, 2, figsize=(16, 10))

    for ax in axs:
        ax.set(xlabel="SFT index", ylabel="Frequency [Hz]")

    time_in_days = (timestamps - timestamps[0]) / 1800

    axs[0].set_title("SFT absolute value")
    c = axs[0].pcolorfast(
        time_in_days, frequency, np.absolute(fourier_data), norm=colors.Normalize()
    )
    fig.colorbar(c, ax=axs[0], orientation="horizontal", label="Value")

    axs[1].set_title("SFT phase")
    c = axs[1].pcolorfast(
        time_in_days, frequency, np.angle(fourier_data), norm=colors.CenteredNorm()
    )

    fig.colorbar(c, ax=axs[1], orientation="horizontal", label="Value")

    return fig, axs
