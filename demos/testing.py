import numpy as np
import matplotlib.pyplot as plt
from bioviewer import Signal
from bioviewer import Display
from bioviewer import Viewer
from bioviewer import StateManager
    
# init signals
data = np.load('../demos/example.npy')

signal0 = Signal(data,Fs=128,scale_factor=100)
signal1 = Signal(data,Fs=128,scale_factor=100)

# init statemanager
statemanager = StateManager()

# init figure
fig,axs = plt.subplots(2,1,figsize=(10,4))

# init displays

display0 = Display(axs[0],n_channels=signal0.data.shape[0],y_ticks=[1,2,3,4,5,6])
display0.init_display(statemanager.t_start,statemanager.windowsize,Fs=signal0.fs)

display1 = Display(axs[1],n_channels=signal1.data.shape[0],y_ticks=[1,2,3,4,5,6])
display1.init_display(statemanager.t_start,statemanager.windowsize,Fs=signal1.fs)


# tie everything together in Coordinator
coordinator = Coordinator(signals = [signal0,signal1],displays=[display0,display1],statemanager=statemanager)

# make coordinator interactive
fig.canvas.mpl_connect('key_press_event', lambda event: coordinator.update(event.key))
plt.ion()

# show
plt.show(block=True)

