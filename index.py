import serial
import time

# Setup serial connection
# Make sure to replace 'COM4' with the port where your ESP32 is connected
ser = serial.Serial('COM4', 9600, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # Read a line and strip newline
            print(f"Received: {line}")
        # time.sleep(0)  # Delay to match the ESP32 sending rate
except KeyboardInterrupt:
    print("Stopped by User")
    ser.close()  # Close serial port
