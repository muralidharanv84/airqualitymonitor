import time
import board
import busio
import displayio
import fourwire
import terminalio
import utils
from adafruit_display_text import label
from adafruit_ili9341 import ILI9341

# -------- WiFi icon widget (top-right) --------

_WIFI_16 = [
    "0000000000000000",
    "0000011111100000",
    "0001110000111000",
    "0011000000001100",
    "0110001111000110",
    "0100110000110010",
    "0001100000001100",
    "0000011111100000",
    "0000001111000000",
    "0000010000100000",
    "0000000110000000",
    "0000000010000000",
    "0000000010000000",
    "0000000000000000",
    "0000000000000000",
    "0000000000000000",
]

_X_16 = [
    "0000000000000000",
    "0100000000000010",
    "0010000000000100",
    "0001000000001000",
    "0000100000010000",
    "0000010000100000",
    "0000001001000000",
    "0000000110000000",
    "0000000110000000",
    "0000001001000000",
    "0000010000100000",
    "0000100000010000",
    "0001000000001000",
    "0010000000000100",
    "0100000000000010",
    "0000000000000000",
]


def init_display(rotation=0, baudrate=12000000):
    displayio.release_displays()

    spi = busio.SPI(clock=board.D36, MOSI=board.D35, MISO=board.D37)

    tft_cs = board.D5
    tft_dc = board.D6
    tft_rst = board.D7

    display_bus = fourwire.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst, baudrate=baudrate
    )

    disp = ILI9341(
        display_bus,
        width=240, height=320,
        rotation=rotation)
    return disp


def hello_world(disp):
    group = displayio.Group()
    text_area = label.Label(
        terminalio.FONT,
        text="Hello, world!",
        color=utils.compensate_color(0x7E0023),
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

    aqi_desc_label = label.Label(
        terminalio.FONT,
        text="AQI Description",
        color=color,
        x=x,
        y=y + 2*line_gap,
        scale=scale,
    )


    group.append(pm_label)
    group.append(aqi_label)
    group.append(aqi_desc_label)
    return group, pm_label, aqi_label, aqi_desc_label

def update_pm_aqi(pm_label, aqi_label, aqi_desc_label, pm25, aqi):
    """
    Call from your while loop. Just updates text.
    """
    color, desc = utils.get_classification_from_aqi(int(aqi))
    print(f"AQI color: {hex(color)} desc: {desc}")
    pm_label.text = f"PM2.5: {pm25:.1f} ug/m3"
    aqi_label.text = f"AQI US: {int(aqi)}"
    pm_label.color = color
    aqi_label.color = color
    aqi_desc_label.text = desc
    aqi_desc_label.color = color

def _bitmap_from_str(rows):
    bmp = displayio.Bitmap(16, 16, 2)  # 0 transparent, 1 ink
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            bmp[x, y] = 1 if ch == "1" else 0
    return bmp


class WifiIcon:
    INIT = 0   # blinking white
    ERROR = 1  # red + X
    OK = 2     # solid white

    def __init__(self, x, y, scale=1):
        self.group = displayio.Group(x=x, y=y, scale=scale)

        self.pal = displayio.Palette(2)
        self.pal[0] = 0x000000
        self.pal.make_transparent(0)
        self.pal[1] = 0xFFFFFF

        self.wifi_bmp = _bitmap_from_str(_WIFI_16)
        self.x_bmp = _bitmap_from_str(_X_16)

        self.wifi_tg = displayio.TileGrid(self.wifi_bmp, pixel_shader=self.pal)
        self.x_tg = displayio.TileGrid(self.x_bmp, pixel_shader=self.pal)

        self.group.append(self.wifi_tg)
        self.group.append(self.x_tg)

        self.state = WifiIcon.INIT
        self._blink_on = True
        self._last_blink = time.monotonic()

        self.set_state(WifiIcon.INIT)

    def set_state(self, state):
        self.state = state

        if state == WifiIcon.INIT:
            self.pal[1] = 0xFFFFFF
            self.x_tg.hidden = True
            self.wifi_tg.hidden = False
            self._blink_on = True
            self._last_blink = time.monotonic()

        elif state == WifiIcon.ERROR:
            self.pal[1] = 0xFF0000
            self.wifi_tg.hidden = False
            self.x_tg.hidden = False

        elif state == WifiIcon.OK:
            self.pal[1] = 0xFFFFFF
            self.wifi_tg.hidden = False
            self.x_tg.hidden = True

    def tick(self, now=None, period=0.5):
        if self.state != WifiIcon.INIT:
            return
        if now is None:
            now = time.monotonic()
        if now - self._last_blink >= period:
            self._last_blink = now
            self._blink_on = not self._blink_on
            self.wifi_tg.hidden = not self._blink_on


def add_wifi_icon_to_group(root_group, display_width=240, margin=4, scale=1):
    size = 16 * scale
    x = display_width - size - margin
    y = margin
    wifi = WifiIcon(x=x, y=y, scale=scale)
    root_group.append(wifi.group)
    return wifi
