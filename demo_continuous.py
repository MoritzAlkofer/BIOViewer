import matplotlib.pyplot as plt
from viewers import ContinuousViewer
from src import ContinuousConfig
import os
import numpy as np

#path_signal = '/media/moritz/a80fe7e6-2bb9-4818-8add-17fb9bb673e1/Data/mgh_psg/continuous/121273430_2.npy'
path_signal = '/home/moritz/Desktop/programming/BIOViewer/BIOViewer/example.h5'
dtype = 'h5'
channels = ['F3', 'F4', 'C3', 'C4', 'O1', 'O2']
y_locations = [0, -100, -200, -300, -400, -500]
title='random_signal'

config = ContinuousConfig(path_signal,dtype=dtype,
                          start=0,windowsize=15,stepsize=10,
                          Fq_signal=128,
                          channels=channels,y_locations=y_locations, 
                          title=title)

ContinuousViewer(config)


