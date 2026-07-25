import numpy as np
from signal_lti import DiscreteSignal, LTISystem

def main():
    # Stock Market Prices as a Python List
    # price_list = list(map(int, input("Stock Prices: ").split()))
    # n = int(input("Window size: "))

    price_list = [5,-2, 3, 1, 0,-6, 4,-2, 1]
    n = 3

    prices = DiscreteSignal(0, len(price_list) - 1)
    for i in range(len(price_list)):
        prices.set_value_at_time(i, price_list[i])


 
    # Please determine uma and wma.

    # Unweighted Moving Averages as a Python list
    h = DiscreteSignal(0, n - 1)
    for i in range(n):
        h.set_value_at_time(i, 1 / n)
    uma_system = LTISystem(h)

    uma = uma_system.stock_overlap(prices).values

    # Weighted Moving Averages as a Python list
    h = DiscreteSignal(0, n - 1)
    weight_sum = n * (n + 1) / 2
    for i in range(n):
        h.set_value_at_time(i, (n - i) / weight_sum)
    wma_system = LTISystem(h)

    wma = wma_system.stock_overlap(prices).values

    # Print the two moving averages
    print("Unweighted Moving Averages: " + ", ".join(f"{num:.2f}" for num in uma))
    print("Weighted Moving Averages:   " + ", ".join(f"{num:.2f}" for num in wma))


if __name__ == "__main__":
    main()