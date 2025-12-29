import time
import json
import os


try:
    import adafruit_hashlib
    def _sha256(data: bytes) -> bytes:
        h = adafruit_hashlib.sha256()
        h.update(data)
        return h.digest()
except ImportError:
    raise RuntimeError("No SHA256 available. Install adafruit_hashlib (adafruit_hashlib.mpy in /lib).")


# Only allow server-approved fields (unknown fields rejected server-side)
ALLOWED_FIELDS = {
    "pm25_ugm3",
    "aqi_us",
    "co2_ppm",
    "voc_ppm",
    "voc_index",
    "temp_c",
    "rh_pct",
}

DEFAULT_STALE_S = 300.0  # 5 minutes
DEFAULT_POST_EVERY_S = 60.0

def load_device_credentials():
    """
    Looks for credentials in:
        os.getenv (settings.toml)
    Returns (device_id, device_secret_str)
    """
    device_id = os.getenv("DEVICE_ID")
    device_secret = os.getenv("DEVICE_SECRET")

    if not device_id or not device_secret:
        raise RuntimeError("Missing DEVICE_ID / DEVICE_SECRET (put them in secrets.toml or settings.toml).")

    return device_id, device_secret

def _hexlify(b: bytes) -> str:
    # CP-safe hex without binascii
    return "".join("{:02x}".format(x) for x in b)

def _hmac_sha256_hex(secret_str, body_bytes):
    # HMAC-SHA256 per RFC 2104
    key = _hexlify(_sha256(secret_str)).encode("utf-8")
    block_size = 64

    print(f"key {key} size {len(key)}")
    if len(key) > block_size:
        key = _sha256(key)
    if len(key) < block_size:
        key = key + b"\x00" * (block_size - len(key))

    o_key_pad = bytes((b ^ 0x5C) for b in key)
    i_key_pad = bytes((b ^ 0x36) for b in key)

    inner = _sha256(i_key_pad + body_bytes)
    mac = _sha256(o_key_pad + inner)

    # hex encoding without binascii dependency
    return "".join("{:02x}".format(b) for b in mac)

class MetricStore:
    """
    Stores latest metric values with timestamps and last-sent timestamps.
    """
    def __init__(self):
        # key -> {"value": v, "ts": t, "sent_ts": t or None}
        self._m = {}

    def update(self, key, value, ts=None):
        if key not in ALLOWED_FIELDS:
            raise ValueError("Metric key not allowed: %s" % key)
        if ts is None:
            ts = time.monotonic()
        rec = self._m.get(key)
        if rec is None:
            self._m[key] = {"value": value, "ts": ts, "sent_ts": None}
        else:
            rec["value"] = value
            rec["ts"] = ts

    def build_payload(self, now=None, stale_s=DEFAULT_STALE_S):
        """
        Returns (payload_dict, keys_included).
        Includes only metrics that:
          - are not stale (now - ts <= stale_s)
          - have ts > sent_ts (i.e., not reported before)
        """
        if now is None:
            now = time.monotonic()

        payload = {}
        included = []

        for k, rec in self._m.items():
            ts = rec["ts"]
            sent_ts = rec["sent_ts"]

            if (now - ts) > stale_s:
                continue
            if sent_ts is not None and ts <= sent_ts:
                continue

            payload[k] = rec["value"]
            included.append(k)

        return payload, included

    def mark_sent(self, keys, now=None):
        """
        Mark included keys as sent at their current reading timestamp.
        """
        for k in keys:
            rec = self._m.get(k)
            if rec is not None:
                rec["sent_ts"] = rec["ts"]


class IngestClient:
    def __init__(self, requests_session, ingest_url, device_id, device_secret):
        self.requests = requests_session
        self.url = ingest_url
        self.device_id = device_id
        self.device_secret = device_secret

    def post_metrics(self, payload):
        """
        Sends payload with HMAC signature over raw body bytes.
        Returns (ok_bool, server_ts_or_None, status_code)
        """
        if not payload:
            return True, None, 0

        # Canonicalize JSON to avoid accidental whitespace differences
        # CircuitPython json.dumps may not support sort_keys/separators.
        # We just sign exactly what we send.
        body = json.dumps(payload).encode("utf-8")
        sig = _hmac_sha256_hex(self.device_secret, body)

        headers = {
            "Content-Type": "application/json",
            "X-Device-Id": self.device_id,
            "X-Signature": sig,
        }

        try:
            print(f"Posting telemetry at {self.url}")
            r = self.requests.post(self.url, data=body, headers=headers, timeout=6)
            status = r.status_code
            # Expect {"ok": true, "ts": ...}
            server_ts = None
            ok = False
            try:
                j = r.json()
                ok = bool(j.get("ok", False))
                server_ts = j.get("ts")
            except Exception:
                ok = (200 <= status < 300)
            r.close()
            print(f"Telemetry status code {status}")
            return ok and (200 <= status < 300), server_ts, status
        except Exception as e:
            print(f"Telemetry exception {e}")
            return False, None, -1


class TelemetryManager:
    """
    Owns MetricStore + ingest scheduling.
    Call:
      - update_metric(...) whenever a sensor updates
      - tick(...) frequently; it posts at most once per post_every_s
    """
    def __init__(self, ingest_url, device_id, device_secret, post_every_s=DEFAULT_POST_EVERY_S, stale_s=DEFAULT_STALE_S):
        self.store = MetricStore()
        self.ingest_url = ingest_url
        self.device_id = device_id
        self.device_secret = device_secret
        self.post_every_s = float(post_every_s)
        self.stale_s = float(stale_s)
        self._next_post = 0.0

    def update_metric(self, key, value, ts=None):
        self.store.update(key, value, ts=ts)

    def tick(self, requests_session, now=None):
        """
        If due, posts all non-stale, not-yet-sent metrics.
        Only marks as sent on successful POST.
        """
        if now is None:
            now = time.monotonic()

        if now < self._next_post:
            return False

        self._next_post = now + self.post_every_s

        payload, keys = self.store.build_payload(now=now, stale_s=self.stale_s)
        if not payload:
            return False

        client = IngestClient(
            requests_session=requests_session,
            ingest_url=self.ingest_url,
            device_id=self.device_id,
            device_secret=self.device_secret,
        )
        ok, server_ts, status = client.post_metrics(payload)

        if ok:
            self.store.mark_sent(keys)
            print("Ingest OK status=%s ts=%s payload_keys=%s" % (status, server_ts, keys))
        else:
            print("Ingest FAIL status=%s payload_keys=%s" % (status, keys))

        return ok
