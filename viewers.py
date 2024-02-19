import matplotlib.pyplot as plt
from display import  SignalDisplay
from loader import SignalLoader
from action import ActionHandler
from config import ViewerConfig, SignalConfig
from functools import partial

class Viewer():
    def __init__(self,signal_configs,t_start=0,windowsize=15,stepsize=10,
                 title=None,path_save='Figures',timestamps=None):
        self.signal_configs = ([signal_configs] 
                          if not isinstance(signal_configs,list) 
                          else signal_configs)
        
        self.viewer_config = ViewerConfig(t_start,windowsize,stepsize,title,
                                          path_save,timestamps)
        
        self.fig, self.axs = plt.subplots((len(signal_configs)))

        self.displays = []
        self.loaders = []
        for i,signal_config in enumerate(signal_configs):
            # add viewer base configuration to signal confisg
            ax = self.axs if len(signal_configs)==1 else self.axs[i]
            display, loader = self.init_signal(ax,signal_config,self.viewer_config)
            self.displays.append(display); self.loaders.append(loader)
        self.fig.suptitle(title)
        self.fig.tight_layout()
        action_handler = ActionHandler(self.fig,self.viewer_config,
                                       self.signal_configs,self.displays,self.loaders)
        self.fig.canvas.mpl_connect('key_press_event', lambda event: action_handler(event.key))

    def init_signal(self,ax,signal_config,viewer_config):
        display = SignalDisplay(ax,
                                viewer_config.t_start,
                                viewer_config.t_end,
                                signal_config.channel_names,
                                signal_config.y_locations,
                                signal_config.Fs,
                                signal_config.y_pad)
        
        loader = SignalLoader(signal_config.path_signal,
                              signal_config.Fs,
                              signal_config.dtype,
                              signal_config.transforms)
        return display, loader
