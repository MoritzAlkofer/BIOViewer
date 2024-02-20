import numpy as np
import h5py 

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
        
        
    def load_signal(self,start,windowsize,scale):
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

class EventLoader():
    def __init__(self,config,transforms=None):
        self.config = config

    def load_signal(self,path_signal):
        signal = np.load(path_signal)
        start, end  = self.config.t_start*self.config.Fs, self.config.t_end*self.config.Fs
        signal = signal[:,start:end]
        for transform in self.transforms:
            signal = transform(signal)
        return signal
