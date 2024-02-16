import matplotlib.pyplot as plt
from display import  SignalDisplay
from loader import SignalLoader
from action import SignalAction, ViewerAction
import os
from functools import partial

class ContinuousViewer():
    def __init__(self,configs,t_start=0,windowsize=15,stepsize=10,title=None,path_save='Figures'):
        self.t_start = t_start
        self.windowsize = windowsize
        self.stepsize = stepsize
        self.title = title
        self.t_end = t_start+windowsize
        self.path_save = path_save

        self.fig, axs = plt.subplots((len(configs)))

        for i,config in enumerate(configs):
            # add viewer base configuration to signal config
            config.__dict__.update(self.__dict__)
            ax = axs if len(configs)==1 else axs[i]
            self.init_signal(self.fig,ax,config)

        self.fig.suptitle(title)
        self.fig.tight_layout()
        handler = ViewerAction(self)
        self.fig.canvas.mpl_connect('key_press_event', lambda event: handler(event.key))

    def init_signal(self,fig,ax,config):
        display = SignalDisplay(ax,config)
        loader = SignalLoader(config.path_signal,config.Fs,config.windowsize,config.dtype)
        action = SignalAction(config,display,loader)
        # Use a default argument to capture the current actionhandler
        fig.canvas.mpl_connect('key_press_event', lambda event, handler=action: handler(event.key))
        # load first image
        action('init')

