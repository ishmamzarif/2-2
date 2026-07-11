import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Time axis
# ----------------------------
T_MIN, T_MAX, N = -4.0, 4.0, 4001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """
    Base signal x(t): sinusoidal signal
    """
    return (
        np.sin(2 * np.pi * 0.5 * t)
        + 0.5 * np.sin(2 * np.pi * 1.5 * t)
    )


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interpolate_signal(
    t_original: np.ndarray,
    x_original: np.ndarray,
    t_query: np.ndarray
) -> np.ndarray:
    """
    Interpolate using average of two neighboring samples.
    """
    n = len(x_original)
    k = t_original[0] / t_query[0]
    t_center_idx = 0
    for i in range(n):
        if (t_original[i] == 0):
            t_center_idx = i
            break

    y = np.zeros_like(x_original)
    for i in range(n):
        time = i - t_center_idx
        # at time, we need to use (time / k) value of x
        time_k = (time / k)
        if (time_k.is_integer()):
            # get corresponding index
            idx = time_k + t_center_idx
            if (0 <= idx and idx < n):
                y[i] = x_original[int(idx)]
        else:
            # interpolate
            left = int(np.floor(time_k)) + t_center_idx
            right = int(np.ceil(time_k)) + t_center_idx
            y[i] = 0.5 * (x_original[left] + x_original[right])
    
    # y = np.interp(
    #     t_query, # where we want values
    #     t_original, # original time values
    #     x_original # original signal values
    # )

    return y



def time_scale(
    t: np.ndarray,
    x: np.ndarray,
    k: int
) -> np.ndarray:
    """
    Time sub-scaling:
        y(t) = x(t / k)
    """
    t_query = t / k
    return interpolate_signal(t, x, t_query)


def plot_pair(t: np.ndarray, x: np.ndarray, y: np.ndarray, title: str):
    """
    Plot graphs.
    """
    pass
    plt.figure()
    plt.plot(t, x, color = "red", label = "x(t)")
    plt.plot(t, y, color = "blue", label = "x(t/k)")
    # plt.stem(t, x, linefmt = "b.")
    # plt.stem(t, y, linefmt = "r-")
    plt.grid(True, alpha = 0.3)
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

# ----------------------------
# Main
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    k = 2   # sub-scaling factor
    y = time_scale(t, x, k)

    plot_pair(
        t,
        x,
        y,
        title=f"Time Sub-scaling: y(t) = x(t / {k})"
    )

    plot_pair(
        t,
        x,
        time_scale(t, x, 4),
        title="Time Sub-scaling: y(t) = x(t / 4)"
    )

    plt.show()


if __name__ == "__main__":
    main()
