from functools import partial
from typing import Any, List


class StateManager:
    def __init__(self,t_start = 0,windowsize=15,stepsize=13,timestamps = [],real_time=True):
        self.t_start = t_start
        self.windowsize = windowsize
        self.stepsize = stepsize
        self.timestamps = timestamps
        self._timestamp_idx = -1
        self.real_time=real_time

        self.actions = self._init_actions()

    def _init_actions(self):
        return {
            'right': partial(self.move_t_start, 'right'),
            'left': partial(self.move_t_start, 'left'),                             
            'n': partial(self.move_t_start, 'n'),                             
            'b': partial(self.move_t_start, 'b'),
            'pass': lambda: None
            }
    
    def __call__(self,key):
         if key in self.actions.keys():
            self.actions[key]()

    def move_t_start(self,direction):
        if direction =='init':
            pass            
        if direction =='right':
            self.t_start = self.t_start + self.stepsize
        if direction =='left':
            self.t_start = self.t_start - self.stepsize
        if direction in ['n','b']:
            self.go_to_marker(direction)        

    def go_to_marker(self,direction):
        if len(self.timestamps)==0:
            print('No timestamps specified!')
        elif direction == 'n':
            self._timestamp_idx += 1
            self.t_start = self.timestamps[self._timestamp_idx%len(self.timestamps)]-self.windowsize/2
        elif direction == 'b':
            self._timestamp_idx -= 1
            self.t_start = self.timestamps[self._timestamp_idx%len(self.timestamps)]-self.windowsize/2
        