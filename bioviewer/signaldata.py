import numpy as np

class SignalData():
    # this class handles everything related to the signal information
    def __init__(self,data: np.ndarray ,fs: int,scale_factor=1):
        self.data = data
        self.fs = fs
        self.scale_factor = self._init_scalefactor(scale_factor,data) 
        self.n_channels = data.shape[0]
        self.n_timesteps = data.shape[1]

    def _init_scalefactor(self, scale_factor,data):
        if scale_factor=='auto':
            scale_factor = self._auto_scale(data)
        else:
            if not (isinstance(scale_factor,int) or isinstance(scale_factor,float)):
                raise ValueError(f"Expected scale to be 'auto' or integer/float.")
        
        return scale_factor
    
    def _auto_scale(self,signal):
        percentiles = np.nanpercentile(np.abs(signal), 95, axis=1)
        scale_factor = max(percentiles)
        if scale_factor ==0: # this is only when all the data is 0. set to 1 to prevent bugs
            scale_factor = 1
        scale_factor = self._round_to_first_digit(scale_factor)
        return scale_factor
    
    def _round_to_first_digit(self,value):
        if value == 0:
            return 0  # Handle the zero case separately to avoid log10(0)
        
        # Calculate the order of magnitude of the absolute value
        order_of_magnitude = np.floor(np.log10(np.abs(value)))
        
        # Calculate the rounding factor
        rounding_factor = 10**order_of_magnitude
        
        # Round the value to the nearest magnitude based on its first significant digit
        rounded_value = np.round(value / rounding_factor) * rounding_factor
        
        return rounded_value
    
    def load(self,t_start=int,windowsize=int):
        """
        Load a segment of the signal data.
        Args:
            start (float): Start time of the segment to load (in seconds).
        Returns:
            np.ndarray: Loaded segment of the signal.
        """
        start_ts = int(round(t_start* self.fs))
        end_ts = int(round((t_start+windowsize)*self.fs))
        
        # regular case, no padding required
        if (start_ts>=0) and (end_ts<self.n_timesteps):
            signal = self.data[:,start_ts:end_ts]

        # if start is before timestep 0, pad to the left
        elif (start_ts<0)and(end_ts>0):
            n_timesteps = int(round(-t_start*self.fs))
            padding = np.full((self.n_channels,n_timesteps), np.nan)
            signal = self.data[:,0:end_ts] # from 0 to desired end of window
            signal = np.hstack([padding,signal]) # pad from negative time to 0
        # if end_ts is before ts, set all singal to nan
        elif end_ts<0:
            n_timesteps = int(round(windowsize*self.fs))
            signal = np.full((self.n_channels,n_timesteps), np.nan)

        # if end timestep is after end of signal, pad to the right
        elif (start_ts<self.n_timesteps)and(end_ts>self.n_timesteps):
            n_timesteps = end_ts - self.n_timesteps
            padding = np.full((self.n_channels,n_timesteps), np.nan) # pad from end of signal to end of window
            signal = self.data[:,start_ts:self.n_timesteps]  # last bit of available signal
            signal = np.hstack([signal,padding])
        # if start_ts is after signal ends, set all signal to none
        elif start_ts>self.n_timesteps:
            signal = np.full((self.n_channels,windowsize*self.fs), np.nan)
        return signal    

    def scale(self,signal):
        signal = (1/self.scale_factor)*signal
        return signal


