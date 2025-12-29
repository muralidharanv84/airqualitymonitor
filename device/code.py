import time, gc
import neopixel
import board
import tinys3
import os

import sps30_uart
import pixel_wheel
import utils
import display
import networking
import telemetry

enable_pixel_wheel = True
enable_sps30 = True
enable_display = True
enable_wifi = True

# NeoPixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB)
color_index = 0

print("\nHello from TinyS3!")
print("----------------------\n")
print("Free RAM:", gc.mem_free())

# ---------- Setup ----------
if enable_pixel_wheel:
    pixel_wheel.power_up()

if enable_sps30:
    sps30_uart.wake_up()

disp = None
pm_lbl = aqi_lbl = aqi_desc_label = None
wifi_icon = None

if enable_display:
    disp = display.init_display()
    display.hello_world(disp)
    time.sleep(2)

    group, pm_lbl, aqi_lbl, aqi_desc_label = display.make_pm_aqi_labels(scale=2)
    disp.root_group = group

    wifi_icon = display.add_wifi_icon_to_group(group, display_width=240, scale=1)
    wifi_icon.set_state(display.WifiIcon.INIT)

# Network manager
net = networking.NetworkManager(healthcheck_every_s=30.0, wifi_retry_s=5.0, debug=True) if enable_wifi else None
last_net_state = None  # IMPORTANT: prevents blink timer from resetting every loop

# --- Telemetry setup ---
API_INGEST_URL = os.getenv("API_INGEST_URL")
if not API_INGEST_URL:
    raise RuntimeError("Missing API_INGEST_URL in settings.toml")

device_id, device_secret = telemetry.load_device_credentials()
tm = telemetry.TelemetryManager(
    ingest_url=API_INGEST_URL,
    device_id=device_id,
    device_secret=device_secret,
    post_every_s=60.0,
    stale_s=300.0
)
# Scheduling (monotonic timers)
PM_EVERY_S = 5.0
PIXEL_EVERY_S = 5.0
LOOP_SLEEP_S = 0.05

next_pm = 0.0
next_pixel = 0.0

# ---------- Main loop ----------
while True:
    now = time.monotonic()

    # keep blink animation responsive
    if enable_display and wifi_icon:
        wifi_icon.tick(now, period=0.5)

    # --- WiFi state machine (non-blocking) ---
    if enable_wifi and net and enable_display and wifi_icon:
        st = net.tick(now)

        # Only set state when it changes (otherwise blink never blinks)
        if st != last_net_state:
            if st == networking.NetState.INIT:
                wifi_icon.set_state(display.WifiIcon.INIT)   # blinking
            elif st == networking.NetState.ERROR:
                wifi_icon.set_state(display.WifiIcon.ERROR)  # red + X
            else:
                wifi_icon.set_state(display.WifiIcon.OK)     # solid white
            last_net_state = st

        #Update telemetry
        if st == networking.NetState.OK and net.requests:
            tm.tick(net.requests, now=now)

    # --- NeoPixel rotation (scheduled) ---
    if enable_pixel_wheel and now >= next_pixel:
        next_pixel = now + PIXEL_EVERY_S
        color_index = pixel_wheel.change(pixel, color_index)

    # --- SPS30 read + display update (scheduled) ---
    if enable_sps30 and now >= next_pm:
        next_pm = now + PM_EVERY_S

        pm25 = sps30_uart.read_pm25()
        aqi_us = utils.aqi_us_from_pm25(pm25)
        print(f"PM2.5={pm25:.1f} AQI_US={aqi_us}")
        now = time.monotonic()
        tm.update_metric("pm25_ugm3", float(pm25), ts=now)
        tm.update_metric("aqi_us", int(aqi_us), ts=now)

        if enable_display and pm_lbl and aqi_lbl and aqi_desc_label:
            display.update_pm_aqi(pm_lbl, aqi_lbl, aqi_desc_label, pm25, aqi_us)

    time.sleep(LOOP_SLEEP_S)
