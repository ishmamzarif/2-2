from math import exp


def rc_response(resistance, capacitance, input_voltage, times):
    """Return capacitor-voltage samples for an RC step input."""
    if resistance <= 0 or capacitance <= 0:
        raise ValueError("R and C must be positive")

    tau = resistance * capacitance
    values = []

    for time in times:
        voltage = input_voltage * (1 - exp(-time / tau))
        values.append(voltage)

    return values


times = [0.0, 0.5, 1.0, 2.0]
print(rc_response(2.0, 0.5, 5.0, times))
