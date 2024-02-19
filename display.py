import numpy as np

class SignalDisplay():
    def __init__(self,ax,t_start,t_end,channel_names,y_locations,Fs,y_pad):
        self.lines = []
        for y_location in y_locations:
            n_points = int((t_end-t_start)*Fs)
            line, = ax.plot((np.linspace(t_start,t_end,n_points)),([y_location]*n_points),'black',linewidth=0.7)
            self.lines.append(line)
        ax.set_yticks(y_locations,channel_names)
        ax.set_ylim(min(y_locations)-y_pad,max(y_locations)+y_pad)
        ax.set_xlim(t_start,t_end)
        self.ax = ax

    def plot_data(self,signal,y_locations):
        for i,(line,y_location) in enumerate(zip(self.lines,y_locations)):
            channel_signal = signal[i,:]+y_location
            line.set_ydata(channel_signal)

    def set_t_ticks(self,ticks,labels):
        self.ax.set_xticks(ticks,labels)