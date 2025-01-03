from dataclasses import dataclass,field
from functools import partial
from typing import Any, List
import numpy as np
import os


class Signal():
    # this class handles everything related to the signal information
    def __init__(self,data: np.ndarray ,Fs=128,scale_factor=1,unit="arbitrary units"):
        self.data = data
        self.fs = Fs
        self.scale_factor = scale_factor 
        self.unit = unit

    def load(self,t_start=int,windowsize=int):
        """
        Load a segment of the signal data.
        Args:
            start (float): Start time of the segment to load (in seconds).
        Returns:
            np.ndarray: Loaded segment of the signal.
        """
        start_ts = int(t_start* self.fs)
        end_ts = int((t_start+windowsize)*self.fs)
        signal = self.data[:,start_ts:end_ts]
        return signal
    
    def scale(self,signal):
        signal = (1/self.scale_factor)*signal
        return signal

    def get_metadata(self) -> dict:
        return {
            "shape": self.data.shape,
            "Fs": self.Fs,
            "scale": self.scale,
            "unit": self.unit
        }    
    
@dataclass  
class DisplayConfig:
    """Configuration for signal processing."""
    n_channels: int
    y_ticks: List[Any]
    real_time: bool = True
    t_label: str = 'Time [h:m:s]'
    show_t_ticks: bool = True
    y_locations: List[int] = field(init=False)  # Computed field

    def __post_init__(self):
        self.y_locations = [-idx for idx in range(len(self.y_ticks))]

class Display():
    # this class only displays the information
    def __init__(self,ax,config = DisplayConfig):
        self.ax = ax
        self.config = config

    def init_display(self,t_start,windowsize,n_channels,Fs):
        self.init_y_ticks_and_lim(t_start,windowsize)
        self.init_channels(n_channels,windowsize,Fs)

    def init_y_ticks_and_lim(self,t_start,windowsize):
        self.ax.set_yticks(self.config.y_locations,self.config.y_ticks)
        self.ax.set_ylim(min(self.config.y_locations)-1,max(self.config.y_locations)+1)
        self.ax.set_xlim(t_start,t_start+windowsize)
    
    def init_channels(self,n_channels,windowsize,Fs):
        lines = []
        timesteps =windowsize*Fs
        for idx in range(n_channels):
            line, = self.ax.plot((np.linspace(0,windowsize,timesteps)),([-idx]*timesteps),'black',linewidth=0.7)
            lines.append(line)
        self.lines = lines
    
    def update_lines(self, data):
        n_channels = data.shape[0]
        for idx in range(n_channels):
            channel_signal = data[idx,:] + self.config.y_locations[idx]
            self.lines[idx].set_ydata(channel_signal)
                
    def update_t_ticks(self,t_start,windowsize):
        ticks = list(range(0, windowsize + 1))
        labels = list(range(int(t_start), int(t_start+windowsize) + 1))
        if self.config.show_t_ticks ==True:     
            self.ax.set_xticks(ticks,labels)
            # if self.real_time==True:
            #     labels = [seconds_to_hms(label) for label in labels]
            #     self.ax.set_xticks(ticks,labels)
        else:
            self.ax.set_xticks([],[])
   
@dataclass  
class State:
    t_start: int = 0
    windowsize: int = 15
    stepsize: int = 13
    real_time: bool = False
    timestamps: List[Any] = None
    timestamp_idx = -1

class StateManager:
    def __init__(self,state = State):
        self.state = state
        self.actions = self._init_actions()

    def _init_actions(self):
        return {
            'right': partial(self.move_t_start, 'right'),
            'left': partial(self.move_t_start, 'left'),                             
            'n': partial(self.move_t_start, 'n'),                             
            'b': partial(self.move_t_start, 'b')
            }
    
    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def move_t_start(self,direction):
        if direction =='init':
            pass            
        if direction =='right':
            self.state.t_start = self.state.t_start + self.state.stepsize
        if direction =='left':
            self.state.t_start = self.state.t_start - self.state.stepsize
        if direction in ['n','b']:
            self.go_to_marker(direction)        

    def go_to_marker(self,direction):
        if len(self.state.timestamps)==0:
            print('No timestamps specified!')
            return t_start, 0 
        if direction == 'n':
            idx += 1
            t_start = self.state.timestamps[idx%len(self.state.timestamps)]-self.state.windowsize/2
        if direction == 'b':
            idx -= 1
            t_start = self.state.timestamps[idx%len(self.state.timestamps)]-self.state.windowsize/2
        # update state
        self.state.t_start,self.state.idx

class Coordinator:
    def __init__(self,state=State,signals=List[Signal],displays=List[Display],statemanager=StateManager):
        self.state = state
        self.signals = signals
        self.displays = displays
        self.statemanager = statemanager

    def update(self,key):
        statemanager(key)
        for signal,display in zip(self.signals,self.displays):
            data = signal.load(self.state.t_start,self.state.windowsize)
            data = signal.scale(data)
            display.update_lines(data=data)
            display.update_t_ticks(state.t_start,state.windowsize)
    
    def init(ax,signal,display_config,state):
        # build display
        display = Display(ax,display_config)
        display.init_display(state.t_start,state.windowsize,n_channels=signal.data.shape[0],Fs=signal.Fs)

if __name__ =="__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    # init signals
    data = np.load('../demos/example.npy')
    
    signal1 = Signal(data,Fs=128,scale_factor=100)
    signal2 = Signal(data,Fs=128,scale_factor=100)

    # init state    
    state = State()
    
    # init figure
    fig,axs = plt.subplots(1,2,figsize=(10,4))

    # init displays
    display_config = DisplayConfig(n_channels=6,y_ticks=[1,2,3,4,5,6])
    display0 = Display(axs[0],display_config)
    display0.init_display(state.t_start,state.windowsize,n_channels=signal1.data.shape[0],Fs=signal1.fs)
    
    display1 = Display(axs[1],display_config)
    display1.init_display(state.t_start,state.windowsize,n_channels=signal1.data.shape[0],Fs=signal1.fs)
    
    # init statemanager
    statemanager = StateManager(state)
    
    # tie everything together in Coordinator
    coordinator = Coordinator(signals = [signal1,signal2],displays=[display0,display1],statemanager=statemanager,state=state)

    # make coordinator interactive
    fig.canvas.mpl_connect('key_press_event', lambda event: coordinator.update(event.key))
    plt.ion()
    
    # show
    plt.show(block=True)

