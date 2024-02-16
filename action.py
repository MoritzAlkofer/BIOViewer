import matplotlib.pyplot as plt
import datetime
from functools import partial
import os

class SignalAction():
    def __init__(self,config,display,loader):
        self.actions = {
            'right': partial(move_window, config, display, loader, 'right'), 
            'left': partial(move_window, config, display, loader, 'left'),
            'init': partial(init_display, config, display, loader),
            }

    def __call__(self,key):
        if key in self.actions.keys():
            self.actions[key]()

def move_window(config,display,loader,direction='right'):
    config.t_start = move_t_start(config.t_start,config.windowsize,direction)
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

def update_t_ticks(config, display):
    ticks = list(range(0, config.windowsize + 1))
    labels = list(range(config.t_start, config.t_start+config.windowsize + 1))
    if config.t_ticks ==True:        
        if config.real_time==True:
            labels = [seconds_to_hms(label) for label in labels]
        display.set_t_ticks(ticks,labels)
    else:
        display.set_t_ticks([],[])

class ViewerAction():
    def __init__(self,viewer):
         self.actions = {
            'z': lambda: self.save_figure(viewer.fig,viewer.path_save,viewer.title,viewer.t_start),
            'right': partial(self.move_viewer, viewer, 'right'),
            'left': partial(self.move_viewer, viewer, 'left')
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)

    def move_viewer(self,viewer,direction):
        viewer.t_start = move_t_start(viewer.t_start,viewer.windowsize,direction)

def move_t_start(t_start,windowsize,direction):
    if direction =='right':
        t_start = t_start + windowsize
    if direction =='left':
        t_start = t_start - windowsize
    return t_start
