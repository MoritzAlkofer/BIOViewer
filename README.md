# BIOViewer


You can install this library via pip:

```bash
pip install BIOViewer

### Usage
This library is designed to help you built visualisation tools for Biosignals
You can use the prebuilt viewers or use the basic modules to configure your own!

There are two prebuilt modules: one for looking at a continuous signal and one for looking at multiple short signal samples.
You can find demos in their respective demo.py files.

When building your own viewer, you can orient yourself at the structure used in viewers. 

There are three main modules
* the config class handles all the meta information
* the display class handles the display of a single signal
* the loader classes handle loading the signal for the viewer

The viewers are structured into __init__, refresh, and actions. 
* the init module builds the viewer 
* the actions modify the information stored in config
* the refresh function applies the modification to the dispays, axis, titles etc