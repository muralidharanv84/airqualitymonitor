import time, gc, os
import neopixel
import board, digitalio
import busio, struct
import tinys3

START_STOP = 0x7E
ESC = 0x7D
STUFF = {0x7E: 0x5E, 0x7D: 0x5D, 0x11: 0x31, 0x13: 0x33}
UNSTUFF = {v: k for k, v in STUFF.items()}

def checksum(payload: bytes) -> int:
    return (~(sum(payload) & 0xFF)) & 0xFF

def stuff_bytes(data: bytes) -> bytes:
    out = bytearray()
    for b in data:
        if b in STUFF:
            out.append(ESC); out.append(STUFF[b])
        else:
            out.append(b)
    return bytes(out)

def unstuff_bytes(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        if b == ESC:
            i += 1
            out.append(UNSTUFF[data[i]])
        else:
            out.append(b)
        i += 1
    return bytes(out)

# Use board.TX/board.RX if available on TinyS3; otherwise swap to the correct D-pins for your board.
uart = busio.UART(board.TX, board.RX, baudrate=115200, bits=8, parity=None, stop=1, timeout=0.2)

def send_cmd(cmd: int, data: bytes = b""):
    adr = 0x00
    payload = bytes([adr, cmd, len(data)]) + data
    frame = bytes([START_STOP]) + stuff_bytes(payload + bytes([checksum(payload)])) + bytes([START_STOP])
    uart.write(frame)

def read_frame(timeout=1.0):
    t0 = time.monotonic()
    buf = bytearray()
    in_frame = False
    while time.monotonic() - t0 < timeout:
        b = uart.read(1)
        if not b:
            continue
        b = b[0]
        if b == START_STOP:
            if in_frame and buf:
                return unstuff_bytes(bytes(buf))
            in_frame = True
            buf = bytearray()
        elif in_frame:
            buf.append(b)
    return None

def parse_miso(raw: bytes, expect_cmd=None):
    # raw: ADR CMD STATE LEN DATA... CHK
    if raw is None or len(raw) < 5:
        raise RuntimeError("No/short response from SPS30 (check RX/TX wiring and SEL floating)")

    adr, cmd, state, length = raw[0], raw[1], raw[2], raw[3]
    data = raw[4:4+length]
    chk  = raw[4+length] if (4+length) < len(raw) else None

    payload = raw[:-1]
    if chk is None or checksum(payload) != chk:
        raise RuntimeError("Bad checksum (noise / wrong baud / wrong pins)")

    if expect_cmd is not None and cmd != expect_cmd:
        raise RuntimeError(f"Unexpected cmd in response: got 0x{cmd:02X}, expected 0x{expect_cmd:02X}")

    err_code = state & 0x7F
    if err_code != 0:
        raise RuntimeError(f"SPS30 exec error=0x{err_code:02X}")

    return data

def wake_up():
    # ---- Wake-up sequence (safe even if not asleep) ----
    uart.write(b"\xFF")      # low pulse to enable UART interface in sleep  [oai_citation:5‡SparkFun](https://cdn.sparkfun.com/assets/4/e/e/f/8/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)
    time.sleep(0.01)
    send_cmd(0x11)           # Wake-up command  [oai_citation:6‡SparkFun](https://cdn.sparkfun.com/assets/4/e/e/f/8/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)
    try:
        parse_miso(read_frame(1.0), expect_cmd=0x11)
    except Exception:
        pass  # if it wasn't asleep, it may ignore / reject; that's fine

    # ---- Soft reset to known state ----
    send_cmd(0xD3)           # Reset  [oai_citation:7‡SparkFun](https://cdn.sparkfun.com/assets/4/e/e/f/8/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)
    try:
        parse_miso(read_frame(1.0), expect_cmd=0xD3)
    except Exception:
        pass
    time.sleep(0.5)

    # ---- Start measurement (float output) ----
    send_cmd(0x00, bytes([0x01, 0x03]))  # subcmd 0x01, format 0x03  [oai_citation:8‡SparkFun](https://cdn.sparkfun.com/assets/4/e/e/f/8/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)
    parse_miso(read_frame(1.0), expect_cmd=0x00)

    time.sleep(1.2)

def read_pm():

    send_cmd(0x03)  # Read measured values  [oai_citation:9‡SparkFun](https://cdn.sparkfun.com/assets/4/e/e/f/8/Sensirion_PM_Sensors_Datasheet_SPS30.pdf)
    data = parse_miso(read_frame(1.0), expect_cmd=0x03)

    pm1  = struct.unpack(">f", data[0:4])[0]
    pm25 = struct.unpack(">f", data[4:8])[0]
    pm4  = struct.unpack(">f", data[8:12])[0]
    pm10 = struct.unpack(">f", data[12:16])[0]

    return pm1, pm25, pm4, pm10


