import numpy as np
import matplotlib.pyplot as plt

# Todo: Define Signal class

# Todo: Define LTI class

from signal_lti import DiscreteSignal, LTISystem

# h_combined = h3 (h1 + h2)
#            = h3 * (h1 + h2)

if __name__ == "__main__":
    INF = 10

    x = DiscreteSignal(-INF, INF)
    x.set_value_at_time(2, -1)
    x.plot("Input x(n)")

    h1 = DiscreteSignal(-INF, INF)
    h1.set_value_at_time(0, 1)

    h2 = DiscreteSignal(-INF, INF)
    h2.set_value_at_time(1, 0.5)

    h3 = DiscreteSignal(-INF, INF)
    h3.set_value_at_time(0, 1)
    h3.set_value_at_time(1, 1)

    sys1 = LTISystem(h1)
    sys2 = LTISystem(h2)
    sys3 = LTISystem(h3)
    
    x1 = sys1.output(x)
    x2 = sys2.output(x)
    y_final_1 = sys3.output(x1.add(x2))
    # Todo: Determine output block by block

    y_final_1.plot("Output via block-by-block system")

    # Todo: Determine h_combined
    h_combined = sys3.output(h1.add(h2))
    sys_combined = LTISystem(h_combined)

    y_final_2 = sys_combined.output(x)
    y_final_2.plot("Output via combined impulse response")

    print("Outputs are equal:",
          np.allclose(y_final_1.values, y_final_2.values))
