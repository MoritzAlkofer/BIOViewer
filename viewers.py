import matplotlib.pyplot as plt
from display import  SignalDisplay
from loader import SignalLoader
from action import ActionHandler
from config import ViewerConfig
import numpy as np


class Viewer():
    def __init__(self,signal_configs,t_start=0,windowsize=15,stepsize=10,
                 title=None,path_save='Figures',timestamps=None,
                 height_ratios='auto',figsize=(7,4)):
        self.signal_configs = ([signal_configs] 
                          if not isinstance(signal_configs,list) 
                          else signal_configs)
        if height_ratios == 'auto':
            height_ratios = [len(signal_config.channel_names)+1 for signal_config in signal_configs]
    
        self.viewer_config = ViewerConfig(t_start,windowsize,stepsize,title,
                                          path_save,timestamps)
        
        self.fig, self.axs = plt.subplots((len(signal_configs)),height_ratios=height_ratios,figsize=figsize)

        self.displays = []
        self.loaders = []
        for i,signal_config in enumerate(signal_configs):
            # add viewer base configuration to signal configs
            ax = self.axs if len(signal_configs)==1 else self.axs[i]
            display, loader = self.init_signal(ax,signal_config,self.viewer_config)
            self.displays.append(display); self.loaders.append(loader)
        self.fig.suptitle(title)
        self.fig.tight_layout()
        action_handler = ActionHandler(self.fig,self.viewer_config,
                                       self.signal_configs,self.displays,self.loaders)
        action_handler('init')
        self.fig.canvas.mpl_connect('key_press_event', lambda event: action_handler(event.key))

    def auto_scale(self,signal):
        percentiles = np.percentile(np.abs(signal), 95, axis=1)
        scale = max(percentiles)
        scale = round_to_first_digit(scale)
        return scale
    
    
    def init_signal(self,ax,signal_config,viewer_config):
        loader = SignalLoader(signal_config.signal,
                              signal_config.Fs,
                              signal_config.transforms)
        signal_config.scale = (self.auto_scale(loader.signal) 
                               if signal_config.scale == 'auto' 
                               else signal_config.scale)
        display = SignalDisplay(ax,viewer_config,signal_config)
        
        return display, loader

def round_to_first_digit(value):
    if value == 0:
        return 0  # Handle the zero case separately to avoid log10(0)
    
    # Calculate the order of magnitude of the absolute value
    order_of_magnitude = np.floor(np.log10(np.abs(value)))
    
    # Calculate the rounding factor
    rounding_factor = 10**order_of_magnitude
    
    # Round the value to the nearest magnitude based on its first significant digit
    rounded_value = np.round(value / rounding_factor) * rounding_factor
    
    return rounded_value
