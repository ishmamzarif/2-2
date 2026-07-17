import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

INF = 8

def plot(
        signal, 
        title=None, 
        y_range=(-1, 3), 
        figsize = (8, 3),
        x_label='n (Time Index)',
        y_label='x[n]',
        saveTo=None
    ):
    plt.figure(figsize=figsize)
    plt.xticks(np.arange(-INF, INF + 1, 1))
    
    y_range = (y_range[0], max(np.max(signal), y_range[1]) + 1)
    # set y range of 
    plt.ylim(*y_range)
    plt.stem(np.arange(-INF, INF + 1, 1), signal)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    if saveTo is not None:
        plt.savefig(saveTo)
    # plt.show()

def init_signal():
    return np.zeros(2 * INF + 1)


def time_scale_signal(x: np.ndarray, k: int) -> np.ndarray:
    center = INF
    N = len(x)

    y = np.zeros_like(x)

    for i in range(N):
        # convert array index to signal index
        n = i - center
        source = n / k

        if source.is_integer():
            source_index = int(source) + center
            if 0 <= source_index < N:
                y[i] = x[source_index]

    return y

def time_scale_signal_interpolate(x : np.ndarray, k : int) -> np.ndarray:
    # implement this function
    center = INF
    N = len(x)
    y = np.zeros_like(x)

    for i in range(N):
        n = i - center
        source = n / k
        if (source.is_integer()):
            source_index = int(source) + center
            if 0 <= source_index < N:
                y[i] = x[source_index]
        else:
            # interpolate
            left = np.floor(source)
            right = np.ceil(source)

            left_idx = int(left) + center
            right_idx = int(right) + center

            if 0 <= left_idx < N and 0 <= right_idx < N:
                y[i] = (x[left_idx] + x[right_idx]) / 2
    
    return y

def time_scale_signal_interpolate(x: np.ndarray, k: int) -> np.ndarray:
    center = INF
    N = len(x)

    n = np.arange(N) - center
    source = n / k

    left = np.floor(source).astype(int) + center
    right = np.ceil(source).astype(int) + center

    # Prevent out-of-bounds indexing
    left = np.clip(left, 0, N - 1)
    right = np.clip(right, 0, N - 1)

    y = 0.5 * (x[left] + x[right])

    # Zero out samples whose original indices were outside the signal
    valid = (
        (source >= -center) &
        (source <= N - center - 1)
    )
    y[~valid] = 0

    return y


def main():
    img_root = r'online_21\online_1_signals_and_properties\B\B'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root}/x[n].png')
    plot(time_scale_signal(signal, 3), title='x[n/3]', saveTo=f'{img_root}/x[n divided by 3].png')
    plot(time_scale_signal(signal, 1), title='x[n/1]', saveTo=f'{img_root}/x[n divided by 1].png')
    plot(time_scale_signal_interpolate(signal, 3), title='x[n/3] with interpolation', saveTo=f'{img_root}/x[n divided by 3]_with_interpolation.png')
    plot(time_scale_signal_interpolate(signal, 1), title='x[n/1] with interpolation', saveTo=f'{img_root}/x[n divided by 1]_with_interpolation.png')

main()
