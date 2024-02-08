# Step 1: Create a matplotlib figure and axes for the viewer.
# This serves as the visual foundation where our signal data will be displayed.
fig, ax = plt.subplots()

# Step 2: Initialize the configuration for the signal visualization.
# The ContinuousConfig class stores all necessary metadata such as the path to the signal data,
# the sampling frequency, the channel names, and their respective locations on the plot.
path_signal = 'example.npy'
channels = ['F3', 'F4', 'C3', 'C4', 'O1', 'O2']
y_locations = [0, 100,200,300,400,500]
Fq_signal = 128
title = 'Test'

config = ContinuousConfig(path_signal, Fq_signal, channels, y_locations)

# Step 3: Set up the display.
# The SignalDisplay class is responsible for the graphical representation of the signal.
# It uses the matplotlib axes created earlier and the configuration to properly display the signal.
display = SignalDisplay(ax, config)

# Step 4: Initialize the data loader.
# The ContinuousLoader class handles loading the signal data based on the configuration.
# Important: If you create a custom loader, ensure it matches the expected channel order and count as defined in the display configuration.
loader = ContinuousLoader(config)

# Step 5: Define an action handler for interactive control.
# The ActionHandler class allows us to define how the viewer responds to key presses,
# enabling us to interactively manipulate the signal display and data loading process.
actionhandler = ActionHandler(config, display, loader)

# Final Step: Connect key press events to the action handler.
# This line sets up an event listener for key presses on the figure canvas.
# When a key is pressed, it triggers the handle_key_press function, passing along the event and our defined action handler.
fig.canvas.mpl_connect('key_press_event', lambda event: handle_key_press(event, actionhandler))
