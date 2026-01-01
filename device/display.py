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
    height = len(rows)
    width = len(rows[0]) if rows else 0
    bmp = displayio.Bitmap(width, height, 2)  # 0 transparent, 1 ink
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


def _make_battery_bitmap(fill_cols=0, charging=False):
    width = 24
    height = 12
    bmp = displayio.Bitmap(width, height, 2)

    # Outline
    for x in range(0, 20):
        bmp[x, 1] = 1
        bmp[x, 10] = 1
    for y in range(2, 10):
        bmp[0, y] = 1
        bmp[19, y] = 1

    # Nub
    for x in range(20, 23):
        for y in range(4, 8):
            bmp[x, y] = 1

    # Fill
    if fill_cols > 0:
        max_cols = min(fill_cols, 18)
        for x in range(1, 1 + max_cols):
            for y in range(3, 9):
                bmp[x, y] = 1

    # Charging bolt
    if charging:
        bolt = [
            "001100",
            "011110",
            "001100",
            "011000",
            "111100",
            "001100",
        ]
        for y, row in enumerate(bolt):
            for x, ch in enumerate(row):
                if ch == "1":
                    bmp[8 + x, 3 + y] = 1

    return bmp


class BatteryIcon:
    EMPTY = 0
    QUARTER = 1
    HALF = 2
    THREE_QUARTER = 3
    FULL = 4
    CHARGING = 5

    def __init__(self, x, y, scale=1, color=0xFFFFFF):
        self.group = displayio.Group(x=x, y=y, scale=scale)

        self.pal = displayio.Palette(2)
        self.pal[0] = 0x000000
        self.pal.make_transparent(0)
        self.pal[1] = color

        self._bitmaps = {
            BatteryIcon.EMPTY: _make_battery_bitmap(fill_cols=0),
            BatteryIcon.QUARTER: _make_battery_bitmap(fill_cols=4),
            BatteryIcon.HALF: _make_battery_bitmap(fill_cols=9),
            BatteryIcon.THREE_QUARTER: _make_battery_bitmap(fill_cols=13),
            BatteryIcon.FULL: _make_battery_bitmap(fill_cols=18),
            BatteryIcon.CHARGING: _make_battery_bitmap(fill_cols=0, charging=True),
        }

        self.tg = displayio.TileGrid(self._bitmaps[BatteryIcon.EMPTY], pixel_shader=self.pal)
        self.group.append(self.tg)
        self.state = BatteryIcon.EMPTY

    def set_state(self, state):
        if state in self._bitmaps:
            self.state = state
            self.tg.bitmap = self._bitmaps[state]


def add_battery_icon_to_group(
    root_group, display_width=240, margin=4, scale=1, color=0xFFFFFF, x=None, y=None
):
    width = 24 * scale
    if x is None:
        x = display_width - width - margin
    if y is None:
        y = margin
    battery = BatteryIcon(x=x, y=y, scale=scale, color=color)
    root_group.append(battery.group)
    return battery


_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def add_time_label_to_group(root_group, display_width=240, display_height=320, margin=4, scale=1, color=0xFFFFFF):
    time_label = label.Label(
        terminalio.FONT,
        text="--- -- --:--",
        color=color,
        scale=scale,
    )
    time_label.anchor_point = (1.0, 1.0)
    time_label.anchored_position = (display_width - margin, display_height - margin)
    root_group.append(time_label)
    return time_label


def update_time_label(time_label, now=None):
    if now is None:
        now = time.localtime()
    month = _MONTHS[now.tm_mon - 1]
    time_label.text = f"{month} {now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}"


def _make_label(text, color, scale, anchor_point, anchored_position):
    lbl = label.Label(
        terminalio.FONT,
        text=text,
        color=color,
        scale=scale,
    )
    lbl.anchor_point = anchor_point
    lbl.anchored_position = anchored_position
    return lbl


