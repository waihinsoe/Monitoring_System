import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Setup the serial connection (adjust the COM port as needed)
ser = serial.Serial('COM4', 9600, timeout=1)

# Prepare the plot
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, 'r')  # 'r' is the color red
plt.title("Real-time Data from ESP32")
plt.xlabel("Time")
plt.ylabel("Value")

def update(frame):
    if ser.in_waiting > 0:
        data_str = ser.readline().decode('utf-8').rstrip()
        try:
            print(data_str)
            data = float(data_str)  # Convert string to float
            y_data.append(data)
            x_data.append(len(y_data))  # Use the count of data points as x-axis
            line.set_data(x_data, y_data)
            ax.relim()  # Recalculate limits
            ax.autoscale_view()  # Autoscale the view
        except ValueError:
            print(f"Failed to convert data to float: {data_str}")
    return line,

# Keep a reference to the animation object to prevent it from being garbage collected
ani = FuncAnimation(fig, update, interval=500, save_count=200)  # `save_count` limits the cache size

# Show the plot
plt.show()
