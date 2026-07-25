import numpy as np
import matplotlib.pyplot as plt

# Todo: Define Signal class

from signal_lti import DiscreteSignal
        
class SuperSignal:
    def __init__(self):
        self.components = []

    def add(self, signal: DiscreteSignal, coefficient=1.0):
        self.components.append((coefficient, signal))

    def get_final_signal(self):
        if len(self.components) == 0:
            return Exception("no signals in super signal bro")

        coeff, signal = self.components[0]
        signal = signal.multiply(coeff)
        for i in range(1, len(self.components)):
            coeff, sig = self.components[i]
            sig = sig.multiply(coeff)
            signal = signal.add(sig)

        return signal
        
# Todo: Define LTI class
# pasted from offline and output_super written 
class LTISystem:
    """Discrete-time LTI system described by a finite impulse response."""

    def __init__(self, impulse_response: DiscreteSignal):
        self.h = impulse_response


    def output_range(self, input_signal: DiscreteSignal):
        start = self.h.start_time + input_signal.start_time
        end = self.h.end_time + input_signal.end_time
        return (start, end)
        # raise NotImplementedError("Complete output_range")

    def output_at_time(self, input_signal: DiscreteSignal, n):
        start, end = self.output_range(input_signal)

        if n < start or n > end:
            return 0 

        val = 0
        for k in range(start, end + 1):
            val += input_signal.get_value_at_time(k) * self.h.get_value_at_time(n - k)

        return val

    def output_super(self, super_signal: SuperSignal):
        return self.output(super_signal.get_final_signal())

    def output(self, input_signal: DiscreteSignal):
        start, end = self.output_range(input_signal)
        y = DiscreteSignal(start, end)

        for t in range(start, end + 1):
            y.set_value_at_time(t, self.output_at_time(input_signal, t))

        return y

if __name__ == "__main__":
    INF = 10

    # Component signals
    x1 = DiscreteSignal(-INF, INF)
    x1.set_value_at_time(0, 1)

    x2 = DiscreteSignal(-INF, INF)
    x2.set_value_at_time(2, 1)

    # Todo: Create SuperSignal: x(n) = 2*x1(n) - x2(n)
    super_signal = SuperSignal()
    super_signal.add(x1, 2)
    super_signal.add(x2, -1)

    # Impulse response
    h = DiscreteSignal(-INF, INF)
    h.set_value_at_time(0, 1)
    h.set_value_at_time(1, 0.5)

    system = LTISystem(h)
    

    # Todo: Output using superposition
    system.output_super(super_signal).plot("Super Signal Plot")




