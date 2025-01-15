# README: Signal Visualization Library

## Overview

This library simplifies the process of managing and visualizing multi-channel signal data. It provides a high-level API to encapsulate signal data handling and visualization through flexible and intuitive classes.

The library is designed for data scientists, engineers, and researchers working with signal data, enabling them to focus on analysis and visualization without worrying about low-level implementation details.

## Features

- **Streamlined Signal Management**: Encapsulate multi-channel signal data with metadata such as sampling frequency and scale factors.
- **Dynamic Viscd ualization**: Customize signal plots with channel-specific settings (e.g., colors, labels, and scales).
- **Interactive Viewer**: Navigate through signals with keyboard controls and timestamps for quick analysis.

## Installation

``` bash
pip install BIOViewer
```

## Usage

### 1. Signal Creation
Create a Signal instance to encapsulate your data and its display settings:

```python
import numpy as np
from signal_module import Signal

# Generate example data (6 channels, 1000 time steps)
data = np.random.randn(6, 1000)

# Initialize the signal with custom settings
signal = Signal(
    data=data,
    fs=128,
    scale_factor='auto',
    y_ticks=['Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch6'],
    unit='mV',
    colors='rgbcmy',
    linewidth=1,
    show_scale=True
)
```

### 2. Visualize with the Viewer
Combine multiple signals and visualize them interactively:

```python 
from signal_module import Viewer

# Create signals
signal1 = Signal(data=data, fs=128)
signal2 = Signal(data=data, fs=128, colors='bbbkbr')

# Initialize the viewer
viewer = Viewer(
    signals=[signal1, signal2],
    figsize=(14, 4),
    t_start=0,
    windowsize=15,
    stepsize=13,
    timestamps=[10, 50, 100]
)
```

### 3. Keyboard Controls
- **Right Arrow**: Move forward in time.
- **Left Arrow**: Move backward in time.
- **n / b**: Navigate to the next/previous timestamp.
- **z**: Save the current view as an image.

### Example

```python
from signal_module import Signal, Viewer
import numpy as np

# Load example signal data
data = np.random.randn(6, 1000)
timestamps = [3, 7, 12, 21]

# Create a signal
signal = Signal(data=data, fs=128, scale_factor=220, unit='mV')

# Visualize using Viewer
viewer = Viewer(
    signals=[signal],
    timestamps=timestamps,
    windowsize=10
)
```

## Contributing
Contributions are welcome! Feel free to submit a pull request or file an issue.

## Support
For questions or issues, open a GitHub issue or contact me at [moritz.alkofer@protonmail.com].