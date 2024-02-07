import numpy as np

class z_scaler():
    def __init__(self):
        pass
    def __call__(self,signal):
                # Calculate mean and standard deviation of the signal
        mean = np.mean(signal)
        std_dev = np.std(signal) + 1e-10

        # Z-scale the signal
        z_scaled_signal = (signal - mean) / std_dev
        return signal