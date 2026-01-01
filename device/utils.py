def aqi_us_from_pm25(pm25_ug_m3: float) -> int:
    """
    US EPA AQI from PM2.5 (µg/m³), using standard breakpoints.
    Returns AQI as an integer (rounded to nearest whole number).
    """
    # EPA specifies PM2.5 is truncated to 1 decimal before AQI calculation
    pm = int(pm25_ug_m3 * 10) / 10.0

    # (C_low, C_high, I_low, I_high)
    bps = [
        (0.0,   12.0,   0,  50),
        (12.1,  35.4,  51, 100),
        (35.5,  55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5,250.4, 201, 300),
        (250.5,350.4, 301, 400),
        (350.5,500.4, 401, 500),
    ]

    if pm < 0:
        raise ValueError("PM2.5 must be non-negative")

    # Cap at top breakpoint
    if pm > 500.4:
        return 500

    for c_lo, c_hi, i_lo, i_hi in bps:
        if c_lo <= pm <= c_hi:
            aqi = (i_hi - i_lo) / (c_hi - c_lo) * (pm - c_lo) + i_lo
            return int(round(aqi))

    # Should never happen
    raise RuntimeError("No breakpoint matched")

def bgr565(x):
    # x is RGB565; swap red and blue fields => BGR565
    r = (x >> 11) & 0x1F
    g = (x >> 5) & 0x3F
    b = x & 0x1F
    return (b << 11) | (g << 5) | r

def rgb888_to_565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def rgb565_to_rgb888(x):
    r5 = (x >> 11) & 0x1F
    g6 = (x >> 5) & 0x3F
    b5 = x & 0x1F
    r = (r5 * 255) // 31
    g = (g6 * 255) // 63
    b = (b5 * 255) // 31
    return (r << 16) | (g << 8) | b

def compensate_color(rgb888):
    r = (rgb888 >> 16) & 0xFF
    g = (rgb888 >> 8) & 0xFF
    b = rgb888 & 0xFF

    x = rgb888_to_565(r, g, b)  # intended RGB565

    return rgb565_to_rgb888(bgr565(x))

def get_classification_from_aqi(aqi_us):
    color = 0xFFFFFF
    desc = "Description"
    if aqi_us <= 50:
        color = 0x00E400
        desc = "Good"
    elif aqi_us <= 100:
        color = 0xFFFF00
        desc = "Moderate"
    elif aqi_us <= 150:
        color = 0xFF8C00
        desc = "Unhealthy for some"
    elif aqi_us <= 200:
        color = 0xFF0000
        desc = "Unhealthy"
    elif aqi_us <= 300:
        color = 0x8F3F97
        desc = "Very Unhealthy"
    elif aqi_us > 300:
        color = 0x7E0023
        desc = "Hazardous"
    return compensate_color(color), desc

def get_classification_from_voc_index(voc_index):
    color = 0xFFFFFF
    desc = "Description"
    if voc_index <= 150:
        color = 0x00E400
        desc = "Normal"
    elif voc_index <= 175:
        color = 0xFFFF00
        desc = "Elevated"
    elif voc_index <= 210:
        color = 0xFF8C00
        desc = "High"
    elif voc_index <= 335:
        color = 0xFF0000
        desc = "Very High"
    else:
        color = 0x7E0023
        desc = "Severe"
    return compensate_color(color), desc
