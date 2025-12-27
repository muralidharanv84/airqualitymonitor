# network.py
import os
import time
import wifi
import socketpool
import ssl
import adafruit_requests


class NetState:
    INIT = 0   # connecting or waiting for healthcheck -> blink
    ERROR = 1  # wifi not connected (after a failed attempt) -> red X
    OK = 2     # wifi connected + healthcheck OK -> solid


class NetworkManager:
    def __init__(self, healthcheck_every_s=10.0, wifi_retry_s=5.0):
        self.healthcheck_every_s = float(healthcheck_every_s)
        self.wifi_retry_s = float(wifi_retry_s)

        self.requests = None
        self.wifi_ok = False
        self.health_ok = False

        self._next_wifi_attempt = 0.0
        self._next_healthcheck = 0.0
        self._had_wifi_failure = False

    def _get_session(self):
        pool = socketpool.SocketPool(wifi.radio)
        return adafruit_requests.Session(pool, ssl.create_default_context())

    def _connect_wifi_once(self):
        ssid = os.getenv("CIRCUITPY_WIFI_SSID")
        pwd  = os.getenv("CIRCUITPY_WIFI_PASSWORD")
        print(f"Attempting to connect to wifi {ssid} / {pwd}")
        if not ssid or not pwd:
            raise RuntimeError("Missing CIRCUITPY_WIFI_SSID / CIRCUITPY_WIFI_PASSWORD in settings.toml")
        wifi.radio.connect(ssid, pwd)

    def _healthcheck_ok(self):
        # Placeholder for now:
        # If you want it to depend on a URL later, set API_HEALTHCHECK_URL in settings.toml.
        url = os.getenv("API_HEALTHCHECK_URL")
        if not url:
            return True  # placeholder: treat as healthy until you implement real API

        try:
            r = self.requests.get(url, timeout=3)
            ok = 200 <= r.status_code < 300
            r.close()
            return ok
        except Exception:
            return False

    def tick(self, now=None):
        """
        Call frequently (every loop). It will only do real work when timers fire.
        Returns NetState.INIT / ERROR / OK.
        """
        if now is None:
            now = time.monotonic()

        # Track connectivity
        if wifi.radio.connected:
            self.wifi_ok = True
        else:
            self.wifi_ok = False
            self.health_ok = False
            self.requests = None

        # Attempt connect (rate-limited)
        if not self.wifi_ok and now >= self._next_wifi_attempt:
            try:
                self._connect_wifi_once()
                self.requests = self._get_session()
                self.wifi_ok = True
                self._had_wifi_failure = False
                self._next_healthcheck = now  # check soon
            except Exception as e:
                print("WiFi connect failed:", e)
                self._had_wifi_failure = True
                self._next_wifi_attempt = now + self.wifi_retry_s
                return NetState.ERROR

        # Healthcheck (rate-limited)
        if self.wifi_ok and self.requests and now >= self._next_healthcheck:
            self._next_healthcheck = now + self.healthcheck_every_s
            self.health_ok = self._healthcheck_ok()

        # Decide state
        if not self.wifi_ok:
            return NetState.ERROR if self._had_wifi_failure else NetState.INIT

        if self.health_ok:
            return NetState.OK

        return NetState.INIT# Write your code here :-)