def make_dashboard(display_width=240, display_height=320):
    group = displayio.Group()

    margin = 6
    icon_gap = 6
    wifi_w = 16
    battery_w = 24
    battery_x = display_width - margin - battery_w
    wifi_x = battery_x - icon_gap - wifi_w
    icon_y = margin

    wifi_icon = WifiIcon(x=wifi_x, y=icon_y, scale=1)
    group.append(wifi_icon.group)

    battery_icon = BatteryIcon(x=battery_x, y=icon_y + 2, scale=1, color=0xFFFFFF)
    group.append(battery_icon.group)

    aqi_title = _make_label(
        "AQI", 0xFFFFFF, 2, (0.5, 0.5), (display_width // 2, 44)
    )
    aqi_value = _make_label(
        "--", 0xFFFFFF, 5, (0.5, 0.5), (display_width // 2, 92)
    )
    aqi_desc = _make_label(
        " ", 0xFFFFFF, 2, (0.5, 0.5), (display_width // 2, 134)
    )

    col_x = (40, 120, 200)
    row1_label_y = 176
    row1_value_y = 200
    row1_unit_y = 220
    row2_label_y = 244
    row2_value_y = 268

    co2_label = _make_label("CO2", 0xFFFFFF, 1, (0.5, 0.5), (col_x[0], row1_label_y))
    pm25_label = _make_label("PM2.5", 0xFFFFFF, 1, (0.5, 0.5), (col_x[1], row1_label_y))
    tvoc_label = _make_label("TVOC", 0xFFFFFF, 1, (0.5, 0.5), (col_x[2], row1_label_y))

    co2_value = _make_label(" ", 0xFFFFFF, 3, (0.5, 0.5), (col_x[0], row1_value_y))
    pm25_value = _make_label("--", 0xFFFFFF, 3, (0.5, 0.5), (col_x[1], row1_value_y))
    tvoc_value = _make_label(" ", 0xFFFFFF, 3, (0.5, 0.5), (col_x[2], row1_value_y))

    co2_unit = _make_label("ppm", 0xFFFFFF, 1, (0.5, 0.5), (col_x[0], row1_unit_y))
    pm25_unit = _make_label("ug / m3", 0xFFFFFF, 1, (0.5, 0.5), (col_x[1], row1_unit_y))
    tvoc_unit = _make_label("ppm", 0xFFFFFF, 1, (0.5, 0.5), (col_x[2], row1_unit_y))

    temp_label = _make_label("Temp", 0xFFFFFF, 1, (0.5, 0.5), (col_x[0], row2_label_y))
    rh_label = _make_label("RH", 0xFFFFFF, 1, (0.5, 0.5), (col_x[1], row2_label_y))
    tvoc_index_label = _make_label("VOC Ix", 0xFFFFFF, 1, (0.5, 0.5), (col_x[2], row2_label_y))

    temp_value = _make_label(" ", 0xFFFFFF, 2, (0.5, 0.5), (col_x[0], row2_value_y))
    rh_value = _make_label(" ", 0xFFFFFF, 2, (0.5, 0.5), (col_x[1], row2_value_y))
    tvoc_index_value = _make_label(" ", 0xFFFFFF, 2, (0.5, 0.5), (col_x[2], row2_value_y))

    for item in (
        aqi_title, aqi_value, aqi_desc,
        co2_label, pm25_label, tvoc_label,
        co2_value, pm25_value, tvoc_value,
        co2_unit, pm25_unit, tvoc_unit,
        temp_label, rh_label, tvoc_index_label,
        temp_value, rh_value, tvoc_index_value,
    ):
        group.append(item)

    labels = {
        "aqi_title": aqi_title,
        "aqi_value": aqi_value,
        "aqi_desc": aqi_desc,
        "pm25_label": pm25_label,
        "pm25_value": pm25_value,
        "pm25_unit": pm25_unit,
        "co2_value": co2_value,
        "tvoc_value": tvoc_value,
        "temp_value": temp_value,
        "rh_value": rh_value,
        "tvoc_index_value": tvoc_index_value,
    }

    return group, labels, wifi_icon, battery_icon


def update_dashboard(labels, pm25, aqi, temp_c=None, rh_pct=None, tvoc=None, voc_index=None):
    color, desc = utils.get_classification_from_aqi(int(aqi))

    labels["aqi_title"].color = color
    labels["aqi_value"].text = f"{int(aqi)}"
    labels["aqi_value"].color = color
    labels["aqi_desc"].text = desc
    labels["aqi_desc"].color = color

    labels["pm25_label"].color = color
    labels["pm25_value"].text = f"{pm25:.0f}"
    labels["pm25_value"].color = color
    labels["pm25_unit"].color = color

    if temp_c is not None:
        labels["temp_value"].text = f"{temp_c:.1f}C"
    if rh_pct is not None:
        labels["rh_value"].text = f"{int(round(rh_pct))}%"
    if tvoc is not None:
        if tvoc < 1.0:
            tvoc_text = f"{tvoc:.3f}"
            if tvoc_text.startswith("0."):
                tvoc_text = tvoc_text[1:]
        elif tvoc < 10.0:
            tvoc_text = f"{tvoc:.2f}"
        elif tvoc < 100.0:
            tvoc_text = f"{tvoc:.1f}"
        else:
            tvoc_text = f"{tvoc:.0f}"
        labels["tvoc_value"].text = tvoc_text
    if voc_index is not None:
        labels["tvoc_index_value"].text = f"{int(round(voc_index))}"
