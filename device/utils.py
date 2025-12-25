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
