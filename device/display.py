import time
import board
import busio
import displayio
import fourwire
import terminalio
from adafruit_display_text import label
from adafruit_ili9341 import ILI9341

def init_display(rotation=0, baudrate=12000000):
    displayio.release_displays()

    spi = busio.SPI(clock=board.D36, MOSI=board.D35, MISO=board.D37)

    tft_cs = board.D5
    tft_dc = board.D6
    tft_rst = board.D7

    display_bus = fourwire.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst, baudrate=baudrate
    )

    disp = ILI9341(display_bus, width=240, height=320, rotation=rotation)
    return disp


def hello_world(disp):
    group = displayio.Group()
    text_area = label.Label(
        terminalio.FONT,
        text="Hello, world!",
        color=0xFFFF00,
        x=20,
        y=40,
        scale=2
    )
    group.append(text_area)
    disp.root_group = group

def make_pm_aqi_labels(scale=2, x=10, y=30, line_gap=28, color=0xFFFFFF):
    """
    Call once at startup. Returns (group, pm_label, aqi_label).
    Add `group` to your display root_group.
    """
    group = displayio.Group()

    pm_label = label.Label(
        terminalio.FONT,
        text="PM2.5: --.- ug/m3",
        color=color,
        x=x,
        y=y,
        scale=scale,
    )

    aqi_label = label.Label(
        terminalio.FONT,
        text="AQI: --",
        color=color,
        x=x,
        y=y + line_gap,
        scale=scale,
    )

    group.append(pm_label)
    group.append(aqi_label)
    return group, pm_label, aqi_label

def update_pm_aqi(pm_label, aqi_label, pm25, aqi):
    """
    Call from your while loop. Just updates text.
    """
    pm_label.text = f"PM2.5: {pm25:.1f} ug/m3"
    aqi_label.text = f"AQI US: {int(aqi)}"
