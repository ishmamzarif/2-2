import numpy as np
import math
import cmath

import bigmul
import transforms

# def fft(a):
#     pass

# def ifft(a):
    # pass


# def weighted_polynomial_multiply(P, Q, W):
    #implement
    # pass
    

if __name__ == "__main__":
    P = [1, 3, 2, 6, 7]
    Q = [4,1]
    W = [3, 2, 1, 5, 6]

    P_new = np.array(P) * np.array(W)
    Q_new = Q

    n = np.size(P)
    q = np.size(Q)

    N = transforms.next_power_of_two(n + q - 1)

    P_padded = np.zeros(N, dtype=np.int64)
    Q_padded = np.zeros(N, dtype=np.int64)
    P_padded[:n] = P_new
    Q_padded[:q] = Q_new

    engine = transforms.FFTTransformer()
    ans = np.rint(engine.inverse( engine.transform(P_padded) * engine.transform(Q_padded) ))
    ans = np.real(ans)
    # jehetu coeffs descending order e deowa chilo, i have to reverse them here
    ans = ans[:n + q - 1][::-1]
    print("Result:", ans)