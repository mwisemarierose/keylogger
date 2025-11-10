#!/usr/bin/env python3
"""
Consented keystroke recorder for classroom/lab use only.

Usage:
  python3 consented_recorder.py

Requirements:
  pip install pynput
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from pynput import keyboard
import zipfile

# === Configuration ===
EXPORT_DIR = "recorder_exports"
EXPORT_INTERVAL = 60         # seconds; writes partial export every N seconds
FINAL_FILENAME = "final_keystrokes.json"
ZIP_NAME = "keystrokes_package.zip"

# === State ===
keystrokes = []
keystrokes_lock = threading.Lock()
running = True

def stamp():
    return datetime.utcnow().isoformat() + "Z"

def export_partial():
    """Periodically export current buffer to a timestamped file."""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR, exist_ok=True)

    with keystrokes_lock:
        data_copy = list(keystrokes)

    if not data_copy:
        # nothing to export
        schedule_next_export()
        return

    fname = os.path.join(EXPORT_DIR, f"partial_{int(time.time())}.json")
    with open(fname, "w", encoding="utf-8") as f:
        json.dump({"exported_at": stamp(), "records": data_copy}, f, indent=2)

    schedule_next_export()

def schedule_next_export():
    if running:
        t = threading.Timer(EXPORT_INTERVAL, export_partial)
        t.daemon = True
        t.start()

def on_press(key):
    try:
        keystr = key.char
    except AttributeError:
        keystr = str(key)   # special keys: Key.space, Key.enter, etc.

    with keystrokes_lock:
        keystrokes.append({"type": "press", "key": keystr, "ts": stamp()})

def on_release(key):
    try:
        keystr = key.char
    except AttributeError:
        keystr = str(key)
    with keystrokes_lock:
        keystrokes.append({"type": "release", "key": keystr, "ts": stamp()})
    # Example stopping condition: press ESC to stop (can be changed)
    if key == keyboard.Key.esc:
        stop_recorder()

def stop_recorder():
    global running
    running = False
    print("\nStopping recorder and writing final export...")
    write_final_export()
    sys.exit(0)

def write_final_export():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR, exist_ok=True)

    final_path = os.path.join(EXPORT_DIR, FINAL_FILENAME)
    with keystrokes_lock:
        with open(final_path, "w", encoding="utf-8") as f:
            json.dump({"exported_at": stamp(), "records": keystrokes}, f, indent=2)

    # package into a zip for easy sharing (consented)
    zip_path = os.path.join(EXPORT_DIR, ZIP_NAME)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(final_path, arcname=FINAL_FILENAME)
        # include any partial exports
        for fname in os.listdir(EXPORT_DIR):
            if fname.startswith("partial_"):
                z.write(os.path.join(EXPORT_DIR, fname), arcname=fname)

    print(f"Final export written to: {final_path}")
    print(f"Packaged exports to: {zip_path}")

def main():
    print("CLASSROOM CONSENT REQUIRED")
    print("This program will record keystrokes on this machine while running.")
    print("Only run it in a lab with consent from the machine owner.")
    consent = input("Type 'I CONSENT' (exactly) to proceed: ").strip()
    if consent != "I CONSENT":
        print("Consent not given. Exiting.")
        return

    print("Starting recorder. Press ESC to stop and write final export.")
    schedule_next_export()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            stop_recorder()

if __name__ == "__main__":
    main()
