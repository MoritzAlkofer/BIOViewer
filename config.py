class ContinuousConfig():
    """
    Configuration class for continuous signal visualization.

    Attributes:
        path_signal (str): File path to the signal data.
        start (float): Start time for visualization (in seconds).
        windowsize (float): Size of the window for visualization (in seconds).
        stepsize (float): Step size for moving the window (in seconds).
        Fq_signal (int): Sampling frequency of the signal.
        channels (list of str): List of channel names.
        y_locations (list of float): Y-axis locations for each channel.
        title (str): Title for the visualization.
    """
    def __init__(self,signal,Fs=int,channel_names=list,title=None,unit='arbitrary units',
                 real_time=False,t_ticks=True,y_locations='auto',scale='auto',transforms=None):
        self.signal = signal
        self.Fs = Fs
        self.channel_names = _validate_property(channel_names)
        self.y_locations = [-idx for idx in range(len(self.channel_names))] if y_locations == 'auto' else y_locations
        self.title = title
        self.unit = unit
        self.real_time =real_time
        self.t_ticks = t_ticks
        self.scale = scale
        self.transforms = _validate_property(transforms)

class EventConfig():
    def __init__(self,path_signals,loader,Fs=int,channel_names=list,titles=None,unit='arbitrary units',
                 real_time=False,t_ticks=True,y_locations='auto',scale='auto',transforms=None):
        self.path_signals = _validate_property(path_signals)
        self.loader = loader
        self.Fs = Fs
        self.channel_names = _validate_property(channel_names)
        self.y_locations = [-idx for idx in range(len(self.channel_names))] if y_locations == 'auto' else y_locations
        self.titles = _validate_property(titles)
        self.unit = unit
        self.real_time =real_time
        self.t_ticks = t_ticks
        self.scale = scale
        self.transforms = _validate_property(transforms)

class ViewerConfig():
    """
    Configuration class for full Viewer

    Attributes:
        start (float): Start time for visualization (in seconds).
        windowsize (float): Size of the window for visualization (in seconds).
        stepsize (float): Step size for moving the window (in seconds).
        Fq_signal (int): Sampling frequency of the signal.
        title (str): Title for the visualization.
    """
    def __init__(self,t_start=0,windowsize=15,stepsize=10,title=None,path_save='Figures',timestamps=None):
        self.t_start = t_start
        self.windowsize = windowsize
        self.stepsize = stepsize
        self.title = _validate_property(title)
        self.t_end = t_start+windowsize
        self.path_save = path_save
        self.timestamps = _validate_property(timestamps)
        self.timestamp_idx = -1
        self.sample_idx = 0


def _validate_property(property):
    """Ensure signal_configs is a list."""
    if property == None:
        return []
    if not isinstance(property, list):
        return [property]
    return property