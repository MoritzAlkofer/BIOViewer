from BIOViewer.viewer.base_viewer import BaseViewer
from functools import partial
import matplotlib.pyplot as plt

class EventViewer(BaseViewer):
    def __init__(self,signal_configs,t_start=0,windowsize=15,
                 title=None, path_save='Figures', timestamps=None,
                 height_ratios='auto', figsize=(7, 4)):
        super().__init__(signal_configs,t_start=t_start,windowsize=windowsize,
                 title=title, path_save=path_save, timestamps=timestamps,
                 height_ratios=height_ratios, figsize=figsize)

        self.action_handler = ActionHandlerEvent(self.fig,self.viewer_config,self.signal_configs,self.displays)
        self.action_handler('init')
        self.fig.canvas.mpl_connect('key_press_event', lambda event: self.action_handler(event.key))

        # display
        plt.ion()
        plt.show(block=True)

class ActionHandlerEvent():
    def __init__(self,fig,viewer_config,signal_configs,displays):
         self.actions = {
            'z': lambda: self.save_figure(fig,viewer_config.path_save,viewer_config.title,viewer_config.t_start),
            'right': partial(self.change_sample, 'right', fig,
                             viewer_config,signal_configs,displays),
            'left': partial(self.change_sample, 'left', fig,
                             viewer_config,signal_configs,displays),                             
            'init': partial(self.init_viewer, fig,
                             viewer_config,signal_configs,displays)
            }

    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def save_figure(self,fig,path_save,title,t_start):
        title = 'Figure' if title ==None else title
        savename = os.path.join(path_save,title+'_'+str(t_start)+'.png')
        fig.savefig(savename)
                
    def change_sample(self,direction,fig,viewer_config,signal_configs,displays):
        if direction =='right':
            viewer_config.idx +=1
        if direction =='left':
            viewer_config.idx -=1
        self.update(fig,viewer_config,signal_configs,displays)

    def init_viewer(self,fig,viewer_config,signal_configs,displays):
        self.update(fig,viewer_config,signal_configs,displays)
        fig.tight_layout()

    def update(self,fig,viewer_config,signal_configs,displays):
        idx = viewer_config.idx
        for signal_config,display in zip(signal_configs,displays):
            data = signal_config.loader(signal_config.path_signals[idx])
            for transform in signal_config.transforms:
                data = transform(data)
            data = (1/signal_config.scale)*data
            display.plot_data(data,signal_config.y_locations)
        if viewer_config.title!=None:
            fig.suptitle(viewer_config.title[idx])
