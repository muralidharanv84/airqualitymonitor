import time, gc, os
import neopixel
import board, digitalio
import busio, struct
import tinys3
import sps30_uart
import pixel_wheel
import utils

enable_pixel_wheel = True
enable_sps30 = False

# Create a NeoPixel instance
# Brightness of 0.3 is ample for the 1515 sized LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB)
color_index = 0

# Say hello
print("\nHello from TinyS3!")
print("----------------------\n")

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

flash = os.statvfs('/')
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))

if enable_pixel_wheel:
    pixel_wheel.power_up()

if enable_sps30:
    sps30_uart.wake_up()

# Rainbow colours on the NeoPixel
while True:

    if enable_pixel_wheel:
        color_index = pixel_wheel.change(pixel, color_index)

    if enable_sps30:
        pm25 = sps30_uart.read_pm25()
        aqi_us = utils.aqi_us_from_pm25(pm25)
        print(f"PM2.5={pm25:.1f} AQI_US={aqi_us}")

    # Sleep for 150ms so the colour cycle isn't too fast
    time.sleep(1)
