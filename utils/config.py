class BaseConfig():
    def __init__(self,Fs=int,channel_names=list,unit='arbitrary units',
        real_time=False,t_ticks=True,scale='auto',transforms=None
        ):
        self.Fs = Fs
        self.channel_names = _validate_property(channel_names)
        self.y_locations = [-idx for idx in range(len(self.channel_names))]
        self.unit = unit
        self.real_time =real_time
        self.t_label = 'Time [h:m:s]' if real_time else 'Time [s]'
        self.t_ticks = t_ticks
        self.scale = scale
        self.transforms = _validate_property(transforms)


class ContinuousConfig(BaseConfig):
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
    def __init__(self,signal,Fs,channel_names,title=None,unit='arbitrary units',
                 real_time=False,t_ticks=True,scale='auto',transforms=None):
        
        super().__init__(Fs=Fs,channel_names=channel_names,unit=unit,
                         real_time=real_time,t_ticks=t_ticks,scale=scale,transforms=transforms)
        self.signal = signal
        self.title = title

class EventConfig(BaseConfig):
    def __init__(self,path_signals,loader,Fs=int,channel_names=list,titles=None,unit='arbitrary units',
                 real_time=False,t_ticks=True,y_locations='auto',scale='auto',transforms=None):
        super().__init__(Fs=Fs,channel_names=channel_names,unit=unit,
                         real_time=real_time,t_ticks=t_ticks,scale=scale,transforms=transforms)

        self.path_signals = _validate_property(path_signals)
        self.loader = loader
        self.titles = titles if isinstance(titles,list) else [titles]


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
    def __init__(self,t_start=0,windowsize=15,title=None,path_save='Figures',timestamps=None,**kwargs):
        self.t_start = t_start
        self.windowsize = windowsize
        self.title = title
        self.t_end = t_start+windowsize
        self.path_save = path_save
        self.timestamps = _validate_property(timestamps)
        self.idx = -1

        # Iterate through kwargs and set them as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

def _validate_property(property):
    """Ensure signal_configs is a list."""
    if property == None:
        return []
    if not isinstance(property, list):
        return [property]
    return property