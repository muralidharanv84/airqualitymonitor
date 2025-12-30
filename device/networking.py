# networking.py
import os
import time
import rtc
import wifi
import socketpool
import ssl
import adafruit_requests
import adafruit_ntp


class NetState:
    INIT = 0   # connected but not healthy yet (or still trying) -> blink
    ERROR = 1  # wifi not connected -> red X
    OK = 2     # wifi connected + healthcheck OK -> solid


class NetworkManager:
    def __init__(self, healthcheck_every_s=10.0, wifi_retry_s=5.0, debug=True):
        self.healthcheck_every_s = float(healthcheck_every_s)
        self.wifi_retry_s = float(wifi_retry_s)
        self.debug = debug

        self.requests = None
        self._socketpool = None
        self.health_ok = False

        self._next_wifi_attempt = 0.0
        self._next_healthcheck = 0.0
        self._had_wifi_failure = False

    def _log(self, msg):
        if self.debug:
            print(msg)

    def _get_session(self):
        pool = self._get_socketpool()
        return adafruit_requests.Session(pool, ssl.create_default_context())

    def _get_socketpool(self):
        if self._socketpool is None:
            self._socketpool = socketpool.SocketPool(wifi.radio)
        return self._socketpool

    def _connect_wifi_once(self):
        ssid = os.getenv("CIRCUITPY_WIFI_SSID")
        pwd = os.getenv("CIRCUITPY_WIFI_PASSWORD")
        self._log(f"Attempting WiFi connect to SSID='{ssid}'")
        if not ssid or not pwd:
            raise RuntimeError("Missing CIRCUITPY_WIFI_SSID / CIRCUITPY_WIFI_PASSWORD in settings.toml")
        wifi.radio.connect(ssid, pwd)

    def _ensure_session_if_connected(self, now):
        # Key fix: if CircuitPython auto-connects, wifi is connected but requests is None
        if wifi.radio.connected and self.requests is None:
            self._log("WiFi already connected; creating requests session")
            self.requests = self._get_session()
            self._next_healthcheck = now  # run ASAP

    def _healthcheck_ok(self):
        url = os.getenv("API_HEALTHCHECK_URL")
        self._log(f"Attempting healthcheck at: {url}")

        # If no URL yet, treat as "not healthy" so we keep blinking until you add it.
        if not url:
            return False

        try:
            r = self.requests.get(url, timeout=3)
            self._log(f"Healthcheck status: {r.status_code}")
            ok = 200 <= r.status_code < 300
            r.close()
            return ok
        except Exception as e:
            self._log(f"Healthcheck exception: {e}")
            return False

    def tick(self, now=None):
        if now is None:
            now = time.monotonic()

        # If already connected, ensure we can do HTTP
        self._ensure_session_if_connected(now)

        # If disconnected, clear state
        if not wifi.radio.connected:
            self.requests = None
            self.health_ok = False

            # Rate-limited connect attempts
            if now >= self._next_wifi_attempt:
                try:
                    self._connect_wifi_once()
                    self.requests = self._get_session()
                    self._had_wifi_failure = False
                    self._next_healthcheck = now  # check soon
                except Exception as e:
                    self._log(f"WiFi connect failed: {e}")
                    self._had_wifi_failure = True
                    self._next_wifi_attempt = now + self.wifi_retry_s
                    return NetState.ERROR

            # Before the first failure, show INIT (blink). After a failure, ERROR.
            return NetState.ERROR if self._had_wifi_failure else NetState.INIT

        # Connected: do healthcheck occasionally
        if self.requests and now >= self._next_healthcheck:
            self._next_healthcheck = now + self.healthcheck_every_s
            self.health_ok = self._healthcheck_ok()

        return NetState.OK if self.health_ok else NetState.INIT

    def is_connected(self):
        return wifi.radio.connected

    def _utc_offset_hours(self, offset_str):
        # offset_str is like "+05:30" or "-07:00" or "5.5"
        if not offset_str:
            return 0.0
        if ":" in offset_str:
            sign = -1 if offset_str[0] == "-" else 1
            hours = int(offset_str[1:3])
            minutes = int(offset_str[4:6])
            return sign * (hours + minutes / 60.0)
        return float(offset_str)

    def _timezone_offset_hours(self):
        offset = (
            os.getenv("TIMEZONE_OFFSET")
            or os.getenv("TIMEZONE_OFFSET_HOURS")
            or os.getenv("UTC_OFFSET")
        )
        if offset is None:
            return 5.5
        return self._utc_offset_hours(offset)

    def sync_time(self, timezone=None):
        if not self.is_connected():
            raise RuntimeError("WiFi not connected")

        tz_offset = self._timezone_offset_hours()
        self._log(f"Syncing time from NTP: time.google.com (tz_offset={tz_offset})")
        ntp = adafruit_ntp.NTP(self._get_socketpool(), server="time.google.com", tz_offset=tz_offset)
        rtc.RTC().datetime = ntp.datetime
        return rtc.RTC().datetime
