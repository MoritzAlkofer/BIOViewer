import numpy as np
import matplotlib.pyplot as plt
from bioviewer import SignalData
from bioviewer import SignalDisplay
from bioviewer import Viewer
from bioviewer import StateManager
from bioviewer import Signal
    

# init signals
data = np.load('../demos/example.npy')

timestamps = [3,7,12,21] #seconds
markersize = 1 #second
fs = 128
marker = np.full((1,data.shape[1]), np.nan).copy()
for timestamp in timestamps:
    start = int((timestamp-markersize/2)*fs)
    end = int((timestamp+markersize/2)*fs)
    marker[:,start:end]=0

# Example: Assign specific rows

marker = Signal(data=marker,fs=128,show_scale=False,colors='r',linewidth=3,y_ticks=['events'])
signal0 = Signal(data=data,fs=128,scale_factor=220,y_ticks=['a','b','c','d','e','f'],unit='mv',colors='bbbkbr',linewidth=1,show_scale=True)
signal1 = Signal(data=data,fs=128)

# tie everything together in Coordinator
viewer = Viewer(signals = [marker,signal0,signal1],figsize=(14,4),timestamps=timestamps,stepsize=0.5)
