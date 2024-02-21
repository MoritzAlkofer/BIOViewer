import numpy as np

class SignalDisplay():
    def __init__(self,ax,viewer_config, signal_config):
        # unpack configs
        t_start = viewer_config.t_start
        t_end = viewer_config.t_end
        windowsize = viewer_config.windowsize
        channel_names = signal_config.channel_names
        unit = signal_config.unit
        y_locations = signal_config.y_locations
        Fs = signal_config.Fs
        scale = signal_config.scale
        self.ax = ax

        self.lines = self._add_lines(self.ax,t_start,t_end,channel_names,Fs)
        self.ax = self._fix_ticks_and_lim(self.ax,y_locations,channel_names,t_start,t_end)
        self.ax = plot_scale(self.ax,scale,windowsize,unit)

    def _fix_ticks_and_lim(self,ax,y_locations,channel_names,t_start,t_end):
        ax.set_yticks(y_locations,channel_names)
        ax.set_ylim(min(y_locations)-1,max(y_locations)+1)
        ax.set_xlim(t_start,t_end)
        return ax


    def _add_lines(self,ax,t_start,t_end,channel_names,Fs):
        lines =[]
        for idx in range(len(channel_names)):
            n_points = int((t_end-t_start)*Fs)
            line, = ax.plot((np.linspace(t_start,t_end,n_points)),([-idx]*n_points),'black',linewidth=0.7)
            lines.append(line)
        return lines

    def plot_data(self,signal,y_locations):
        for i,(line,y_location) in enumerate(zip(self.lines,y_locations)):
            channel_signal = signal[i,:]+y_location
            line.set_ydata(channel_signal)

def plot_scale(ax,scale,windowsize,unit):
    t = 0.05*windowsize
    ax.plot((t,t),(0,-1),'r')
    ax.text(t+0.1,-0.5,f'{scale} {unit}',c='r')
    return ax