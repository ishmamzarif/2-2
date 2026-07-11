import numpy as np


def interpolate_signal(
    t_original: np.ndarray,
    x_original: np.ndarray,
    t_query: np.ndarray
) -> np.ndarray:
    """
    Interpolate x at t_query, given known samples (t_original, x_original).
    Missing values = average of nearest left and right known samples.
    Exact matches return the known sample directly.
    """
    order = np.argsort(t_original)
    t_sorted = t_original[order]
    x_sorted = x_original[order]
    n = len(t_sorted)

    # Insertion index: t_sorted[idx-1] <= t_query < t_sorted[idx] (roughly)
    idx = np.searchsorted(t_sorted, t_query, side='left')
    idx_clipped = np.clip(idx, 0, n - 1)

    # Exact match: query lands precisely on a known sample
    exact_match = (idx < n) & np.isclose(t_sorted[idx_clipped], t_query)

    left_idx = np.clip(idx - 1, 0, n - 1)
    right_idx = np.clip(idx, 0, n - 1)

    left_val = x_sorted[left_idx]
    right_val = x_sorted[right_idx]

    averaged = 0.5 * (left_val + right_val)
    result = np.where(exact_match, x_sorted[idx_clipped], averaged)

    # Queries outside the known range are undefined -> NaN (dropped when plotting)
    out_of_range = (t_query < t_sorted[0]) | (t_query > t_sorted[-1])
    result = np.where(out_of_range, np.nan, result)

    return result