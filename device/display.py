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


def init_display(rotation=0, baudrate=12000000, board_type="auto", display_invert=False):
    def _spi_from_lcd_pins(retries=2, delay_s=0.2):
        for attempt in range(retries):
            try:
                return busio.SPI(clock=board.LCD_SCK, MOSI=board.LCD_MOSI, MISO=board.LCD_MISO)
            except ValueError as exc:
                if "in use" not in str(exc).lower() or attempt >= retries - 1:
                    raise
                try:
                    displayio.release_displays()
                except Exception:
                    pass
                time.sleep(delay_s)
        return None

    def _try_board_display():
        if hasattr(board, "DISPLAY") and board.DISPLAY is not None:
            disp = board.DISPLAY
            _ = disp.width
            _ = disp.height
            try:
                disp.rotation = rotation
            except Exception:
                pass
            return disp
        return None

    def _display_from_spi(spi, chip_select, command, reset, invert=False):
        display_bus = fourwire.FourWire(
            spi, command=command, chip_select=chip_select, reset=reset, baudrate=baudrate
        )
        try:
            return ILI9341(
                display_bus,
                width=240, height=320,
                rotation=rotation,
                invert=invert,
            )
        except TypeError:
            disp = ILI9341(
                display_bus,
                width=240, height=320,
                rotation=rotation,
            )
            if invert:
                try:
                    disp.invert = True
                except Exception:
                    pass
            return disp

    displayio.release_displays()

    if board_type == "auto":
        try:
            disp = _try_board_display()
            if disp is not None:
                return disp
        except Exception:
            pass
        if hasattr(board, "LCD_CS") and hasattr(board, "LCD_DC"):
            try:
                time.sleep(0.2)
                spi = _spi_from_lcd_pins()
                tft_cs = board.LCD_CS
                tft_dc = board.LCD_DC
                tft_rst = board.LCD_RST if hasattr(board, "LCD_RST") else None
                return _display_from_spi(spi, tft_cs, tft_dc, tft_rst, invert=display_invert)
            except Exception:
                return None
        if hasattr(board, "TFT_CS") and hasattr(board, "TFT_DC"):
            spi = board.SPI()
            tft_cs = board.TFT_CS
            tft_dc = board.TFT_DC
            tft_rst = board.TFT_RST if hasattr(board, "TFT_RST") else None
            return _display_from_spi(spi, tft_cs, tft_dc, tft_rst, invert=display_invert)
        spi = busio.SPI(clock=board.D36, MOSI=board.D35, MISO=board.D37)
        return _display_from_spi(spi, board.D5, board.D6, board.D7, invert=display_invert)

    if board_type == "waveshare_s3_lcd_28":
        try:
            time.sleep(5)
            spi = _spi_from_lcd_pins()
            tft_cs = board.LCD_CS
            tft_dc = board.LCD_DC
            tft_rst = board.LCD_RST if hasattr(board, "LCD_RST") else None
            return _display_from_spi(spi, tft_cs, tft_dc, tft_rst, invert=display_invert)
        except Exception:
            return None

    if board_type == "tinys3":
        spi = busio.SPI(clock=board.D36, MOSI=board.D35, MISO=board.D37)
        return _display_from_spi(spi, board.D5, board.D6, board.D7, invert=display_invert)

    disp = _try_board_display()
    if disp is not None:
        return disp
    return None


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


def _make_solid_background(width, height, color=0x000000):
    bmp = displayio.Bitmap(width, height, 1)
    pal = displayio.Palette(1)
    pal[0] = color
    return displayio.TileGrid(bmp, pixel_shader=pal)


