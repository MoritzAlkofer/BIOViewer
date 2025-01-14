from .signaldata import SignalData
from .signaldisplay import SignalDisplay

class Signal:
    """
    Simplified interface for managing and visualizing multi-channel signal data.

    The `Signal` class is a high-level wrapper that abstracts away the complexities of 
    signal data handling and visualization. It integrates data processing and display, 
    allowing users to focus on configuring and viewing their signals with minimal effort.

    Typical Usage:
        `Signal` instances are created to encapsulate individual signals and their display settings.
        These instances can be combined and visualized using the `Viewer` class.

    Args:
        data (np.ndarray): Multi-channel signal data, where each row represents a channel 
            and each column represents a time step.
        fs (int): Sampling frequency of the signal in Hz. 
        scale_factor (float or str, optional): Scaling factor for the signal. 
            If 'auto', the scaling factor is computed automatically. Default is 'auto'.
        y_ticks (list or str, optional): Labels for the y-axis ticks. If 'auto', default 
            tick labels are generated based on the number of channels. Default is 'auto'.
        y_locations (list or str, optional): Vertical positions of the signal channels 
            on the display. If 'auto', positions are assigned automatically. Default is 'auto'.
        unit (str, optional): Unit label for the signal, displayed on the plot. Default is 'au'.
        colors (str, optional): Specifies the colors for the signal channels. If a single 
            character is provided, the same color is applied to all channels. If the string 
            length matches the number of channels, each channel is assigned the corresponding color. 
            Default is 'k' (black).
        linewidth (float, optional): Width of the signal plot lines. Default is 0.7.
        show_scale (bool, optional): Whether to display a scale bar on the plot. Default is True.

    Example:
        ```python
        import numpy as np
        from signal_module import Signal, Viewer

        # Generate example data
        data = np.random.randn(6, 1000)  # 6 channels, 1000 time steps

        # Create Signal instances
        signal0 = Signal(data=data, fs=128, scale_factor=220, 
                         y_ticks=['a', 'b', 'c', 'd', 'e', 'f'], 
                         unit='mv', colors='bbbkbr', linewidth=1, show_scale=True)
        signal1 = Signal(data=data, fs=128)

        # Combine signals in a Viewer
        viewer = Viewer(signals=[signal0, signal1], figsize=(14, 4), timestamps=[0, 50, 100], stepsize=0.5)
        ```
    """
    def __init__(self,data,fs,scale_factor='auto',y_ticks='auto',y_locations='auto',unit='au',colors='k',linewidth=0.7,show_scale=True):
        self.data = SignalData(data,fs,scale_factor)
        n_channels = self.data.n_channels
        self.display = SignalDisplay(n_channels=n_channels,
                                     y_ticks=y_ticks,
                                     y_locations=y_locations,
                                     unit=unit,
                                     colors=colors,
                                     linewidth=linewidth,
                                     show_scale=show_scale)    