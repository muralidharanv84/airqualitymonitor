import neopixel
import tinys3

def power_up():
    print("Pixel Time!\n")
    # Create a colour wheel index int

    # Turn on the power to the NeoPixel
    tinys3.set_pixel_power(True)# Write your code here :-)

def change(pixel, color_index):
    # Get the R,G,B values of the next colour
    r,g,b = tinys3.rgb_color_wheel( color_index )
    # Set the colour on the NeoPixel
    pixel[0] = ( r, g, b, 0.5)

    print ("Changing pixels to r{} g{} b{}".format(r,g,b))
    return color_index + 1
