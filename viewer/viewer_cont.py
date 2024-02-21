from BIOViewer.viewer.base_viewer import BaseViewer
from functools import partial
import matplotlib.pyplot as plt
from BIOViewer.utils.config import ViewerConfig
import numpy as np
import datetime

class ContinuousViewer(BaseViewer):
    """
    A class for continuous visualization of signal data, extending the BaseViewer.

    This viewer is designed to handle continuous signal data, providing functionalities
    such as automatic scaling, dynamic windowing, and interactive navigation through the signal.
    It integrates with matplotlib for plotting and supports custom actions for user interaction.

    Attributes:
        signal_configs (list): A list of signal configuration objects specifying the signals to be visualized.
        t_start (float): The start time (in seconds) for the initial visualization window.
        windowsize (float): The duration (in seconds) of the visualization window.
        stepsize (float): The step size (in seconds) for navigation through the signal (e.g., moving the window).
        title (str, optional): The title for the visualization window. Defaults to None.
        path_save (str, optional): The path where figures will be saved when triggered. Defaults to 'Figures'.
        timestamps (list, optional): A list of specific timestamps for quick navigation. Defaults to None.
        height_ratios (str or list, optional): Specifies the height ratios for subplots; can be 'auto' or a list of ratios. Defaults to 'auto'.
        figsize (tuple, optional): The figure size for the matplotlib visualization. Defaults to (7, 4).
        scale (str, optional): Specifies the scaling mode for signal amplitude; can be 'auto' or a fixed value. Defaults to 'auto'.

    Inherits from:
        BaseViewer: A base class providing foundational visualization functionalities.

    Example:
        signal_configs = [SignalConfig(signal=data, Fs=256, channel_names=['ch1', 'ch2'])]
        viewer = ContinuousViewer(signal_configs=signal_configs, t_start=0, windowsize=10)
        viewer.show()  # This would initiate the visualization based on the provided configurations.
    """
    def __init__(self,signal_configs,t_start=0,windowsize=15,stepsize=10,
                 title=None, path_save='Figures', timestamps=None,
                 height_ratios='auto', figsize=(7, 4),scale='auto'):
        super().__init__(signal_configs,t_start=t_start,windowsize=windowsize,
                 title=title, path_save=path_save, timestamps=timestamps,
                 height_ratios=height_ratios, figsize=figsize)

        self.viewer_config = ViewerConfig(t_start=t_start,windowsize=windowsize,title=title,path_save=path_save,timestamps=timestamps,stepsize=stepsize)
        self._build_loaders(self.signal_configs)
        if scale =='auto':
            self._auto_scale(signal_configs) 
        self.action_handler = ActionHandlerCont(self.fig,self.viewer_config,self.signal_configs,self.displays)
        self.action_handler('init')
        self.fig.canvas.mpl_connect('key_press_event', lambda event: self.action_handler(event.key))

        # display
        plt.ion()
        plt.show(block=True)

    
    def _auto_scale(self,signal_configs):
        for signal_config in signal_configs:
            signal_config.scale = (self._calcualte_scale(signal_config.loader.signal)) 

    @staticmethod
    def _calcualte_scale(signal):
        percentiles = np.percentile(np.abs(signal), 95, axis=1)
        scale = max(percentiles)
        scale = round_to_first_digit(scale)
        return scale

    @staticmethod
    def _build_loaders(signal_configs):
        for signal_config in signal_configs:
            signal_config.loader = SignalLoader(signal_config.signal,
                            signal_config.Fs,
                            signal_config.transforms)

