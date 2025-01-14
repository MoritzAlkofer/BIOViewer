import matplotlib.pyplot as plt
import os 
from .state import StateManager
from .signal import Signal
from typing import List

class Viewer:
    """
    A comprehensive viewer for visualizing multiple signals with synchronized control.

    The `Viewer` class allows users to display and interact with multiple `Signal` instances 
    in a unified interface. It provides features such as synchronized scrolling, real-time 
    updates, and customizable layouts for intuitive exploration of signal data.

    Args:
        signals (list[Signal]): A list of `Signal` instances to be visualized.
        figsize (tuple, optional): Dimensions of the figure in inches as (width, height). 
            Default is (10, 4).
        t_start (float, optional): Initial start time of the displayed window (in seconds). 
            Default is 0.
        windowsize (float, optional): Duration of the signal window to display (in seconds). 
            Default is 15.
        stepsize (float, optional): Step size for scrolling through the signal (in seconds). 
            Default is 13.
        timestamps (list[float], optional): A list of timestamps (in seconds) representing markers 
            that can be navigated using the 'n' (next) and 'b' (previous) keys. Default is an empty list.
        height_ratios (str or list[int], optional): Proportions of heights for each signal display. 
            If 'auto', heights are determined based on the number of channels in each signal. 
            If a list, it should have one entry per signal. Default is 'auto'.
        real_time (bool, optional): Whether to display time in real-world format (hh:mm:ss) 
            or in seconds. Default is True.

    Example:
        ```python
        import numpy as np
        from signal_module import Signal, Viewer

        # Create signal data
        data = np.random.randn(6, 1000)  # 6 channels, 1000 time steps
        timestamps = [10, 50, 100]

        # Initialize Signal instances
        signal0 = Signal(data=data, fs=128, scale_factor=220, 
                        y_ticks=['a', 'b', 'c', 'd', 'e', 'f'], 
                        unit='mV', colors='bbbkbr', linewidth=1, show_scale=True)
        signal1 = Signal(data=data, fs=128)

        # Create and launch the Viewer
        viewer = Viewer(signals=[signal0, signal1], figsize=(14, 4), 
                        timestamps=timestamps, stepsize=0.5)
        ```
    Notes:
        - Use keyboard shortcuts (`left`, `right`, `n`, `b`) for navigation within the Viewer.
        - All signals are displayed in synchronized windows, enabling intuitive comparison.
        - Scales and labels are customizable through the attributes of the respective `Signal` instances.
    """

    def __init__(self,signals: List[Signal],savepath='Figures',figsize=(10,4),t_start=0,windowsize=15,stepsize=13,timestamps=[],height_ratios='auto',real_time=True):
        self.signals = signals
        self.savepath = savepath
        self.statemanager = StateManager(t_start=t_start,windowsize=windowsize,stepsize=stepsize,timestamps=timestamps,real_time=real_time) #init statemanager
        self.height_ratios = self._init_height_ratios(height_ratios)
        self.fig,self.axs = self._init_fig_and_axs(figsize)
        self._init_signaldisplays()
        self._init_button_connection()
        self._init_scales()
        self._update_display() # initial update to load and display first frame of ts
        self._show_figure()

    def _init_height_ratios(self,height_ratios):
        if height_ratios=='auto':
            height_ratios = [signal.data.n_channels+1 for signal in self.signals]
        elif (len(height_ratios)!= len(self.signals)) or (not isinstance(height_ratios, list)):
            raise ValueError(f"Expected height ratios to be 'auto' or list of {len(self.signals)} entries, but got {len(height_ratios)}.")
        
        return height_ratios

    def _init_fig_and_axs(self,figsize):
        n_displays = len(self.signals)
        fig,axs = plt.subplots(n_displays,1,figsize=figsize,height_ratios=self.height_ratios,sharex=True)
        return fig, axs
    
    def _init_signaldisplays(self):
        for i, signal in enumerate(self.signals):
            signal.display.init_display(ax=self.axs[i],
                                        real_time=self.statemanager.real_time,
                                        t_start=self.statemanager.t_start,
                                        windowsize=self.statemanager.windowsize,
                                        fs=signal.data.fs)

    def _init_scales(self):
        for i, signal in enumerate(self.signals):
            if signal.display.show_scale == True:
                signal.display.plot_scale(signal.data.scale_factor,self.statemanager.windowsize,signal.display.unit)
    
    def _init_button_connection(self):
        self.fig.canvas.mpl_connect('key_press_event', lambda event: self._handle_key_event(event.key))

    def _show_figure(self):
        plt.ion() # make interactive 
        plt.tight_layout()
        plt.show(block=True) # show figure

    def _handle_key_event(self,key):
        if key =='z':
            self._save_figure()
        else:
            self.statemanager.update_state(key)
            self._update_display()

    def _save_figure(self):
        savepath = os.path.join(self.savepath,f'tstart_{self.statemanager.t_start}s.png')
        os.makedirs(os.path.dirname(savepath), exist_ok=True)
        self.fig.savefig(savepath)

    def _update_display(self):
        for signal in self.signals:
            x = signal.data.load(self.statemanager.t_start,self.statemanager.windowsize)
            x = signal.data.scale(x)
            signal.display.update_lines(data=x)
            signal.display.update_t_ticks(self.statemanager.t_start,self.statemanager.windowsize)
    