import matplotlib.pyplot as plt
from src import ContinuousConfig, ContinuousViewer, activate_viewers
from transforms import z_scaler

path_signal = '/home/moritz/Desktop/programming/BIOViewer/BIOViewer/P40-2-4.hf5'
dtype = 'h5'
channels = ['abd','flow_reductions']
y_locations = [0, 10]
Fq_signal = 10
title = 'Test'

fig,axs = plt.subplots(2)

config0 = ContinuousConfig(path_signal,Fq_signal,channels,y_locations,title=title)
viewer0 = ContinuousViewer(axs[0],config0)
config1 = ContinuousConfig(path_signal,Fq_signal,channels,y_locations,title=title)
viewer1 = ContinuousViewer(axs[1],config1)
activate_viewers(fig,viewer0,viewer1)
fig.tight_layout()
plt.show()
