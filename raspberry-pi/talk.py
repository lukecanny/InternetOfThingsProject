# Code for Raspberry Pi Deliverable #1
# Authors: Ciaran Harris, Luke Canny
# Date: 23/02/24

### Library Imports
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import threading
import post_process

### Declare Global Variables
# Bluetooth/UART
ble = BLERadio()
uart_connection = None
# Data Management
index = 1 # Count # of data recieved
data = [] # Store data in array

### Main Loop
while True:
    # If not available, try to connect
    #   Search for BT device with UART service
    if not uart_connection:
        print("Trying to connect...")
        # Check for any device advertising services
        for adv in ble.start_scan(ProvideServicesAdvertisement):
            # Print name of the device
            name = adv.complete_name
            if name:
                print(name)
            # Print what services that are being advertised
            for svc in adv.services:
                print(str(svc))
            # Look for UART service and establish connection
            if UARTService in adv.services:
                uart_connection = ble.connect(adv)
                print("Connected")
                break
        ble.stop_scan()
    # Once connected start receiving data
    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        while uart_connection.connected:
            # Open Output CSV file (for storing data permanently)
            with open("output.csv", "a") as output_file:
                # Read data in from UART service
                dataIn = uart_service.readline().decode("utf-8").rstrip()
                
                # Print data and index to console
                print(f"Index: {index}, Data: {dataIn}")

                # If the data is empty (can sometimes happen due to interference) discard it
                if dataIn == "":
                    continue
                # If the data doesn't end with a newline, insert one
                if not dataIn[-1] == "\n":
                    dataIn = dataIn + "\n"

                # Store incoming data in array (without \n)
                data.append(dataIn[:-1])

                # When the 50th data arrives, plot last 30 points
                if index == 50:
                    print("Triggering Plot!")
                    plot_thread = threading.Thread(target=post_process.main, args=(index, data,))
                    plot_thread.start()
                
                # Write the incoming data to file and increment the index
                output_file.write(dataIn)
                index = index + 1
