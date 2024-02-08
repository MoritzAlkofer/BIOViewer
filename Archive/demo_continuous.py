import matplotlib.pyplot as plt
from BIOViewer.viewers import ContinuousViewer
import os
import numpy as np

path_signal = 'example.npy'
channels = ['F3', 'F4', 'C3', 'C4', 'O1', 'O2']
y_locations = [0, 100,200,300,400,500]
Fq_signal = 128
title = 'Test'

viewer = ContinuousViewer(path_signal,Fq_signal,channels,y_locations)
