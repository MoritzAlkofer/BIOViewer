import numpy as np
import matplotlib.pyplot as plt
from bioviewer import SignalData
from bioviewer import SignalDisplay
from bioviewer import Viewer
from bioviewer import StateManager
from bioviewer import Signal
    

# init signals
data = np.load('../demos/example.npy')
data[:,128:2*128]=np.nan

signal0 = Signal(data=data,colors='bbbkrk',linewidth=1.3)
signal1 = Signal(data=data)



# tie everything together in Coordinator
viewer = Viewer(signals = [signal0,signal1])

