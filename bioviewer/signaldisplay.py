import numpy as np
import datetime

class SignalDisplay():
    # this class only displays the information
    def __init__(self,n_channels, y_ticks='auto',y_locations='auto', unit ='arbitrary units',colors='k',linewidth=0.7,show_scale=True):
        self.unit = unit 
        self.n_channels = n_channels
        self.linewidth = linewidth
        self.show_scale = show_scale
        self.y_ticks = self._init_y_ticks(n_channels,y_ticks)
        self.y_locations = self._init_y_locations(n_channels,y_locations)
        self.colors = self._init_colors(n_channels,colors)

    def init_display(self,ax,real_time,t_start,windowsize,fs):
        # this init function must be called externally and injects external dependencies (ax and global state variables)
        self.ax = ax
        self.real_time = real_time
        self._init_y_ticks_and_lim(t_start,windowsize)
        self._init_channels(windowsize,fs)

    def _init_y_ticks_and_lim(self,t_start,windowsize):
        self.ax.set_yticks(self.y_locations,self.y_ticks)
        self.ax.set_ylim(min(self.y_locations)-1,max(self.y_locations)+1)
        self.ax.set_xlim(t_start,t_start+windowsize)
    
    def _init_channels(self,windowsize,Fs):
        lines = []
        timesteps =windowsize*Fs
        for idx in range(self.n_channels):
            line, = self.ax.plot((np.linspace(0,windowsize,timesteps)),([-idx]*timesteps),self.colors[idx],linewidth=self.linewidth)
            lines.append(line)
        self.lines = lines

    def _init_y_ticks(self,n_channels,y_ticks):
        if y_ticks == 'auto':
            y_ticks = [x for x in range(n_channels)]
        if len(y_ticks)!= n_channels:
            raise ValueError(f"Expected y_ticks to have {n_channels} entries, but got {len(y_ticks)}.")
        return y_ticks
    
    def _init_y_locations(self,n_channels,y_locations):
        if y_locations=='auto':
            y_locations =  [-idx for idx in range(n_channels)]
        if len(y_locations) != n_channels:
            raise ValueError(f"Expected y_locations to have {n_channels} entries, but got {len(y_locations)}.")
        return y_locations
        
    def _init_colors(self,n_channels,colors):
        if len(colors) == 1:
            colors = n_channels*colors
        if len(colors)!= n_channels:
            raise ValueError(f"Expected y_ticks to have a sting with {n_channels} entries, but got {len(colors)}.")
        return colors

    def update_lines(self, data):
        n_channels = data.shape[0]
        for idx in range(n_channels):
            channel_signal = data[idx,:] + self.y_locations[idx]
            self.lines[idx].set_ydata(channel_signal)
                
    def update_t_ticks(self,t_start,windowsize):
        offset = 1 - t_start % 1
        offset = np.round(offset,5)
        
        offset = 0 if offset == 1 else np.round(offset,5) 
        if offset == 0:
            start_label = int(t_start)
            end_label = int(t_start + windowsize + 1)
        else:
            start_label = int(np.ceil(t_start))
            end_label = int(np.floor(t_start+windowsize))+1
        t_labels = list(range(start_label,end_label))
        
        t_ticks = [t+offset for t in range(len(t_labels))]
        # if the time is to be displayed in h:m:s instead of |s|, convert labels
        if self.real_time==True:
            t_labels = [self._seconds_to_hms(label) for label in t_labels]
        self.ax.set_xticks(t_ticks,t_labels)

    def plot_scale(self,scale,windowsize,unit):
        t = 0.05*windowsize
        self.ax.plot((t,t),(0,-1),'r')
        self.ax.text(t+0.1,-0.5,f'{scale} {unit}',c='r')

    @staticmethod        
    def _seconds_to_hms(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

