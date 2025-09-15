import json
import time
import requests
from datetime import datetime, timezone
from ping3 import ping

API_URL = "https://my-vercel-site.com/api/fault-log"
DEVICES_FILE = "devices.json"
CHECK_INTERVAL = 60  # seconds

def load_devices():
    with open(DEVICES_FILE, "r") as f:
        return json.load(f)

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def check_device(ip):
    try:
        response_time = ping(ip, timeout=2)
        return response_time is not None
    except Exception:
        return False

def send_status(device_id, status):
    payload = {
        "device_id": device_id,
        "status": status,
        "timestamp": get_timestamp()
    }
    try:
        r = requests.post(API_URL, json=payload, timeout=5)
        r.raise_for_status()
        print(f"[INFO] Sent status update: {payload}")
    except Exception as e:
        print(f"[ERROR] Failed to send update for {device_id}: {e}")

def main():
    devices = load_devices()
    last_status = {d["id"]: None for d in devices}

    print("[INFO] Starting device monitoring...")
    while True:
        for d in devices:
            is_up = check_device(d["ip"])
            status = "up" if is_up else "down"

            if last_status[d["id"]] != status:
                print(f"[CHANGE] {d['name']} ({d['ip']}) is now {status.upper()}")
                send_status(d["id"], status)
                last_status[d["id"]] = status
            else:
                print(f"[OK] {d['name']} is still {status.upper()}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
