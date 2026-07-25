from signal_lti import DiscreteSignal, LTISystem

# Input for first polynomial
d1 = int(input("Degree of the first polynomial: "))
poly1 = list(map(int, input("Coefficients: ").split()))


# Input for second polynomial
d2 = int(input("Degree of the second polynomial: "))
poly2 = list(map(int, input("Coefficients: ").split()))


# Multiply the polynomials using Discrete-Time Convolution
# index k of the signal = exponent of x^k, so reverse the coefficient order
x1 = DiscreteSignal(0, d1)
for k in range(d1 + 1):
    x1.set_value_at_time(k, poly1[d1 - k])

x2 = DiscreteSignal(0, d2)
for k in range(d2 + 1):
    x2.set_value_at_time(k, poly2[d2 - k])

system = LTISystem(x2)
y = system.output(x1)

degree = d1 + d2
coefficients = [round(y.get_value_at_time(k)) for k in range(degree, -1, -1)]

# Print the result
print("Degree of the Polynomial:", degree)
print("Coefficients:", " ".join(map(str, coefficients)))