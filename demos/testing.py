import numpy as np
import matplotlib.pyplot as plt
from bioviewer import SignalData, SignalDisplay, Signal, Viewer

# Example: Load signal data from a .npy file
data = np.load('../demos/example.npy')  # Load data for visualization

# Parameters for signal markers and visualization
timestamps = [3, 7, 12, 21]  # Timepoints to mark on the signal
marker_size = 1  # Duration of marker (in seconds)
fs = 128  # Sampling frequency (Hz)

# Create a marker signal
marker = np.full((1, data.shape[1]), np.nan).copy()
for timestamp in timestamps:
    start = int(round(timestamp * fs))
    end = int(round((timestamp + marker_size) * fs))
    marker[:, start:end] = 0  # Add marker at the specified timestamps

# Create Signal instances
signal0 = Signal(data=data, fs=fs, scale_factor='auto', y_ticks=['a', 'b', 'c', 'd', 'e', 'f'], 
                 unit='mV', colors='bbbkbr', linewidth=1, show_scale=True)

signal1 = Signal(data=data, fs=fs)

marker_signal = Signal(data=marker, fs=fs, show_scale=False, colors='r', linewidth=3, y_ticks=['events'])

# Combine signals in a Viewer
viewer = Viewer(
    signals=[marker_signal, signal0, signal1],  # Signals to visualize
    figsize=(14, 4),  # Size of the plot
    timestamps=timestamps,  # List of timestamps for navigation
    stepsize=0.1  # Step size for scrolling through the signal
)

# Instructions for the user
print("Viewer Initialized! Use the following keys for navigation:")
print("Right arrow: Scroll right (forward in time)")
print("Left arrow: Scroll left (back in time)")
print("n: Go to the next timestamp")
print("b: Go to the previous timestamp")
print("z: Save the current figure as an image")

# Display the Viewer
plt.show(block=True)  # Display the interactive plot
