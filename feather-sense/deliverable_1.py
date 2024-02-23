# Code for Feather Sense Deliverable #1
# Authors: Ciaran Harris, Luke Canny
# Date: 23/02/24

### Library Imports
import time
import digitalio
import board
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

### Declare Global Variables
# LED 
ledpin= digitalio.DigitalInOut(board.BLUE_LED)
ledpin.direction = digitalio.Direction.OUTPUT

# Bluetooth
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# Status Flags
advertised = False
connected  = False

# Timing (Sampling Rate) Variables
sampling_timer    = 0.0
last_time         = time.monotonic()
sampling_interval = 1

# Output CSV 
file_path = 'sample_data.csv'   # Input File Name - Simulated Sensor Data
index = 0                       # Index in file (Row)

### Set Up Code
# Open Sample Sensor Data
csv_file = open(file_path, 'r')
entire_file = csv_file.read()
rows = entire_file.split("\n")

### Main Loop
while True:
    
    # Check the time
    now = time.monotonic()
    interval = now - last_time
    last_time = now
    sampling_timer -= interval
    # If the interval is greater than sampling time,
    #   set the next simulated value
    if sampling_timer < 0.0:
        sampling_timer += sampling_interval
        if index < len(rows):
            x = rows[index]
            index = index + 1
        else:
            index = 0
            x = f"{rows[index]}"
            index = index + 1
    else:
        x = None

    # If the bluetooth is not advertising - Begin advertising
    if not advertised:
        ble.start_advertising(advertisement)
        print("Waiting for connection.")
        advertised = True

    # If conected flag is not enabled, but bluetooth is connected,
    #   Change the flag, turn on LED, and print message
    if not connected and ble.connected:
        print("Connection received.")
        connected = True
        ledpin.value = True
    
    # If connected (flag) is true:
    #   Check if connection is still active
    #       If not, mark connection is lost and reset flags
    #   Otherwise, print the data to bluetooth!
    if connected:
        if not ble.connected:
            print("Connection lost.")
            connected = False
            advertised = False
            ledpin.value = False            
        else:
            if x is not None:
                uart.write(x)
                