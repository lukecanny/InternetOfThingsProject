# ----------------------------------------------------------------
# Import the Adafruit Bluetooth library, part of Blinka.  Technical reference:
# https://circuitpython.readthedocs.io/projects/ble/en/latest/api.html

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import threading
import post_process
# ----------------------------------------------------------------
# Initialize global variables for the main loop.
ble = BLERadio()
uart_connection = None
index = 1
data = []
# ----------------------------------------------------------------
# Begin the main processing loop.

while True:
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
            with open("output.csv", "a") as output_file:
                dataIn = uart_service.readline().decode("utf-8").rstrip()
                print(f"Index: {index}, Data: {dataIn}")

                if dataIn == "":
                    continue # discard empty data
                if not dataIn[-1] == "\n":
                    dataIn = dataIn + "\n"
                data.append(dataIn[:-1])
                if index == 30:
                    print("Triggering Plot!")
                    plot_thread = threading.Thread(target=post_process.main, args=(index, data,))
                    plot_thread.start()
                output_file.write(dataIn)
                index = index + 1
