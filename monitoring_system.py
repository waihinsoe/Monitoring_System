import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Setup the serial connection (adjust the COM port as needed)
ser = serial.Serial('COM4', 9600, timeout=1)

# Create a figure with 6 subplots arranged in 3 rows and 2 columns
fig, axes = plt.subplots(3, 2, figsize=(10, 10))
fig.suptitle("Real-time Data from ESP32")
axes = axes.flatten()  # Flatten the array to make indexing easier

lines = []
data = [[] for _ in range(6)]  # Data storage for each sensor
x_data = [[] for _ in range(6)]  # X data storage for each sensor
window_size = 50  # Number of points to display on the x-axis

# Colors for each line
colors = ['r', 'g', 'b', 'y', 'm', 'c']

for idx, ax in enumerate(axes):
    ax.set_title(f"Sensor {idx + 1}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    line, = ax.plot([], [], color=colors[idx], label=f'Sensor {idx + 1}')
    lines.append(line)
    ax.legend()

def update(frame):
    if ser.in_waiting > 0:
        data_str = ser.readline().decode('utf-8').rstrip()
        values = data_str.split(',')
        if len(values) == 6:
            for i, value in enumerate(values):
                try:
                    val = float(value)
                    data[i].append(val)
                    x_data[i].append(len(x_data[i]))
                    current_x = x_data[i][-window_size:]  # Current window of x-data
                    current_y = data[i][-window_size:]  # Current window of y-data
                    lines[i].set_data(current_x, current_y)
                    axes[i].set_xlim(current_x[0], current_x[-1])  # Update x-axis limits
                    axes[i].set_ylim(min(current_y) - 1, max(current_y) + 1)  # Dynamically update y-axis limits
                    axes[i].relim()
                    axes[i].autoscale_view()
                except ValueError:
                    print(f"Failed to convert data to float: {value}")

    return lines

def init():
    for line, ax in zip(lines, axes):
        line.set_data([], [])
        ax.set_xlim(0, window_size)
        ax.set_ylim(-1, 1)  # Initialize with a default range
    return lines

ani = FuncAnimation(fig, update, init_func=init, blit=False, interval=500)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for figure title
plt.show()
