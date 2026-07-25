import numpy as np

from signal_lti import DiscreteSignal, LTISystem

def main():
    # Stock Market Prices as a Python List
    # price_list = list(map(int, input("Stock Prices: ").split()))
    # n = int(input("Window size: "))
    # alpha = float(input("Alpha: "))
    # You may use the following input for testing purpose
    price_list = [10,11,12,9,10,13,15,16,17,18]

    n = 3
    alpha = 0.8

    print("hi")

    prices = DiscreteSignal(0, len(price_list) - 1)
    for i in range(len(price_list)):
        prices.set_value_at_time(i, price_list[i])

    h = DiscreteSignal(0, n - 1)
    for i in range(n):
        h.set_value_at_time(i, alpha * ((1 - alpha) ** i))

    system = LTISystem(h)

    # but ekhane full sliding window chai na just for the full overlap

    # Determine the values after performing Exponential Smoothing
    # The length of exsm should be = len(price_list) - n + 1
    exsm = []
    exsm = system.stock_overlap(prices).values

    print("Exponential Smoothing: " + ", ".join(f"{num:.2f}" for num in exsm))
    # Output should be: 11.68, 9.47, 9.82, 12.29, 14.40, 15.62, 16.64, 17.63

if __name__ == "__main__":
    main()