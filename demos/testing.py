import numpy as np
import matplotlib.pyplot as plt
from bioviewer import SignalData
from bioviewer import SignalDisplay
from bioviewer import Viewer
from bioviewer import StateManager
from bioviewer import Signal
    

# init signals
data = np.load('../demos/example.npy')

data1 = data.copy()
data1[:,:]=0
marker = np.full((data.shape[0],data.shape[1]), 1.).copy()
marker[:,:100] = np.nan
marker[:,150:250] = np.nan

# Example: Assign specific rows

signal0 = Signal(data=data,fs=128,scale_factor=220,y_ticks=['a','b','c','d','e','f'],real_time=True,unit='mv',t_label='Time [h:m:s]',colors='bbbkbr',show_t_ticks=True,linewidth=1,show_scale=True)
signal1 = Signal(data=data,fs=128)

# tie everything together in Coordinator
viewer = Viewer(signals = [signal0,signal1],figsize=(14,4))

