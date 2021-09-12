from ppadb.client import Client
import keyboard
import cv2 as cv
import numpy as np
import time
import os


def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    else:
        print("Device Connected")
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('by_screen_capture.png', 'wb') as f:
        f.write(image)

def main():
    device_connected = connect_device()
    while True:
        if keyboard.read_key() == "q":
            take_screenshot(device_connected)


if __name__ == "__main__":
    main()