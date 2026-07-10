import numpy as np
import matplotlib.pyplot as plt

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


def time_shift_signal(x : np.ndarray, k : int) -> np.ndarray:
    # implement this function
    n = 2 * INF + 1
    y = np.zeros(n)
    for i in range(n):
        if i - k < 0 or i - k >= n:
            y[i] = 0
        else:
            y[i] = x[i - k]

    return y

# def time_scale_signal(x : np.ndarray, k : int) -> np.ndarray:
#     # implement this function
#     N = 2 * INF + 1
#     y = np.zeros(N)

#     origin = INF
#     for i in range(N):
#         idx = i
#         n = idx - INF
#         # y[n] = x[2 * n]
#         # y[n + INF] = x[2 * n + INF]
#         if k * n + INF >= -8 and k * n + INF < N:
#             y[idx] = x[k * n + INF]

#     return y

def time_shift_signal(x : np.ndarray, k : int) -> np.ndarray:
    # implement this function
    y = np.roll(x,k)
    # np.roll(a, shift, axis = None)
    # shifts k places, if overflows it wraps back around 
    # due to the wrapback it will not work here
    if k > 0: # right shift
        y[:k] = 0
    else:     # left shift
        # here k is already negative
        y[k:] = 0
    return y
    

def time_scale_signal(x: np.ndarray, k: int) -> np.ndarray:
    center = 8
    y = np.zeros_like(x)

    # origin
    y[center] = x[center]

    # positive side
    j = center + 1
    for i in range(center + k, len(x), k):
        y[j] = x[i]
        j += 1

    # negative side
    j = center - 1
    for i in range(center - k, -1, -k):
        y[j] = x[i]
        j -= 1

    return y
        

def main():
    img_root_path = r'online_21\online_1_signals_and_properties\A\A'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root_path}/x[n].png')

    plot(time_shift_signal(signal, 2), title='x[n-2]', saveTo=f'{img_root_path}/x[n-2].png')
    
    plot(time_shift_signal(signal, -2), title='x[n+2]', saveTo=f'{img_root_path}/x[n+2].png')
    
    plot(time_shift_signal(signal, 0), title='x[n+0]', saveTo=f'{img_root_path}/x[n+0].png')
    
    plot(time_scale_signal(signal, 2), title='x[2n]', saveTo=f'{img_root_path}/x[2n].png')
    
    plot(time_scale_signal(signal, 1), title='x[1n]', saveTo=f'{img_root_path}/x[1n].png')
    
        

main()




