
from BIOViewer.utils.config import ViewerConfig
from BIOViewer.utils.display import  SignalDisplay
from BIOViewer.utils.helper import validate_property

import matplotlib.pyplot as plt

class BaseViewer():
    def __init__(self,signal_configs,t_start=0,windowsize=15,
                 title=None, path_save='Figures', timestamps=None,
                 height_ratios='auto', figsize=(7, 4)):

        # init configs        
        self.signal_configs = validate_property(signal_configs)
        self.viewer_config = ViewerConfig(t_start, windowsize, title, path_save, timestamps)

        # build viewer and displays displays
        height_ratios = self._init_height_ratios(height_ratios,signal_configs)
        self.fig, self.axs = plt.subplots(len(signal_configs), height_ratios=height_ratios, figsize=figsize)
        self.displays = self._build_displays(self.axs,self.signal_configs,self.viewer_config)

    def _init_height_ratios(self,height_ratios,signal_configs):
        if height_ratios == 'auto':
            height_ratios = [len(signal_config.channel_names)+1 for signal_config in signal_configs]
        return height_ratios

    @staticmethod
    def _build_displays(axs,signal_configs,viewer_config):    
        displays = []
        for i,signal_config in enumerate(signal_configs):
            # add viewer base configuration to signal configs
            ax = axs if len(signal_configs)==1 else axs[i]
            display = SignalDisplay(ax,viewer_config,signal_config)
            displays.append(display)
        return displays