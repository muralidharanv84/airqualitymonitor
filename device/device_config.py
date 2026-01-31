DEFAULT_CONFIG = {
    "board_type": "tinys3",
    "display_invert": False,
    "display_rotation": 0,
    "enable_pixel_wheel": True,
    "enable_sps30": True,
    "enable_display": True,
    "enable_wifi": True,
    "enable_sht4x": True,
    "enable_sgp40": True,
    "enable_scd40": True,
    "scd40_altitude_m": 917,
    "enable_battery": True,
}

DEVICE_CONFIGS = {
    # All currently available sensors enabled.
    "murali-1": {
        "board_type": "waveshare_s3_lcd_28",
        "display_invert": True,
        "display_rotation": 180,
        "enable_pixel_wheel": False,
        "enable_sps30": True,
        "enable_display": True,
        "enable_wifi": True,
        "enable_sht4x": True,
        "enable_sgp40": True,
        "enable_scd40": False,
        "enable_battery": True,
        "battery_adc_pin": "IO8",
        "battery_voltage_divider": 3.0,
        "battery_voltage_offset": 0.990476,
    },
   "murali-living-room": {
        "board_type": "waveshare_s3_lcd_28",
        "display_invert": True,
        "display_rotation": 180,
        "enable_pixel_wheel": False,
        "enable_sps30": True,
        "enable_display": True,
        "enable_wifi": True,
        "enable_sht4x": False,
        "enable_sgp40": False,
        "enable_scd40": True,
        "enable_battery": False,
    },
}


def load_device_config(device_id):
    config = DEFAULT_CONFIG.copy()
    if device_id and device_id in DEVICE_CONFIGS:
        config.update(DEVICE_CONFIGS[device_id])
    return config
