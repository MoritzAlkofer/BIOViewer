import matplotlib.pyplot as plt
from BIOViewer.display import  SignalDisplay
from BIOViewer.loader import SignalLoader
from BIOViewer.config import ViewerConfig
import numpy as np


class ContinuousViewer():
    def __init__(self,signal_configs,t_start=0,windowsize=15,stepsize=10,
                 title=None,path_save='Figures',timestamps=None,
                 height_ratios='auto',figsize=(7,4)):
        
        self.signal_configs = _validate_property(signal_configs)
        height_ratios = self._init_height_ratios(height_ratios,signal_configs)
        self.viewer_config = ViewerConfig(t_start,windowsize,stepsize,title,path_save,timestamps)
        self.fig, self.axs = plt.subplots((len(signal_configs)),height_ratios=height_ratios,figsize=figsize)
        self.displays, self.loaders = self._build_displays_and_loaders(self.axs,signal_configs,self.viewer_config)

        action_handler = ActionHandler(self.fig,self.viewer_config,self.signal_configs,self.displays,self.loaders)
        action_handler('init')
        self.fig.canvas.mpl_connect('key_press_event', lambda event: action_handler(event.key))

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

import matplotlib.pyplot as plt
import datetime
from functools import partial
import os

class ActionHandler():
    def __init__(self,fig,viewer_config,signal_configs,displays,loaders):
         self.actions = {
            'z': lambda: self.save_figure(fig,viewer_config.path_save,viewer_config.title,viewer_config.t_start),
            'right': partial(self.move_window, 'right',
                             viewer_config,signal_configs,displays,loaders),
            'left': partial(self.move_window, 'left',
                             viewer_config,signal_configs,displays,loaders),                             
            'n': partial(self.move_window, 'n',
                             viewer_config,signal_configs,displays,loaders),                             
            'b': partial(self.move_window, 'b',
                             viewer_config,signal_configs,displays,loaders),                             
            'init': partial(self.init_viewer,
                             viewer_config,signal_configs,displays,loaders)
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)

    def move_window(self,direction,viewer_config,signal_configs,displays,loaders):
        self.move_t_start(direction,viewer_config)
        self.update(viewer_config,signal_configs,displays,loaders)
    
    def update(self,viewer_config,signal_configs,displays,loaders):
        for signal_config,display,loader in zip(signal_configs,displays,loaders):
            self.update_signal(viewer_config.t_start,viewer_config.windowsize,signal_config,display,loader)

    def update_signal(self,t_start,windowsize,signal_config,display,loader):
        data = loader.load_signal(t_start,windowsize,signal_config.scale)
        display.plot_data(data,signal_config.y_locations)
        self.update_t_ticks(display,t_start,windowsize,signal_config.t_ticks,signal_config.real_time)
        plt.draw()

    def update_t_ticks(self, display,t_start,windowsize,t_ticks,real_time=False):
        ticks = list(range(0, windowsize + 1))
        labels = list(range(int(t_start), int(t_start+windowsize) + 1))
        if t_ticks ==True:        
            if real_time==True:
                labels = [seconds_to_hms(label) for label in labels]
            display.set_t_ticks(ticks,labels)
        else:
            display.set_t_ticks([],[])

    def move_t_start(self,direction,viewer_config):
        if direction =='right':
            viewer_config.t_start = viewer_config.t_start + viewer_config.stepsize
        if direction =='left':
            viewer_config.t_start = viewer_config.t_start - viewer_config.stepsize
        if direction in ['n','b']:
            viewer_config.t_start,viewer_config.timestamp_idx = self.go_to_marker(viewer_config.t_start,
                                                            viewer_config.windowsize,
                                                            viewer_config.timestamps,
                                                            viewer_config.timestamp_idx,
                                                            direction)        

    def go_to_marker(self,t_start,windowsize,timestamps,timestamp_idx,direction):
        if len(timestamps)==0:
            print('No timestamps specified!')
            return t_start, 0 
        if direction == 'n':
            timestamp_idx += 1
            t_start = timestamps[timestamp_idx%len(timestamps)]-windowsize/2
        if direction == 'b':
            timestamp_idx -= 1
            t_start = timestamps[timestamp_idx%len(timestamps)]-windowsize/2
        return t_start, timestamp_idx

    def init_viewer(self,viewer_config,signal_configs,displays,loaders):
        self.fig.suptitle(viewer_config.title)
        self.update(viewer_config,signal_configs,displays,loaders)
        self.fig.tight_layout()

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