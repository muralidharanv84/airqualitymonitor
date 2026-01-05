import time, gc
import neopixel
import board
import busio
import tinys3
import os
import adafruit_sht4x
import adafruit_sgp40
import adafruit_scd4x
import math

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
enable_sht4x = True
enable_sgp40 = True
enable_scd40 = True

# Sensirion lab-only approximation. Valid only with the specified tuning + ethanol calibration.
def voc_index_to_tvoc_ethanol_ppb(voc_index: float) -> float:
    # Clamp to avoid log(<=0)
    vi = max(1.0, min(500.0, float(voc_index)))
    return (math.log(501.0 - vi) - 6.24) * (-381.97)

def voc_index_to_tvoc_ethanol_ppm(voc_index: float) -> float:
    return voc_index_to_tvoc_ethanol_ppb(voc_index) / 1000.0

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
dashboard_labels = None
wifi_icon = None
battery_icon = None
time_label = None

if enable_display:
    disp = display.init_display()
    group, dashboard_labels, wifi_icon, battery_icon = display.make_dashboard(
        display_width=disp.width, display_height=disp.height
    )
    disp.root_group = group

    wifi_icon.set_state(display.WifiIcon.INIT)
    battery_icon.set_state(display.BatteryIcon.CHARGING)
    time_label = display.add_time_label_to_group(
        group, display_width=disp.width, display_height=disp.height, scale=1
    )

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
SHT4X_EVERY_S = 60.0
SHT4X_FIRST_DELAY_S = 5.0
SGP40_EVERY_S = 5.0
SGP40_FIRST_DELAY_S = 7.0
SCD40_EVERY_S = 5.0
SCD40_FIRST_DELAY_S = 10.0
PIXEL_EVERY_S = 5.0
LOOP_SLEEP_S = 0.05

next_pm = 0.0
next_sht4x = 0.0
next_sgp40 = 0.0
next_scd40 = 0.0
next_pixel = 0.0
next_time = 0.0
time_synced = False
next_time_sync = 0.0
last_pm25 = None
last_aqi_us = None
last_temp_c = None
last_rh_pct = None
last_tvoc = None
last_voc_index = None

# ---------- I2C sensors ----------
i2c = busio.I2C(board.SCL, board.SDA)
sht4x = adafruit_sht4x.SHT4x(i2c) if enable_sht4x else None
sgp40 = adafruit_sgp40.SGP40(i2c) if enable_sgp40 else None
scd40 = adafruit_scd4x.SCD4X(i2c) if enable_scd40 else None
if enable_sht4x:
    next_sht4x = time.monotonic() + SHT4X_FIRST_DELAY_S
if enable_sgp40:
    next_sgp40 = time.monotonic() + SGP40_FIRST_DELAY_S
if enable_scd40 and scd40:
    scd40.start_periodic_measurement()
    next_scd40 = time.monotonic() + SCD40_FIRST_DELAY_S

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

        if net.is_connected() and not time_synced and now >= next_time_sync:
            try:
                net.sync_time()
                time_synced = True
                if enable_display and time_label:
                    display.update_time_label(time_label)
            except Exception as e:
                print(f"Time sync failed: {e}")
                next_time_sync = now + 30.0

        if not net.is_connected():
            time_synced = False
            next_time_sync = 0.0

    # --- NeoPixel rotation (scheduled) ---
    if enable_pixel_wheel and now >= next_pixel:
        next_pixel = now + PIXEL_EVERY_S
        color_index = pixel_wheel.change(pixel, color_index)

    # --- SPS30 read + display update (scheduled) ---
    if enable_sps30 and now >= next_pm:
        next_pm = now + PM_EVERY_S

        pm1, pm25, pm4, pm10 = sps30_uart.read_pm()
        aqi_us = utils.aqi_us_from_pm25(pm25)
        print(f"PM2.5={pm25:.1f} AQI_US={aqi_us} PM1={pm1:.1f} PM4={pm4:.1f} PM10={pm10:.1f}")
        last_pm25 = pm25
        last_aqi_us = aqi_us
        now = time.monotonic()
        tm.update_metric("pm25_ugm3", float(pm25), ts=now)
        tm.update_metric("aqi_us", int(aqi_us), ts=now)

        if enable_display and dashboard_labels:
            display.update_dashboard(dashboard_labels, pm25, aqi_us)

    # --- SHT4x read + serial log (scheduled) ---
    if enable_sht4x and sht4x and now >= next_sht4x:
        next_sht4x = now + SHT4X_EVERY_S
        temp_c = sht4x.temperature
        rh_pct = sht4x.relative_humidity
        print(f"Temp={temp_c:.2f}C RH={rh_pct:.1f}%")
        last_temp_c = temp_c
        last_rh_pct = rh_pct
        tm.update_metric("temp_c", float(temp_c), ts=now)
        tm.update_metric("rh_pct", float(rh_pct), ts=now)
        if enable_display and dashboard_labels:
            if last_pm25 is not None and last_aqi_us is not None:
                display.update_dashboard(
                    dashboard_labels,
                    last_pm25,
                    last_aqi_us,
                    temp_c=temp_c,
                    rh_pct=rh_pct,
                )

    # --- SGP40 read + serial log (scheduled) ---
    if enable_sgp40 and sgp40 and now >= next_sgp40:
        next_sgp40 = now + SGP40_EVERY_S
        comp_temp = last_temp_c if last_temp_c is not None else 25.0
        comp_rh = last_rh_pct if last_rh_pct is not None else 50.0
        voc_index = sgp40.measure_index(temperature=comp_temp, relative_humidity=comp_rh)
        tvoc_ppm = voc_index_to_tvoc_ethanol_ppm(voc_index)
        print(f"TVOC={tvoc_ppm:.3f}ppm VOC_INDEX={voc_index}")
        last_tvoc = tvoc_ppm
        last_voc_index = voc_index
        tm.update_metric("voc_ppm", float(tvoc_ppm), ts=now)
        tm.update_metric("voc_index", int(voc_index), ts=now)
        if enable_display and dashboard_labels:
            if last_pm25 is not None and last_aqi_us is not None:
                display.update_dashboard(
                    dashboard_labels,
                    last_pm25,
                    last_aqi_us,
                    temp_c=last_temp_c,
                    rh_pct=last_rh_pct,
                    tvoc=tvoc_ppm,
                    voc_index=voc_index,
                )

    # --- SCD40 read + serial log (scheduled) ---
    if enable_scd40 and scd40 and now >= next_scd40:
        next_scd40 = now + SCD40_EVERY_S
        if scd40.data_ready:
            co2 = scd40.CO2
            scd_temp_c = scd40.temperature
            scd_rh_pct = scd40.relative_humidity
            print(f"SCD40 CO2={co2}ppm Temp={scd_temp_c:.2f}C RH={scd_rh_pct:.1f}%")

    if enable_display and time_label and now >= next_time:
        next_time = now + 1.0
        display.update_time_label(time_label)

    time.sleep(LOOP_SLEEP_S)
