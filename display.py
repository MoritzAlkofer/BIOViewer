import numpy as np

class SignalDisplay():
    def __init__(self,ax,viewer_config, signal_config):
        # unpack configs
        t_start = viewer_config.t_start
        t_end = viewer_config.t_end
        channel_names = signal_config.channel_names
        unit = signal_config.unit
        y_locations = signal_config.y_locations
        Fs = signal_config.Fs
        scale = signal_config.scale

        self.lines = []
        for idx in range(len(channel_names)):
            n_points = int((t_end-t_start)*Fs)
            line, = ax.plot((np.linspace(t_start,t_end,n_points)),([-idx]*n_points),'black',linewidth=0.7)
            self.lines.append(line)
        plot_scale(ax,scale,unit)
        ax.set_yticks(y_locations,channel_names)
        ax.set_ylim(min(y_locations)-1.5,max(y_locations)+1.5)
        ax.set_xlim(t_start,t_end)
        self.ax = ax

    def plot_data(self,signal,y_locations):
        for i,(line,y_location) in enumerate(zip(self.lines,y_locations)):
            channel_signal = signal[i,:]+y_location
            line.set_ydata(channel_signal)

    def set_t_ticks(self,ticks,labels):
        self.ax.set_xticks(ticks,labels)


def plot_scale(ax,scale,unit):
    ax.plot((1,1),(0,1),'r')
    ax.text(1.1,0.5,f'{scale} {unit}',c='r')