class SignalLoader():
    """
    Loader class for continuous signal data.

    Attributes:
        config (ContinuousConfig): Configuration object for loading.
        transforms (list of callable): List of functions for signal transformation.
    """
    def __init__(self,signal,Fs,transforms=None):
        self.transforms = transforms if transforms is not None else []
        self.Fs = Fs
        self.signal = signal
        
        
    def __call__(self,start,windowsize,scale):
        """
        Load a segment of the signal data.
        Args:
            start (float): Start time of the segment to load (in seconds).
        Returns:
            np.ndarray: Loaded segment of the signal.
        """
        start_ts = int(start* self.Fs)
        end_ts = int((start+windowsize)*self.Fs)
        signal = self.signal[:,start_ts: end_ts]
        for transform in self.transforms:
            signal = transform(signal)
        signal = (1/scale)*signal
        return signal

class ActionHandlerCont():
    def __init__(self,fig,viewer_config,signal_configs,displays):
         self.actions = {
            'z': lambda: self.save_figure(fig,viewer_config.path_save,viewer_config.title,viewer_config.t_start),
            'right': partial(self.move_window, 'right',
                             viewer_config,signal_configs,displays),
            'left': partial(self.move_window, 'left',
                             viewer_config,signal_configs,displays),                             
            'n': partial(self.move_window, 'n',
                             viewer_config,signal_configs,displays),                             
            'b': partial(self.move_window, 'b',
                             viewer_config,signal_configs,displays),                             
            'init': partial(self.init_viewer,fig,
                             viewer_config,signal_configs,displays)
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)

    def move_window(self,direction,viewer_config,signal_configs,displays):
        self.move_t_start(direction,viewer_config)
        self.update(viewer_config,signal_configs,displays)
    
    def update(self,viewer_config,signal_configs,displays):
        for signal_config,display in zip(signal_configs,displays):
            self.update_signal(viewer_config,signal_config,display)

    def update_signal(self,viewer_config,signal_config,display):
        t_start,windowsize = viewer_config.t_start,viewer_config.windowsize
        data = signal_config.loader(t_start,windowsize,signal_config.scale)
        display.plot_data(data,signal_config.y_locations)
        self.update_t_ticks(display,t_start,windowsize,signal_config.t_ticks,signal_config.real_time,signal_config.t_label)
        plt.draw()

    def update_t_ticks(self, display,t_start,windowsize,t_ticks,real_time,t_label):
        ticks = list(range(0, windowsize + 1))
        labels = list(range(int(t_start), int(t_start+windowsize) + 1))
        if t_ticks ==True:     
            display.ax.set_xlabel(t_label)
            if real_time==True:
                labels = [self._seconds_to_hms(label) for label in labels]
                display.ax.set_xticks(ticks,labels)
        else:
            display.ax.set_xticks([],[])

    def move_t_start(self,direction,viewer_config):
        if direction =='right':
            viewer_config.t_start = viewer_config.t_start + viewer_config.stepsize
        if direction =='left':
            viewer_config.t_start = viewer_config.t_start - viewer_config.stepsize
        if direction in ['n','b']:
            viewer_config.t_start,viewer_config.idx = self.go_to_marker(viewer_config.t_start,
                                                            viewer_config.windowsize,
                                                            viewer_config.timestamps,
                                                            viewer_config.idx,
                                                            direction)        

    def go_to_marker(self,t_start,windowsize,timestamps,idx,direction):
        if len(timestamps)==0:
            print('No timestamps specified!')
            return t_start, 0 
        if direction == 'n':
            idx += 1
            t_start = timestamps[idx%len(timestamps)]-windowsize/2
        if direction == 'b':
            idx -= 1
            t_start = timestamps[idx%len(timestamps)]-windowsize/2
        return t_start, idx

    def init_viewer(self,fig,viewer_config,signal_configs,displays):
        fig.suptitle(viewer_config.title)
        self.update(viewer_config,signal_configs,displays)
        fig.tight_layout()

    @staticmethod
    def _seconds_to_hms(seconds):
        # Construct a datetime object with a base date
        base_date = datetime.datetime(1900, 1, 1)
        # Add the timedelta to the base date
        result_datetime = base_date + datetime.timedelta(seconds=seconds)
        # Format the result as hours:minutes:seconds
        formatted_time = result_datetime.strftime('%H:%M:%S')

        return formatted_time

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