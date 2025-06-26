#!/usr/bin/env python3
import os
import evdev
from evdev import InputDevice, categorize, ecodes

device_path = '/dev/input/event3'  # adjust if needed

dev = InputDevice(device_path)
print(f"Listening on {dev.path} ({dev.name})")

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keycode == "KEY_VOLUMEUP" and event.value == 2:
            os.system("hyprctl dispatch exit")
            break
        elif key_event.keycode == "KEY_VOLUMEDOWN":
            os.system('notify-send "canceled"')
            break

