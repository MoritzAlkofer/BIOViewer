import matplotlib.pyplot as plt
from BIOViewer.display import  SignalDisplay
from BIOViewer.loader import SignalLoader
from BIOViewer.config import ViewerConfig
import numpy as np


class EventViewer():
    def __init__(self,signal_configs,t_start=0,windowsize=15,stepsize=10,
                 title=None,path_save='Figures',timestamps=None,
                 height_ratios='auto',figsize=(7,4)):

        # init configs        
        self.signal_configs = _validate_property(signal_configs)
        self.viewer_config = ViewerConfig(t_start,windowsize,stepsize,title,path_save,timestamps)

        # build viewer, displays and loaders
        height_ratios = self._init_height_ratios(height_ratios,signal_configs)
        self.fig, self.axs = plt.subplots((len(signal_configs)),height_ratios=height_ratios,figsize=figsize)
        self.displays, self.loaders = self._build_displays_and_loaders(self.axs,signal_configs,self.viewer_config)

        # add action, init viewer and connect 
        action_handler = ActionHandler(self.fig,self.viewer_config,self.signal_configs,self.displays,self.loaders)
        action_handler('init')
        self.fig.canvas.mpl_connect('key_press_event', lambda event: action_handler(event.key))
        # display
        plt.ion()
        plt.show(block=True)

    def _init_height_ratios(self,height_ratios,signal_configs):
        if height_ratios == 'auto':
            height_ratios = [len(signal_config.channel_names)+1 for signal_config in signal_configs]
        return height_ratios
    
    def _build_displays_and_loaders(self,axs,signal_configs,viewer_config):    
        displays = []
        loaders = []
        for i,signal_config in enumerate(signal_configs):
            # add viewer base configuration to signal configs
            ax = axs if len(signal_configs)==1 else axs[i]
            display, loader = self.init_signal(ax,signal_config,viewer_config)
            displays.append(display); loaders.append(loader)
        return displays,loaders

    def init_signal(self,ax,signal_config,viewer_config):
        display = SignalDisplay(ax,viewer_config,signal_config)        
        return display, signal_config.loader

import datetime
from functools import partial
import os

class ActionHandler():
    def __init__(self,fig,viewer_config,signal_configs,displays,loaders):
         self.actions = {
            'z': lambda: self.save_figure(fig,viewer_config.path_save,viewer_config.title,viewer_config.t_start),
            'right': partial(self.change_sample, 'right', fig,
                             viewer_config,signal_configs,displays,loaders),
            'left': partial(self.change_sample, 'left', fig,
                             viewer_config,signal_configs,displays,loaders),                             
            'init': partial(self.init_viewer, fig,
                             viewer_config,signal_configs,displays,loaders)
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)
    
    def update(self,fig,viewer_config,signal_configs,displays,loaders):
        sample_idx = viewer_config.sample_idx
        for signal_config,display,loader in zip(signal_configs,displays,loaders):
            data = loader.load_signal(signal_config.path_signals[sample_idx])
            for transform in signal_config.transforms:
                data = transform(data)
            data = (1/signal_config.scale)*data
            display.plot_data(data,signal_config.y_locations)
        if len(viewer_config.title)!=0:
            fig.suptitle(viewer_config.title[sample_idx])
            
    def change_sample(self,direction,fig,viewer_config,signal_configs,displays,loaders):
        if direction =='right':
            viewer_config.sample_idx +=1
        if direction =='left':
            viewer_config.sample_idx -=1
        self.update(fig,viewer_config,signal_configs,displays,loaders)

    def init_viewer(self,fig,viewer_config,signal_configs,displays,loaders):
        self.update(fig,viewer_config,signal_configs,displays,loaders)
        fig.tight_layout()

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

def seconds_to_hms(seconds):
        # Construct a datetime object with a base date
        base_date = datetime.datetime(1900, 1, 1)
        # Add the timedelta to the base date
        result_datetime = base_date + datetime.timedelta(seconds=seconds)
        # Format the result as hours:minutes:seconds
        formatted_time = result_datetime.strftime('%H:%M:%S')

        return formatted_time

def _validate_property(property):
    """Ensure signal_configs is a list."""
    if property == None:
        return []
    if not isinstance(property, list):
        return [property]
    return property