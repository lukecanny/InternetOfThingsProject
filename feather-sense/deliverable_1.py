# Code for Feather Sense for Deliverable #1
# Authors: Ciaran Harris, Luke Canny
# Date: 23/02/24

import time
import digitalio
import board


# Import the Adafruit Bluetooth library.  Technical reference:
# https://circuitpython.readthedocs.io/projects/ble/en/latest/api.html
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# ----------------------------------------------------------------
# Initialize global variables for the main loop.
ledpin= digitalio.DigitalInOut(board.BLUE_LED)
ledpin.direction = digitalio.Direction.OUTPUT

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# Flags for detecting state changes.
advertised = False
connected  = False

# The sensor sampling rate is precisely regulated using the following timer variables.
sampling_timer    = 0.0
last_time         = time.monotonic()
sampling_interval = 1

# CSV File 
file_path = 'sample_data.csv'

csv_file = open(file_path, 'r')
entire_file = csv_file.read()
rows = entire_file.split("\n")
index = 0
# csv_reader = csv.reader(csv_file)

# ----------------------------------------------------------------
# Begin the main processing loop.

while True:
    # Read the accelerometer at regular intervals.  Measure elapsed time and
    # wait until the update timer has elapsed.
    now = time.monotonic()
    interval = now - last_time
    last_time = now
    sampling_timer -= interval
    if sampling_timer < 0.0:
        sampling_timer += sampling_interval
        x, y, z = (10,20,30)
    else:
        x = None

    if not advertised:
        ble.start_advertising(advertisement)
        print("Waiting for connection.")
        advertised = True

    if not connected and ble.connected:
        print("Connection received.")
        connected = True
        ledpin.value = True
        
    if connected:
        if not ble.connected:
            print("Connection lost.")
            connected = False
            advertised = False
            ledpin.value = False            
        else:
            if x is not None:
                if index < len(rows):
                    uart.write(rows[index])
                    index = index + 1
                else:
                    index = 0
                    uart.write(f"{rows[index]}")
                    index = index + 1
                