def _column_centers(count, display_width):
    if count <= 0:
        return ()
    if count == 1:
        return (display_width // 2,)
    if count == 2:
        return (70, display_width - 70)
    if count == 3:
        return (40, display_width // 2, display_width - 40)
    margin = 20
    usable = display_width - (2 * margin)
    step = usable / (count - 1)
    return tuple(int(margin + (step * i)) for i in range(count))


def make_dashboard(
    display_width=240,
    display_height=320,
    enabled_sps30=True,
    enabled_scd40=True,
    enabled_sgp40=True,
    enabled_temp_rh=True,
):
    group = displayio.Group()
    group.append(_make_solid_background(display_width, display_height, color=0x000000))

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

    row1_label_y = 176
    row1_value_y = 200
    row1_unit_y = 220
    row2_label_y = 244
    row2_value_y = 268

    row1_items = []
    if enabled_scd40:
        row1_items.append(("co2", "CO2", "ppm"))
    if enabled_sps30:
        row1_items.append(("pm25", "PM2.5", "ug / m3"))
    if enabled_sgp40:
        row1_items.append(("tvoc", "TVOC", "ppm"))

    row2_items = []
    if enabled_temp_rh:
        row2_items.append(("temp", "Temp", None))
        row2_items.append(("rh", "RH", None))
    if enabled_sgp40:
        row2_items.append(("voc_index", "VOC Ix", None))

    row1_x = _column_centers(len(row1_items), display_width)
    row2_x = _column_centers(len(row2_items), display_width)

    labels = {
        "aqi_title": aqi_title,
        "aqi_value": aqi_value,
        "aqi_desc": aqi_desc,
    }

    for (key, title, unit), x in zip(row1_items, row1_x):
        label_item = _make_label(title, 0xFFFFFF, 1, (0.5, 0.5), (x, row1_label_y))
        value_item = _make_label(" ", 0xFFFFFF, 3, (0.5, 0.5), (x, row1_value_y))
        unit_item = _make_label(unit or " ", 0xFFFFFF, 1, (0.5, 0.5), (x, row1_unit_y))
        group.append(label_item)
        group.append(value_item)
        group.append(unit_item)
        labels[f"{key}_label"] = label_item
        labels[f"{key}_value"] = value_item
        labels[f"{key}_unit"] = unit_item

    for (key, title, _unit), x in zip(row2_items, row2_x):
        label_item = _make_label(title, 0xFFFFFF, 1, (0.5, 0.5), (x, row2_label_y))
        value_item = _make_label(" ", 0xFFFFFF, 2, (0.5, 0.5), (x, row2_value_y))
        group.append(label_item)
        group.append(value_item)
        labels[f"{key}_label"] = label_item
        labels[f"{key}_value"] = value_item

    for item in (aqi_title, aqi_value, aqi_desc):
        group.append(item)

    return group, labels, wifi_icon, battery_icon


def update_dashboard(labels, pm25=None, aqi=None, co2_ppm=None, temp_c=None, rh_pct=None, tvoc=None, voc_index=None):
    color = None
    if aqi is not None:
        color, desc = utils.get_classification_from_aqi(int(aqi))
        labels["aqi_title"].color = color
        labels["aqi_value"].text = f"{int(aqi)}"
        labels["aqi_value"].color = color
        labels["aqi_desc"].text = desc
        labels["aqi_desc"].color = color
    else:
        labels["aqi_title"].color = 0xFFFFFF
        labels["aqi_value"].text = "--"
        labels["aqi_value"].color = 0xFFFFFF
        labels["aqi_desc"].text = " "
        labels["aqi_desc"].color = 0xFFFFFF

    if "pm25_label" in labels:
        if pm25 is None:
            labels["pm25_value"].text = "--"
            labels["pm25_label"].color = 0xFFFFFF
            labels["pm25_value"].color = 0xFFFFFF
            labels["pm25_unit"].color = 0xFFFFFF
        else:
            labels["pm25_value"].text = f"{pm25:.0f}"
            if color is None:
                labels["pm25_label"].color = 0xFFFFFF
                labels["pm25_value"].color = 0xFFFFFF
                labels["pm25_unit"].color = 0xFFFFFF
            else:
                labels["pm25_label"].color = color
                labels["pm25_value"].color = color
                labels["pm25_unit"].color = color

    if co2_ppm is not None and "co2_label" in labels:
        co2_color, _ = utils.get_classification_from_co2(int(round(co2_ppm)))
        labels["co2_label"].color = co2_color
        labels["co2_value"].color = co2_color
        labels["co2_unit"].color = co2_color
        labels["co2_value"].text = f"{int(round(co2_ppm))}"

    if temp_c is not None and "temp_value" in labels:
        labels["temp_value"].text = f"{temp_c:.1f}C"
    if rh_pct is not None and "rh_value" in labels:
        labels["rh_value"].text = f"{int(round(rh_pct))}%"
    voc_color = None
    if voc_index is not None and "voc_index_label" in labels:
        voc_color, _ = utils.get_classification_from_voc_index(int(round(voc_index)))
        labels["voc_index_label"].color = voc_color
        labels["voc_index_value"].color = voc_color
        labels["voc_index_value"].text = f"{int(round(voc_index))}"
    if tvoc is not None and "tvoc_value" in labels:
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
        if voc_color is not None:
            labels["tvoc_label"].color = voc_color
            labels["tvoc_value"].color = voc_color
            labels["tvoc_unit"].color = voc_color
