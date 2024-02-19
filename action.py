import matplotlib.pyplot as plt
import datetime
from functools import partial
import os

class SignalAction():
    def __init__(self,config,display,loader):
        self.actions = {
            'right': partial(move_window, config, display, loader, 'right'), 
            'left': partial(move_window, config, display, loader, 'left'),
            'n': partial(move_window, config, display, loader, 'n'),
            'b': partial(move_window, config, display, loader, 'b'),
            'init': partial(init_display, config, display, loader),
            }

    def __call__(self,key):
        if key in self.actions.keys():
            self.actions[key]()

def move_window(config,display,loader,direction='right'):
    if direction in ['left','right']:
        config.t_start = move_t_start(config.t_start,config.windowsize,direction)
    if direction in ['n','b']:
        config.t_start,config.timestamp_idx = go_to_marker(config.t_start,config.windowsize,config.timestamps,config.timestamp_idx,direction)
    signal = loader.load_signal(config.t_start)
    display.plot_data(signal)
    update_t_ticks(config,display)
    # add info 
    plt.draw()

def init_display(config,display,loader):
    signal = loader.load_signal(config.t_start)
    display.plot_data(signal)
    update_t_ticks(config,display)
    # add info 
    plt.draw()

def seconds_to_hms(seconds):
    # Construct a datetime object with a base date
    base_date = datetime.datetime(1900, 1, 1)
    # Add the timedelta to the base date
    result_datetime = base_date + datetime.timedelta(seconds=seconds)
    # Format the result as hours:minutes:seconds
    formatted_time = result_datetime.strftime('%H:%M:%S')

    return formatted_time

def update_t_ticks( display,t_start,windowsize,t_ticks,real_time=False):
    ticks = list(range(0, windowsize + 1))
    labels = list(range(int(t_start), int(t_start+windowsize) + 1))
    if t_ticks ==True:        
        if real_time==True:
            labels = [seconds_to_hms(label) for label in labels]
        display.set_t_ticks(ticks,labels)
    else:
        display.set_t_ticks([],[])

class ActionHandler():
    def __init__(self,fig,viewer_config,signal_configs,displays,loaders):
         self.actions = {
            'z': lambda: self.save_figure(fig,viewer_config.path_save,viewer_config.title,viewer_config.t_start),
            'right': partial(self.move_window, 'right',
                             viewer_config,signal_configs,displays,loaders),
            'left': partial(self.move_window, 'left',
                             viewer_config,signal_configs,displays,loaders),                             
            'n': partial(self.move_t_start, viewer_config, 'n'),
            'b': partial(self.move_t_start, viewer_config, 'b')
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)

    def move_window(self,direction,viewer_config,signal_configs,displays,loaders):
        self.move_t_start(direction,viewer_config)
        for signal_config,display,loader in zip(signal_configs,displays,loaders):
            update_signal(viewer_config.t_start,viewer_config.windowsize,signal_config,display,loader)

    def move_t_start(self,direction,viewer_config):
        if direction in ['left','right']:
            viewer_config.t_start = move_t_start(viewer_config.t_start,viewer_config.windowsize,direction)
        if direction in ['n','b']:
            viewer_config.t_start,viewer_config.timestamp_idx = go_to_marker(viewer_config.t_start,
                                                            viewer_config.windowsize,
                                                            viewer_config.timestamps,
                                                            viewer_config.timestamp_idx,
                                                            direction)        

def update_signal(t_start,windowsize,signal_config,display,loader):
    data = loader.load_data(t_start,windowsize)
    display.plot_data(data,signal_config.y_locations)
    update_t_ticks(display,t_start,windowsize,signal_config.t_ticks,signal_config.real_time)
    plt.draw()

def move_t_start(t_start,windowsize,direction):
    if direction =='right':
        t_start = t_start + windowsize
    if direction =='left':
        t_start = t_start - windowsize
    return t_start

def go_to_marker(t_start,windowsize,timestamps,timestamp_idx,direction):
    if direction == 'n':
        t_start = timestamps[timestamp_idx]-windowsize/2
        timestamp_idx += 1
    if direction == 'b':
        t_start = timestamps[timestamp_idx]-windowsize/2
        timestamp_idx -= 1
    return t_start, timestamp_idx

