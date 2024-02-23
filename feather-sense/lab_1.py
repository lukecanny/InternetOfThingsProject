import time
import array
import math
import board
import audiobusio
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_bmp280 import Adafruit_BMP280_I2C
from adafruit_lis3mdl import LIS3MDL
from adafruit_sht31d import SHT31D
import neopixel

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

 # Define the onboard Neopixel
pixel_pin = board.NEOPIXEL
num_pixels = 1  # The Feather nRF52840 Sense has one onboard Neopixel
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

# check for LSM6DS33 or LSM6DS3TR-C
try:
    from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS
    lsm6ds = LSM6DS(i2c)
except RuntimeError:
    from adafruit_lsm6ds.lsm6ds3 import LSM6DS3 as LSM6DS
    lsm6ds = LSM6DS(i2c)

apds9960 = APDS9960(i2c)
bmp280 = Adafruit_BMP280_I2C(i2c)
lis3mdl = LIS3MDL(i2c)
sht31d = SHT31D(i2c)
microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                              sample_rate=16000, bit_depth=16)

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *
                             (sample - minbuf) for sample in values) / len(values)))

apds9960.enable_proximity = True
apds9960.enable_color = True

# Set this to sea level pressure in hectoPascals at your location for accurate altitude reading.
bmp280.sea_level_pressure = 1013.25

#while True:
    #samples = array.array('H', [0] * 160)
    #microphone.record(samples, len(samples))
#
    ## print("\nFeather Sense Sensor Demo")
    #print("---------------------------------------------")
    ## print(f"Proximity: {apds9960.proximity}")
    ## print(f"Red: {apds9960.color_data[0]}, Green: {apds9960.color_data[1]}, " +
    #    #   f"Blue: {apds9960.color_data[2]}, Clear: {apds9960.color_data[3]}")
    #print(f"Altitude: {bmp280.altitude:.1f} m")
    ## print(f"Magnetic: {lis3mdl.magnetic[0]:.3f} {lis3mdl.magnetic[1]:.3f} " +
    #                #   f"{lis3mdl.magnetic[2]:.3f} uTesla")
    ## print(f"Acceleration: {lsm6ds.acceleration[0]:.2f} " +
    #    #   f"{lsm6ds.acceleration[1]:.2f} {lsm6ds.acceleration[2]:.2f} m/s^2")
    ## print(f"Gyro: {lsm6ds.gyro[0]:.2f} {lsm6ds.gyro[1]:.2f} {lsm6ds.gyro[2]:.2f} dps")
    ## print(f"Sound level: {normalized_rms(samples)}")
#

counter = 0

while True:
    if bmp280.temperature > 30.0:   # If temperature levels reach a dangerous level the LED is red
        pixels.fill((255,0,0))      # Set the pixel colour to red
        pixels.show()
    elif bmp280.temperature > 24.0: # If temperature levels reach a concerning level the LED is orange
        pixels.fill((255,55,0))      # Set the pixel colour to orange
        pixels.show()
    elif bmp280.temperature > 20.0: # If temperature levels reach a worrying level the LED is yellow
        pixels.fill((255,105,0))    # Set the pixel colour to yellow
        pixels.show()
    elif bmp280.temperature < 10.0: # If temperature levels drop to cold the LED is blue
        pixels.fill((0,0,255))      # Set the pixel colour to blue
        pixels.show()  
    else:                           # If temperature levels are between 10 and 20 the LED will be green.
        pixels.fill((0,255,0))      # Set the pixel colour to green
        pixels.show()

    # If the temperature is very high and the humidity is very low, *alarm mode* - flash red on and off fast
    if bmp280.temperature > 30.0:
        if sht31d.relative_humidity < 10.0:
            while True:
                pixels.fill((255,0,0))# Ret to red
                pixels.show()
                time.sleep(0.2)       # Wait for 0.2 seconds
                pixels.fill((0,0,0))  # Set LED to white
                pixels.show()
                time.sleep(0.2)       # Wait for 0.2 seconds
    
    if counter > 2:
        print(f"Humidity: {sht31d.relative_humidity:.1f} %")
        print(f"Barometric pressure: {bmp280.pressure}")
        print(f"Temperature: {bmp280.temperature:.1f} C")
        print("============================")
        counter = 0
    counter += 1

    time.sleep(0.3) # Pause quickly before looping back