from ppadb.client import Client
import os
import cv2 as cv
import keyboard
import numpy as np

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
    with open('screen.png', 'wb') as f:
        f.write(image)

def take_screenshot(device, screen_name):
    image = device.screencap()
    with open(screen_name, 'wb') as f:
        f.write(image)

def isPower8(screen_path):
    img = cv.imread(screen_path,0)
    template = cv.imread('move_8-10.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    return np.any(res >= threshold)


def isPower0(screen_path):
    img = cv.imread(screen_path,0)
    template = cv.imread('move_0-10.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    return np.any(res >= threshold)

def main():
    img = cv.imread('screen.png',0)
    template = cv.imread('move_0-10.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 0, 255), 2)
    cv.imwrite('res.png', img)

    print("is Power 8? ", isPower8('screen.png'))
    print("is Power 0? ", isPower0('screen.png'))

if __name__ == "__main__":
    main()





