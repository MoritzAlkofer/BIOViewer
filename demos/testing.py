import numpy as np
import matplotlib.pyplot as plt
from bioviewer import SignalData
from bioviewer import SignalDisplay
from bioviewer import Viewer
from bioviewer import StateManager
from bioviewer import Signal
    

# init signals
data = np.load('../demos/example.npy')

signal0 = Signal(data=data,y_ticks=[1,2,3,4,5,6])
signal1 = Signal(data=data,y_ticks=[1,2,3,4,5,6])



# tie everything together in Coordinator
viewer = Viewer(signals = [signal0,signal1])

# make coordinator interactive
viewer.fig.canvas.mpl_connect('key_press_event', lambda event: viewer.update(event.key))
plt.ion()

# show
plt.show(block=True)

