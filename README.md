# BIOViewer


## Installation
You can install this library via pip:

``` bash
pip install BIOViewer
```

### Usage

This library is designed to help you build visualization tools for Biosignals. You can use the prebuilt viewers or use the basic modules to configure your own!
Prebuilt Modules

### Prebuilt modules:
currently there are two prebuilt modules available

**Continuous Signal Viewer**: This module is designed for viewing continuous signal data.
**Multiple Short Signal Samples Viewer**: This module is designed for viewing multiple short signal samples.

You can find demos for these modules in their respective demo.py files.
Building Your Own Viewer

### Building your own viewer
For building you can follow the structure used in the prebuilt viewers. The viewer consists of three main modules:

1. **Config Class**: Handles all the meta information about the signal, such as its title, channels, sampling rate, etc.
2. **Display Class**: Handles the display of a single signal.
3. **Loader Classes**: Handle loading the signal data for the viewer.

The viewers are structured into the following components:

**Initialization**: The __init__ module initializes the viewer.
**Actions**: The actions module modifies the information stored in the configuration class.
**Refresh Function**: The refresh function applies the modifications to the displays, axes, titles, etc.

Feel free to explore the examples and adapt them to your own use case!
