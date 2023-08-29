# %%
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
def create_sin_signal(time, amplitude, period, offset):
        return (0.5 + 0.5 * np.sin(
            2 * np.pi / (2 * period) * np.arange(0, len(time), 1) + offset * 2 * np.pi / (2 * period))) * amplitude

# Create a signal with a superposition of two sine waves with different periods and amplitudes  
times = pd.date_range(datetime(2000, 1, 1), datetime(2000, 2, 1), freq='3H')
values = create_sin_signal(times, 2, 10, 0) + create_sin_signal(times, 1, 3, 4) + create_sin_signal(times, 1, 24, 10)

# %%
# Find the crossings of a threshold value of 2
threshold_value = 2

# Find upward zero_crossings
upward_crossings = np.argwhere((values[:-1] < threshold_value) & (values[1:] >= threshold_value)).flatten()
downward_crossings = np.argwhere((values[:-1] >= threshold_value) & (values[1:] < threshold_value)).flatten()

# Use pandas.to_numeric() to convert the times array to a float array of timestamps
float_times = pd.to_numeric(times)

def interpolate_crossings(crossings, direction='upward'):
    interpolated_times = []
    for index in crossings:
        if values[index + 1] == threshold_value:
            # If the exact threshold value is already in the timeseries, use the corresponding time
            interpolated_times.append(times[index + 1])
        else:
            # Interpolate the time
            if direction == 'upward':
                interpolated_time = np.interp(threshold_value, [values[index], values[index + 1]], [float_times[index], float_times[index + 1]])
            elif direction == 'downward':
                interpolated_time = np.interp(threshold_value, [values[index + 1], values[index]], [float_times[index + 1], float_times[index]])
            interpolated_times.append(pd.to_datetime(interpolated_time, unit='ns'))
    return interpolated_times

interpolated_times_upward = np.array(interpolate_crossings(upward_crossings, direction='upward'))
interpolated_times_downward = np.array(interpolate_crossings(downward_crossings, direction='downward'))
# %%
# Create a plot of the upward and downward interpolated crossing times
plt.figure()
# Plot the original timeseries
plt.plot(times, values, label='Original timeseries')

# Plot the threshold value as a horizontal line
plt.axhline(y=threshold_value, color='r', linestyle='--', label=f'Threshold: {threshold_value}')

# Plot the upward interpolated times with green dots
valid_interpolated_times_upward = [t for t in interpolated_times_upward if t is not None]
valid_interpolated_values_upward = [threshold_value] * len(valid_interpolated_times_upward)
plt.scatter(valid_interpolated_times_upward, valid_interpolated_values_upward, marker='o', color='g', label='Upward Interpolated times')

# Plot the downward interpolated times with red dots
valid_interpolated_times_downward = [t for t in interpolated_times_downward if t is not None]
valid_interpolated_values_downward = [threshold_value] * len(valid_interpolated_times_downward)
plt.scatter(valid_interpolated_times_downward, valid_interpolated_values_downward, marker='o', color='red', label='Downward Interpolated times')

# Customize the plot
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()
plt.title('Original Timeseries, Upward and Downward Interpolated Times')

# Show the plot
plt.show()
# %%
# Assumption: same number of upward and downward crossings
if interpolated_times_upward[0] < interpolated_times_downward[0]:
    # The first crossing is upward
    durations = interpolated_times_upward[1::] - interpolated_times_downward
else:
    durations = interpolated_times_upward - interpolated_times_downward

for i in range(len(durations)):
    durations[i] = durations[i].total_seconds() / 3600
    
plt.figure()
plt.hist(durations, bins=int(np.max(durations)//2), density=False)
plt.xlabel("Periods below the threshold [hour]")
plt.ylabel("Count")
plt.title("Periods below the threshold")
plt.show()
# %%
